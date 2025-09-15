"""Greetings endpoint"""

from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Query, status, HTTPException
from app.models.responses import GreetingResponse, ErrorResponse
from app.config.settings import settings
from app.core.metrics import metrics


router = APIRouter()


@router.get(
    "/greet",
    response_model=GreetingResponse,
    status_code=status.HTTP_200_OK,
    summary="Greetings",
    description="Returns a personalized greeting msg",
    responses={
        200: {
            "description": "Sucessfully greeting",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Hello you!",
                        "name": "you",
                        "timestamp": "2025-09-12T10:30:00Z"
                    }
                }
            }
        },
        400: {
            "description": "Invalid name parameter",
            "model": ErrorResponse
        }
    },
    tags=["greet"]
)
async def greet_user(
    name: Optional[str] = Query(
        default=None,
        description="Name to send greeting. If it was not sent, it use a standard name to greet!",
        example="Darlei",
        min_length=1,
        max_length=100,
        # This refex filter only alphanumeric chars (a-z, A-Z, 0-9), spaces, hífens, underlines and dots
        regex=r"^[a-zA-Z0-9\s\-_\.]+$"
    )
) -> GreetingResponse:
    """
    Greetings endpoint.
    
    Returns a personalized greeting msg for the provided name.
    
    Args:
        name: Optional name to greet, it should have only 
        alphanumeric chars, spaces, hífens, underlines and dots.
    
    Returns:
        GreetingResponse: Personalized greet msg
        
    Raises:
        HTTPException: When parameters is invalid
    """
    # Use a standard name if was not sent
    if name is None:
        name = settings.default_greeting_name
    
    # Validate if name doesn't have empty after removing spaces
    name = name.strip()
    if not name:
        timestamp = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "Invalid name parameter",
                "detail": "The name can't been empty or have only spaces",
                "timestamp": timestamp
            }
        )
    
    # Save greeting request metric
    metrics.record_greet_request(name)
    
    # Generate greeting message pattern
    message = f"Hello, {name}!"
    
    # timestamp
    timestamp = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    
    return GreetingResponse(
        message=message,
        name=name,
        timestamp=timestamp
    )

"""Endpoint de verificação de saúde."""

from datetime import datetime, timezone
from fastapi import APIRouter, status
from app.models.responses import HealthResponse
from app.config.settings import settings
from app.core.metrics import metrics


router = APIRouter()


@router.get(
    "/healthz",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Healthy verification",
    description="Return application healthy state",
    responses={
        200: {
            "description": "Application is healthy",
            "content": {
                "application/json": {
                    "example": {
                        "status": "healthy",
                        "timestamp": "2025-09-12T10:30:00Z",
                        "version": "1.0.0"
                    }
                }
            }
        }
    },
    tags=["health"]
)
async def health_check() -> HealthResponse:
    """
    Endpoint to check healthy app.
    
    It returns 200 OK with the health when the app is working ok.
    
    Returns:
        HealthResponse: Status of app health
    """
    # Save the metric of health check
    metrics.record_health_check()
    
    # Generate timestamp
    timestamp = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    
    return HealthResponse(
        status="healthy",
        timestamp=timestamp,
        version=settings.app_version
    )

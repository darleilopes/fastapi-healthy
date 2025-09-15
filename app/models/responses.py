"""Response models for API endpoints."""

from typing import Dict, Any
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Health check response model."""
    
    status: str = Field(..., description="Health status", example="healthy")
    timestamp: str = Field(..., description="Response timestamp", example="2025-09-12T10:30:00Z")
    version: str = Field(..., description="App version", example="1.0.0")


class GreetingResponse(BaseModel):
    """Greeting response model."""
    
    message: str = Field(..., description="Greeting message", example="Hello, World!")
    name: str = Field(..., description="Name used to greeted", example="World")
    timestamp: str = Field(..., description="Response timestamp", example="2025-09-12T10:30:00Z")


class MetricsResponse(BaseModel):
    """Metrics response model (documentation only)."""
    
    content_type: str = Field(default="text/plain", description="Response content type")
    format: str = Field(default="prometheus", description="Metrics format")
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "content_type": "text/plain",
                "format": "prometheus",
                "note": "The actual response is Prometheus format metrics text"
            }
        }


class ErrorResponse(BaseModel):
    """Error response model."""
    
    error: str = Field(..., description="Error message", example="Invalid request")
    detail: str = Field(..., description="Error details", example="Name parameter is required")
    timestamp: str = Field(..., description="Error timestamp", example="2025-09-12T10:30:00Z")

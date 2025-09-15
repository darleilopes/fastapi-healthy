"""Endpoint de métricas Prometheus."""

from fastapi import APIRouter, Response, status
from app.core.metrics import metrics


router = APIRouter()


@router.get(
    "/metrics",
    status_code=status.HTTP_200_OK,
    summary="Prometheus metrics",
    description="returns app metrics and system in Prometheus format",
    responses={
        200: {
            "description": "Prometheus format metrics",
            "content": {
                "text/plain": {
                    "example": "# HELP http_requests_total Total HTTP requests\n# TYPE http_requests_total counter\nhttp_requests_total{method=\"GET\",endpoint=\"/healthz\",status=\"200\"} 1.0\n..."
                }
            }
        }
    },
    tags=["metrics"],
    response_class=Response
)
async def get_metrics() -> Response:
    """
    Endpoint of Prometheus metrics.
    
    Return Prometheus metrics about app and system.
    This endpoint provides:
    
    - App metrics (HTTP request, time response)
    - System metrics (CPU, memory, disk usage)
    - Process metrics (CPU, memory and file descriptors of process)
    - Personalized metrics of app (greeting requests, health checks)
    
    These metrics are automatcly updated when the endpoint is requested,
    allowing to have fresh stats of system.
    
    Returns:
        Response: Prometheus metrics format
    """
    metrics_data = metrics.get_metrics()
    content_type = metrics.get_content_type()
    
    return Response(
        content=metrics_data,
        media_type=content_type,
        status_code=status.HTTP_200_OK
    )

"""API router config."""

from fastapi import APIRouter
from app.api.v1.endpoints import health, greet, metrics


# API v1
api_v1_router = APIRouter()

api_v1_router.include_router(health.router, tags=["health"])
api_v1_router.include_router(greet.router, tags=["greet"])
api_v1_router.include_router(metrics.router, tags=["metrics"])

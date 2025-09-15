"""Módulo principal da aplicação FastAPI."""

import time
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.config.settings import settings
from app.api.router import api_v1_router
from app.core.metrics import metrics


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """    
    Manage application FastAPI lifecycle events.
    """
    # Initialization
    print(f"Starting {settings.app_name} v{settings.app_version}")
    
    # Initialize metrics with app info
    metrics.set_app_info(
        app_name=settings.app_name,
        version=settings.app_version,
        environment=settings.environment
    )
    
    print(f"Application started successfully on {settings.environment} environment")
    
    yield
    
    # Shutdown
    print(f"Shutting down {settings.app_name}")


def create_application() -> FastAPI:
    """
    Create and configure FastAPI application.

    Returns:
        FastAPI: Configured FastAPI application instance
    """
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="A clean and well structured FastAPI application with health checks, greetings and Prometheus metrics",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
        debug=settings.debug
    )
    
    # Configuring CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Adding metrics middleware
    @app.middleware("http")
    async def metrics_middleware(request: Request, call_next) -> Response:
        """Middleware to collect request metrics."""
        start_time = time.time()
        
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Record metrics
        metrics.record_request(
            method=request.method,
            endpoint=request.url.path,
            status_code=response.status_code,
            duration=duration
        )
        
        return response
    
    # Exception handlers
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
        """Handle HTTP exceptions."""
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": "HTTP Exception",
                "detail": str(exc.detail),
                "status_code": exc.status_code
            }
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        """Handle request validation errors."""
        return JSONResponse(
            status_code=422,
            content={
                "error": "Validation Error",
                "detail": exc.errors(),
                "body": exc.body
            }
        )
    
    @app.exception_handler(ValidationError)
    async def pydantic_validation_exception_handler(request: Request, exc: ValidationError) -> JSONResponse:
        """Handle Pydantic validation errors."""
        return JSONResponse(
            status_code=422,
            content={
                "error": "Validation Error",
                "detail": exc.errors()
            }
        )
    
    # Including routers
    app.include_router(api_v1_router, prefix=settings.api_v1_prefix)
    
    # Root endpoint
    @app.get(
        "/",
        summary="Root",
        description="Root endpoint with basic application information",
        tags=["root"]
    )
    async def root() -> dict:
        """Root endpoint with application information."""
        return {
            "app": settings.app_name,
            "version": settings.app_version,
            "environment": settings.environment,
            "docs_url": "/docs",
            "health_url": f"{settings.api_v1_prefix}{settings.health_path}",
            "metrics_url": f"{settings.api_v1_prefix}{settings.metrics_path}"
        }
    
    return app


app = create_application()


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        access_log=True,
        log_level="info" if not settings.debug else "debug"
    )

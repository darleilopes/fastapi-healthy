# Multi-stage Dockerfile for FastAPI Healthy application

###################
# Build Stage
###################
FROM python:3.12-slim AS builder

# OCI Labels for build stage
LABEL org.opencontainers.image.title="FastAPI healthy API - Builder"
LABEL org.opencontainers.image.description="Build stage for FastAPI healthy API app"

# Set build arguments
ARG BUILD_DATE
ARG VCS_REF
ARG VERSION="1.0.0"

# Set environment variables for build
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Create non-root user for security
RUN groupadd --gid 1000 appuser && \
    useradd --uid 1000 --gid appuser --shell /bin/bash --create-home appuser

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements first for better layer caching
COPY requirements.txt .

# Switch to appuser and install Python dependencies
USER appuser
RUN pip install --user --no-warn-script-location -r requirements.txt

# Switch back to root for runtime setup
USER root

###################
# Runtime Stage
###################
FROM python:3.12-slim AS runtime

# Set build arguments
ARG BUILD_DATE
ARG VCS_REF
ARG VERSION="1.0.0"

# OCI Image Labels - following opencontainers/image-spec
LABEL org.opencontainers.image.title="FastAPI healthy API"
LABEL org.opencontainers.image.description="A basic FastAPI application with health checks, greetings, and Prometheus metrics for Kubernetes testing propouse"
LABEL org.opencontainers.image.version="${VERSION}"
LABEL org.opencontainers.image.created="${BUILD_DATE}"
LABEL org.opencontainers.image.authors="Darlei Dal Medico Lopes <darleilopes@gmail.com>"
LABEL org.opencontainers.image.vendor="My Company"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.url="https://github.com/darleilopes/fastapi-healthy"
LABEL org.opencontainers.image.documentation="https://github.com/darleilopes/fastapi-healthy/blob/main/README.md"
LABEL org.opencontainers.image.source="https://github.com/darleilopes/fastapi-healthy"
LABEL org.opencontainers.image.revision="${VCS_REF}"
LABEL org.opencontainers.image.ref.name="fastapi-healthy:${VERSION}"

# Additional custom labels
LABEL maintainer="Darlei Dal Medico Lopes <darleilopes@gmail.com>"
LABEL application.name="fastapi-healthy"
LABEL application.version="${VERSION}"
LABEL application.component="api"
LABEL application.part-of="observability"
LABEL application.managed-by="kubernetes"

# Set runtime environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PATH="/home/appuser/.local/bin:${PATH}"

# Install runtime system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        tini \
        procps \
        && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN groupadd --gid 1000 appuser && \
    useradd --uid 1000 --gid appuser --shell /bin/bash --create-home appuser

# Set work directory
WORKDIR /app

# Copy Python dependencies from builder stage
COPY --from=builder --chown=appuser:appuser /home/appuser/.local /home/appuser/.local

# Copy application code
COPY --chown=appuser:appuser ./app ./app

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/healthz', timeout=5)" || exit 1

# Expose port
EXPOSE 8000

# Use tini as init system for proper signal handling
ENTRYPOINT ["/usr/bin/tini", "--"]

# Start application
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]

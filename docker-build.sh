#!/bin/bash

# Docker build script for FastAPI Healthy application
# This script builds the Docker image with proper OCI labels

set -e

# Configuration
IMAGE_NAME="fastapi-healthy"
IMAGE_TAG="${1:-latest}"
BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ')
VCS_REF=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
VERSION="${2:-1.0.0}"

echo "Building FastAPI Healthy Docker image..."
echo "Image: ${IMAGE_NAME}:${IMAGE_TAG}"
echo "Version: ${VERSION}"
echo "Build Date: ${BUILD_DATE}"
echo "VCS Ref: ${VCS_REF}"
echo ""

# Build the Docker image
docker build \
  --build-arg BUILD_DATE="${BUILD_DATE}" \
  --build-arg VCS_REF="${VCS_REF}" \
  --build-arg VERSION="${VERSION}" \
  --tag "${IMAGE_NAME}:${IMAGE_TAG}" \
  --tag "${IMAGE_NAME}:latest" \
  .

echo ""
echo "Build completed successfully!"
echo ""
echo "To run the container:"
echo "  docker run -p 8000:8000 ${IMAGE_NAME}:${IMAGE_TAG}"
echo ""
echo "To test the endpoints:"
echo "  curl http://localhost:8000/healthz"
echo "  curl http://localhost:8000/greet?name=Docker"
echo "  curl http://localhost:8000/metrics"
echo ""
echo "To view container labels:"
echo "  docker inspect ${IMAGE_NAME}:${IMAGE_TAG} | jq '.[0].Config.Labels'"

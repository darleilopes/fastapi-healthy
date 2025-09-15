"""Configurações e fixtures para testes."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

from app.main import create_application
from app.core.metrics import PrometheusMetrics


@pytest.fixture
def test_client():
    """Cliente de teste para a aplicação FastAPI."""
    app = create_application()
    return TestClient(app)


@pytest.fixture
def mock_metrics():
    """Mock do sistema de métricas para testes isolados."""
    mock = MagicMock(spec=PrometheusMetrics)
    mock.record_request.return_value = None
    mock.record_health_check.return_value = None
    mock.record_greet_request.return_value = None
    mock.get_metrics.return_value = "# Mock metrics data"
    mock.get_content_type.return_value = "text/plain; version=0.0.4; charset=utf-8"
    return mock


@pytest.fixture
def sample_health_response():
    """Resposta exemplo de health check."""
    return {
        "status": "healthy",
        "timestamp": "2025-09-12T10:30:00Z",
        "version": "1.0.0"
    }


@pytest.fixture
def sample_greeting_response():
    """Resposta exemplo de greeting."""
    return {
        "message": "Hello, Test!",
        "name": "Test",
        "timestamp": "2025-09-12T10:30:00Z"
    }


@pytest.fixture
def sample_app_info():
    """Informações exemplo da aplicação."""
    return {
        "app": "FastAPI Healthy",
        "version": "1.0.0",
        "environment": "development",
        "docs_url": "/docs",
        "health_url": "/healthz", 
        "metrics_url": "/metrics"
    }

"""Testes para os modelos de resposta."""

import pytest
from datetime import datetime, timezone
from pydantic import ValidationError

from app.models.responses import (
    HealthResponse,
    GreetingResponse,
    MetricsResponse,
    ErrorResponse
)


class TestHealthResponse:
    """Testes para o modelo HealthResponse."""

    def test_health_response_valid(self):
        """Testa criação válida de HealthResponse."""
        data = {
            "status": "healthy",
            "timestamp": "2025-09-12T10:30:00Z",
            "version": "1.0.0"
        }
        
        response = HealthResponse(**data)
        
        assert response.status == "healthy"
        assert response.timestamp == "2025-09-12T10:30:00Z"
        assert response.version == "1.0.0"

    def test_health_response_required_fields(self):
        """Testa campos obrigatórios do HealthResponse."""
        with pytest.raises(ValidationError):
            HealthResponse()

    def test_health_response_json_serialization(self):
        """Testa serialização JSON do HealthResponse."""
        data = {
            "status": "healthy",
            "timestamp": "2025-09-12T10:30:00Z",
            "version": "1.0.0"
        }
        
        response = HealthResponse(**data)
        json_data = response.model_dump()
        
        assert json_data == data

    def test_health_response_field_types(self):
        """Testa tipos dos campos do HealthResponse."""
        data = {
            "status": "healthy",
            "timestamp": "2025-09-12T10:30:00Z",
            "version": "1.0.0"
        }
        
        response = HealthResponse(**data)
        
        assert isinstance(response.status, str)
        assert isinstance(response.timestamp, str)
        assert isinstance(response.version, str)


class TestGreetingResponse:
    """Testes para o modelo GreetingResponse."""

    def test_greeting_response_valid(self):
        """Testa criação válida de GreetingResponse."""
        data = {
            "message": "Hello, World!",
            "name": "World",
            "timestamp": "2025-09-12T10:30:00Z"
        }
        
        response = GreetingResponse(**data)
        
        assert response.message == "Hello, World!"
        assert response.name == "World"
        assert response.timestamp == "2025-09-12T10:30:00Z"

    def test_greeting_response_required_fields(self):
        """Testa campos obrigatórios do GreetingResponse."""
        with pytest.raises(ValidationError):
            GreetingResponse()

    def test_greeting_response_partial_data(self):
        """Testa GreetingResponse com dados parciais."""
        with pytest.raises(ValidationError):
            GreetingResponse(message="Hello!")

    def test_greeting_response_json_serialization(self):
        """Testa serialização JSON do GreetingResponse."""
        data = {
            "message": "Hello, Test!",
            "name": "Test",
            "timestamp": "2025-09-12T10:30:00Z"
        }
        
        response = GreetingResponse(**data)
        json_data = response.model_dump()
        
        assert json_data == data

    def test_greeting_response_special_characters(self):
        """Testa GreetingResponse com caracteres especiais."""
        data = {
            "message": "Hello, João!",
            "name": "João",
            "timestamp": "2025-09-12T10:30:00Z"
        }
        
        response = GreetingResponse(**data)
        
        assert response.message == "Hello, João!"
        assert response.name == "João"


class TestMetricsResponse:
    """Testes para o modelo MetricsResponse."""

    def test_metrics_response_defaults(self):
        """Testa valores padrão do MetricsResponse."""
        response = MetricsResponse()
        
        assert response.content_type == "text/plain"
        assert response.format == "prometheus"

    def test_metrics_response_custom_values(self):
        """Testa MetricsResponse com valores customizados."""
        data = {
            "content_type": "application/json",
            "format": "json"
        }
        
        response = MetricsResponse(**data)
        
        assert response.content_type == "application/json"
        assert response.format == "json"

    def test_metrics_response_json_serialization(self):
        """Testa serialização JSON do MetricsResponse."""
        response = MetricsResponse()
        json_data = response.model_dump()
        
        expected = {
            "content_type": "text/plain",
            "format": "prometheus"
        }
        
        assert json_data == expected


class TestErrorResponse:
    """Testes para o modelo ErrorResponse."""

    def test_error_response_valid(self):
        """Testa criação válida de ErrorResponse."""
        data = {
            "error": "Validation Error",
            "detail": "Invalid input",
            "timestamp": "2025-09-12T10:30:00Z"
        }
        
        response = ErrorResponse(**data)
        
        assert response.error == "Validation Error"
        assert response.detail == "Invalid input"
        assert response.timestamp == "2025-09-12T10:30:00Z"

    def test_error_response_required_fields(self):
        """Testa campos obrigatórios do ErrorResponse."""
        with pytest.raises(ValidationError):
            ErrorResponse()

    def test_error_response_json_serialization(self):
        """Testa serialização JSON do ErrorResponse."""
        data = {
            "error": "Test Error",
            "detail": "Test detail",
            "timestamp": "2025-09-12T10:30:00Z"
        }
        
        response = ErrorResponse(**data)
        json_data = response.model_dump()
        
        assert json_data == data

    def test_error_response_field_types(self):
        """Testa tipos dos campos do ErrorResponse."""
        data = {
            "error": "Test Error",
            "detail": "Test detail",
            "timestamp": "2025-09-12T10:30:00Z"
        }
        
        response = ErrorResponse(**data)
        
        assert isinstance(response.error, str)
        assert isinstance(response.detail, str)
        assert isinstance(response.timestamp, str)


class TestResponseModelsIntegration:
    """Testes de integração dos modelos de resposta."""

    def test_all_models_with_timestamp(self):
        """Testa todos os modelos que incluem timestamp."""
        timestamp = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        
        health = HealthResponse(
            status="healthy",
            timestamp=timestamp,
            version="1.0.0"
        )
        
        greeting = GreetingResponse(
            message="Hello, Test!",
            name="Test",
            timestamp=timestamp
        )
        
        error = ErrorResponse(
            error="Test Error",
            detail="Test detail",
            timestamp=timestamp
        )
        
        assert health.timestamp == timestamp
        assert greeting.timestamp == timestamp
        assert error.timestamp == timestamp

    def test_models_serialization_consistency(self):
        """Testa consistência na serialização dos modelos."""
        models = [
            HealthResponse(status="healthy", timestamp="2025-09-12T10:30:00Z", version="1.0.0"),
            GreetingResponse(message="Hello!", name="Test", timestamp="2025-09-12T10:30:00Z"),
            MetricsResponse(),
            ErrorResponse(error="Error", detail="Detail", timestamp="2025-09-12T10:30:00Z")
        ]
        
        for model in models:
            json_data = model.model_dump()
            assert isinstance(json_data, dict)
            assert len(json_data) > 0

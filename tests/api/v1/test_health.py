"""Testes para o endpoint de health check."""

import pytest
from unittest.mock import patch
from datetime import datetime, timezone


class TestHealthEndpoint:
    """Testes para o endpoint de health check."""

    def test_health_check_success(self, test_client):
        """Testa o health check bem-sucedido."""
        response = test_client.get("/api/v1/healthz")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "version" in data
        assert data["version"] == "1.0.0"

    def test_health_check_response_structure(self, test_client):
        """Testa a estrutura da resposta do health check."""
        response = test_client.get("/api/v1/healthz")
        
        assert response.status_code == 200
        data = response.json()
        
        required_fields = ["status", "timestamp", "version"]
        for field in required_fields:
            assert field in data
            assert data[field] is not None

    def test_health_check_timestamp_format(self, test_client):
        """Testa o formato do timestamp na resposta."""
        response = test_client.get("/api/v1/healthz")
        
        assert response.status_code == 200
        data = response.json()
        
        timestamp = data["timestamp"]
        assert timestamp.endswith("Z")
        
        # Verifica se o timestamp pode ser parseado
        parsed_time = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        assert parsed_time.tzinfo == timezone.utc

    def test_health_check_content_type(self, test_client):
        """Testa o content-type da resposta."""
        response = test_client.get("/api/v1/healthz")
        
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"

    @patch('app.core.metrics.metrics.record_health_check')
    def test_health_check_metrics_recorded(self, mock_record, test_client):
        """Testa se as métricas de health check são registradas."""
        response = test_client.get("/api/v1/healthz")
        
        assert response.status_code == 200
        mock_record.assert_called_once()

    def test_health_check_multiple_calls(self, test_client):
        """Testa múltiplas chamadas do health check."""
        for _ in range(3):
            response = test_client.get("/api/v1/healthz")
            assert response.status_code == 200
            
            data = response.json()
            assert data["status"] == "healthy"

    def test_health_check_response_time(self, test_client):
        """Testa o tempo de resposta do health check."""
        import time
        
        start_time = time.time()
        response = test_client.get("/api/v1/healthz")
        end_time = time.time()
        
        assert response.status_code == 200
        
        # Health check deve ser rápido (< 1 segundo)
        response_time = end_time - start_time
        assert response_time < 1.0

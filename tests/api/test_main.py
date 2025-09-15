"""Testes para o módulo principal da aplicação."""

import pytest
from fastapi.testclient import TestClient

from app.main import create_application


class TestMainApplication:
    """Testes para a aplicação principal."""

    def test_create_application(self):
        """Testa se a aplicação é criada corretamente."""
        app = create_application()
        
        assert app.title == "FastAPI Healthy"
        assert app.version == "1.0.0"
        assert app.docs_url == "/docs"
        assert app.redoc_url == "/redoc"
        assert app.openapi_url == "/openapi.json"

    def test_root_endpoint(self, test_client, sample_app_info):
        """Testa o endpoint raiz da aplicação."""
        response = test_client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["app"] == sample_app_info["app"]
        assert data["version"] == sample_app_info["version"]
        assert data["environment"] == sample_app_info["environment"]
        assert "docs_url" in data
        assert "health_url" in data
        assert "metrics_url" in data

    def test_root_endpoint_structure(self, test_client):
        """Testa a estrutura da resposta do endpoint raiz."""
        response = test_client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        
        required_fields = ["app", "version", "environment", "docs_url", "health_url", "metrics_url"]
        for field in required_fields:
            assert field in data
            assert data[field] is not None

    def test_openapi_schema(self, test_client):
        """Testa se o schema OpenAPI está disponível."""
        response = test_client.get("/openapi.json")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "openapi" in data
        assert "info" in data
        assert "paths" in data
        assert data["info"]["title"] == "FastAPI Healthy"

    def test_404_error_handling(self, test_client):
        """Testa o tratamento de erro 404."""
        response = test_client.get("/endpoint-inexistente")
        
        assert response.status_code == 404
        data = response.json()
        
        assert "error" in data
        assert data["error"] == "HTTP Exception"
        assert "detail" in data
        assert "status_code" in data

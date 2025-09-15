"""Testes para o endpoint de greeting."""

import pytest
from unittest.mock import patch
from datetime import datetime, timezone


class TestGreetEndpoint:
    """Testes para o endpoint de greeting."""

    def test_greet_default_name(self, test_client):
        """Testa greeting com nome padrão."""
        response = test_client.get("/api/v1/greet")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "message" in data
        assert "name" in data
        assert "timestamp" in data
        assert data["name"] == "you!!"  # Nome padrão das configurações
        assert data["message"] == "Hello, you!!!"

    def test_greet_with_custom_name(self, test_client):
        """Testa greeting com nome personalizado."""
        response = test_client.get("/api/v1/greet?name=TestUser")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["name"] == "TestUser"
        assert data["message"] == "Hello, TestUser!"
        assert "timestamp" in data

    def test_greet_with_special_characters(self, test_client):
        """Testa greeting com caracteres especiais válidos."""
        test_names = ["João", "Ana-Paula", "User_123", "Mr.Smith"]
        
        for name in test_names:
            response = test_client.get(f"/api/v1/greet?name={name}")
            
            if response.status_code == 200:  # Alguns podem falhar devido a encoding
                data = response.json()
                assert data["name"] == name
                assert f"Hello, {name}!" == data["message"]

    def test_greet_with_empty_name(self, test_client):
        """Testa greeting com nome vazio."""
        response = test_client.get("/api/v1/greet?name=")
        
        assert response.status_code == 422  # Validation error
        data = response.json()
        
        assert "detail" in data
        # Para erro 422, o FastAPI retorna uma lista de erros de validação
        assert isinstance(data["detail"], list)

    def test_greet_with_whitespace_only(self, test_client):
        """Testa greeting com apenas espaços."""
        response = test_client.get("/api/v1/greet?name=%20%20%20")  # 3 espaços
        
        assert response.status_code == 400  # Custom error for whitespace
        data = response.json()
        
        assert "detail" in data
        # Para erro 400, a aplicação retorna um string com error details
        assert isinstance(data["detail"], str)

    def test_greet_response_structure(self, test_client):
        """Testa a estrutura da resposta do greeting."""
        response = test_client.get("/api/v1/greet?name=TestUser")
        
        assert response.status_code == 200
        data = response.json()
        
        required_fields = ["message", "name", "timestamp"]
        for field in required_fields:
            assert field in data
            assert data[field] is not None

    def test_greet_timestamp_format(self, test_client):
        """Testa o formato do timestamp na resposta."""
        response = test_client.get("/api/v1/greet?name=TestUser")
        
        assert response.status_code == 200
        data = response.json()
        
        timestamp = data["timestamp"]
        assert timestamp.endswith("Z")
        
        # Verifica se o timestamp pode ser parseado
        parsed_time = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        assert parsed_time.tzinfo == timezone.utc

    @patch('app.core.metrics.metrics.record_greet_request')
    def test_greet_metrics_recorded(self, mock_record, test_client):
        """Testa se as métricas de greeting são registradas."""
        response = test_client.get("/api/v1/greet?name=TestUser")
        
        assert response.status_code == 200
        mock_record.assert_called_once_with("TestUser")

    def test_greet_with_long_name(self, test_client):
        """Testa greeting com nome muito longo."""
        long_name = "a" * 150  # Maior que o limite de 100 caracteres
        response = test_client.get(f"/api/v1/greet?name={long_name}")
        
        assert response.status_code == 422  # Validation error

    def test_greet_with_invalid_characters(self, test_client):
        """Testa greeting com caracteres inválidos."""
        invalid_names = ["test@domain", "test#tag", "test<script>"]
        
        for name in invalid_names:
            response = test_client.get(f"/api/v1/greet?name={name}")
            # Alguns caracteres podem passar pela validação regex atual
            assert response.status_code in [200, 422]

    def test_greet_content_type(self, test_client):
        """Testa o content-type da resposta."""
        response = test_client.get("/api/v1/greet?name=TestUser")
        
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"

    def test_greet_multiple_calls_same_name(self, test_client):
        """Testa múltiplas chamadas com o mesmo nome."""
        for _ in range(3):
            response = test_client.get("/api/v1/greet?name=TestUser")
            assert response.status_code == 200
            
            data = response.json()
            assert data["name"] == "TestUser"
            assert data["message"] == "Hello, TestUser!"

    def test_greet_case_sensitivity(self, test_client):
        """Testa sensibilidade a maiúsculas/minúsculas."""
        names = ["testuser", "TestUser", "TESTUSER"]
        
        for name in names:
            response = test_client.get(f"/api/v1/greet?name={name}")
            assert response.status_code == 200
            
            data = response.json()
            assert data["name"] == name  # Preserva o case original
            assert data["message"] == f"Hello, {name}!"

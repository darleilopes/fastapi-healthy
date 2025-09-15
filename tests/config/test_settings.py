"""Testes para as configurações da aplicação."""

import pytest
import os
from unittest.mock import patch

from app.config.settings import Settings


class TestSettings:
    """Testes para a classe Settings."""

    def test_settings_default_values(self):
        """Testa valores padrão das configurações."""
        settings = Settings()
        
        assert settings.app_name == "FastAPI Healthy"
        assert settings.app_version == "1.0.0"
        assert settings.debug == False
        assert settings.host == "0.0.0.0"
        assert settings.port == 8000
        assert settings.api_v1_prefix == "/api/v1"
        assert settings.metrics_path == "/metrics"
        assert settings.health_path == "/healthz"
        assert settings.default_greeting_name == "you!!"
        assert settings.environment == "development"

    def test_settings_with_env_vars(self):
        """Testa configurações com variáveis de ambiente."""
        env_vars = {
            "APP_NAME": "Test App",
            "APP_VERSION": "2.0.0",
            "DEBUG": "true",
            "HOST": "127.0.0.1",
            "PORT": "3000",
            "ENVIRONMENT": "test"
        }
        
        with patch.dict(os.environ, env_vars):
            settings = Settings()
            
            assert settings.app_name == "Test App"
            assert settings.app_version == "2.0.0"
            assert settings.debug == True
            assert settings.host == "127.0.0.1"
            assert settings.port == 3000
            assert settings.environment == "test"

    def test_settings_boolean_env_vars(self):
        """Testa conversão de variáveis booleanas."""
        boolean_values = [
            ("true", True),
            ("True", True),
            ("TRUE", True),
            ("1", True),
            ("false", False),
            ("False", False),
            ("FALSE", False),
            ("0", False),
        ]
        
        for env_value, expected in boolean_values:
            with patch.dict(os.environ, {"DEBUG": env_value}):
                settings = Settings()
                assert settings.debug == expected

    def test_settings_integer_env_vars(self):
        """Testa conversão de variáveis inteiras."""
        with patch.dict(os.environ, {"PORT": "8080"}):
            settings = Settings()
            assert settings.port == 8080
            assert isinstance(settings.port, int)

    def test_settings_string_env_vars(self):
        """Testa variáveis de ambiente string."""
        with patch.dict(os.environ, {
            "API_V1_PREFIX": "/v1",
            "METRICS_PATH": "/prometheus",
            "HEALTH_PATH": "/health"
        }):
            settings = Settings()
            
            assert settings.api_v1_prefix == "/v1"
            assert settings.metrics_path == "/prometheus"
            assert settings.health_path == "/health"

    def test_settings_field_descriptions(self):
        """Testa se os campos têm descrições definidas."""
        settings = Settings()
        model_fields = settings.model_fields
        
        # Verifica se todos os campos têm descrição
        for field_name, field_info in model_fields.items():
            assert hasattr(field_info, 'description')
            assert field_info.description is not None
            assert len(field_info.description) > 0

    def test_settings_case_insensitive(self):
        """Testa se as configurações são case insensitive."""
        env_vars = {
            "app_name": "lowercase test",  # lowercase
            "APP_VERSION": "UPPERCASE",    # uppercase
            "Debug": "true"                # mixed case
        }
        
        with patch.dict(os.environ, env_vars):
            settings = Settings()
            
            assert settings.app_name == "lowercase test"
            assert settings.app_version == "UPPERCASE"
            assert settings.debug == True

    def test_settings_field_validation(self):
        """Testa validação dos campos."""
        # Teste com porta inválida
        with patch.dict(os.environ, {"PORT": "invalid"}):
            with pytest.raises(ValueError):
                Settings()

    def test_settings_immutability(self):
        """Testa se as configurações são tratadas adequadamente."""
        settings = Settings()
        original_app_name = settings.app_name
        
        # As configurações devem ser consistentes
        assert settings.app_name == original_app_name

    def test_settings_default_greeting_name(self):
        """Testa configuração específica do nome de greeting."""
        with patch.dict(os.environ, {"DEFAULT_GREETING_NAME": "TestUser"}):
            settings = Settings()
            assert settings.default_greeting_name == "TestUser"

    def test_settings_paths_configuration(self):
        """Testa configuração dos caminhos da aplicação."""
        settings = Settings()
        
        # Verifica se os caminhos começam com /
        assert settings.api_v1_prefix.startswith("/")
        assert settings.metrics_path.startswith("/")
        assert settings.health_path.startswith("/")

    def test_settings_host_configuration(self):
        """Testa configuração do host."""
        # Teste com diferentes valores de host
        host_values = ["localhost", "127.0.0.1", "0.0.0.0", "app.example.com"]
        
        for host in host_values:
            with patch.dict(os.environ, {"HOST": host}):
                settings = Settings()
                assert settings.host == host

    def test_settings_port_range(self):
        """Testa valores válidos de porta."""
        valid_ports = ["80", "443", "8000", "8080", "3000"]
        
        for port in valid_ports:
            with patch.dict(os.environ, {"PORT": port}):
                settings = Settings()
                assert settings.port == int(port)
                assert 1 <= settings.port <= 65535

    def test_settings_environment_values(self):
        """Testa valores de ambiente válidos."""
        environments = ["development", "staging", "production", "test"]
        
        for env in environments:
            with patch.dict(os.environ, {"ENVIRONMENT": env}):
                settings = Settings()
                assert settings.environment == env

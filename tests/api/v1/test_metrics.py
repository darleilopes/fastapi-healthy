"""Testes para o endpoint de métricas."""

import pytest
from unittest.mock import patch, MagicMock


class TestMetricsEndpoint:
    """Testes para o endpoint de métricas."""

    def test_metrics_endpoint_success(self, test_client):
        """Testa se o endpoint de métricas retorna sucesso."""
        response = test_client.get("/api/v1/metrics")
        
        assert response.status_code == 200
        assert "text/plain" in response.headers["content-type"]

    def test_metrics_content_format(self, test_client):
        """Testa o formato do conteúdo das métricas."""
        response = test_client.get("/api/v1/metrics")
        
        assert response.status_code == 200
        content = response.text
        
        # Verifica se contém elementos básicos do formato Prometheus
        assert "# HELP" in content or "# TYPE" in content

    @patch('app.core.metrics.metrics.get_metrics')
    @patch('app.core.metrics.metrics.get_content_type')
    def test_metrics_mock_response(self, mock_content_type, mock_get_metrics, test_client):
        """Testa o endpoint com métricas mockadas."""
        # Configurar mocks
        mock_get_metrics.return_value = "# HELP test_metric Test metric\n# TYPE test_metric counter\ntest_metric 1.0"
        mock_content_type.return_value = "text/plain; version=0.0.4; charset=utf-8"
        
        response = test_client.get("/api/v1/metrics")
        
        assert response.status_code == 200
        assert "test_metric 1.0" in response.text
        mock_get_metrics.assert_called_once()
        mock_content_type.assert_called_once()

    def test_metrics_content_type_header(self, test_client):
        """Testa o header content-type das métricas."""
        response = test_client.get("/api/v1/metrics")
        
        assert response.status_code == 200
        content_type = response.headers["content-type"]
        assert "text/plain" in content_type

    def test_metrics_response_not_empty(self, test_client):
        """Testa se a resposta de métricas não está vazia."""
        response = test_client.get("/api/v1/metrics")
        
        assert response.status_code == 200
        assert len(response.text) > 0

    def test_metrics_response_structure(self, test_client):
        """Testa a estrutura da resposta de métricas."""
        response = test_client.get("/api/v1/metrics")
        
        assert response.status_code == 200
        content = response.text
        
        # Verifica se contém pelo menos algumas métricas esperadas
        expected_metrics = [
            "http_requests_total",
            "app_info",
            "system_cpu_usage_percent"
        ]
        
        # Pelo menos uma das métricas deve estar presente
        assert any(metric in content for metric in expected_metrics)

    def test_metrics_multiple_calls(self, test_client):
        """Testa múltiplas chamadas ao endpoint de métricas."""
        for _ in range(3):
            response = test_client.get("/api/v1/metrics")
            assert response.status_code == 200
            assert len(response.text) > 0

    @patch('app.core.metrics.metrics.update_system_metrics')
    @patch('app.core.metrics.metrics.update_process_metrics')
    def test_metrics_updates_called(self, mock_process, mock_system, test_client):
        """Testa se as atualizações de métricas são chamadas."""
        response = test_client.get("/api/v1/metrics")
        
        assert response.status_code == 200
        # As métricas devem ser atualizadas quando o endpoint é chamado
        mock_system.assert_called()
        mock_process.assert_called()

    def test_metrics_performance(self, test_client):
        """Testa a performance do endpoint de métricas."""
        import time
        
        start_time = time.time()
        response = test_client.get("/api/v1/metrics")
        end_time = time.time()
        
        assert response.status_code == 200
        
        # Endpoint de métricas deve ser razoavelmente rápido (< 2 segundos)
        response_time = end_time - start_time
        assert response_time < 2.0

    def test_metrics_encoding(self, test_client):
        """Testa a codificação da resposta de métricas."""
        response = test_client.get("/api/v1/metrics")
        
        assert response.status_code == 200
        # Verifica se a resposta pode ser decodificada como UTF-8
        content = response.content.decode('utf-8')
        assert len(content) > 0

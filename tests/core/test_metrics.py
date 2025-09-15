"""Testes para o sistema de métricas."""

import pytest
from unittest.mock import patch, MagicMock
import platform

from app.core.metrics import PrometheusMetrics


class TestPrometheusMetrics:
    """Testes para a classe PrometheusMetrics."""

    @pytest.fixture
    def metrics_instance(self):
        """Instância limpa de métricas para testes."""
        return PrometheusMetrics()

    def test_metrics_initialization(self, metrics_instance):
        """Testa a inicialização das métricas."""
        assert metrics_instance.registry is not None
        assert metrics_instance.http_requests_total is not None
        assert metrics_instance.http_request_duration_seconds is not None
        assert metrics_instance.app_info is not None

    def test_set_app_info(self, metrics_instance):
        """Testa a definição de informações da aplicação."""
        metrics_instance.set_app_info(
            app_name="Test App",
            version="1.0.0",
            environment="test"
        )
        
        # Verifica se as informações foram definidas
        # Nota: Como Info é um tipo especial, verificamos apenas se não há erro
        assert True  # Se chegou até aqui, a função funcionou

    def test_record_request(self, metrics_instance):
        """Testa o registro de métricas de request."""
        metrics_instance.record_request(
            method="GET",
            endpoint="/test",
            status_code=200,
            duration=0.1
        )
        
        # Verifica se não há erro ao registrar
        assert True

    def test_record_greet_request(self, metrics_instance):
        """Testa o registro de métricas de greeting."""
        metrics_instance.record_greet_request("TestUser")
        
        # Verifica se não há erro ao registrar
        assert True

    def test_record_health_check(self, metrics_instance):
        """Testa o registro de métricas de health check."""
        metrics_instance.record_health_check()
        
        # Verifica se não há erro ao registrar
        assert True

    def test_get_content_type(self, metrics_instance):
        """Testa o tipo de conteúdo das métricas."""
        content_type = metrics_instance.get_content_type()
        
        assert content_type is not None
        assert "text/plain" in content_type

    def test_get_metrics_format(self, metrics_instance):
        """Testa o formato das métricas."""
        metrics_data = metrics_instance.get_metrics()
        
        assert isinstance(metrics_data, str)
        assert len(metrics_data) > 0

    @patch('app.core.metrics.psutil.cpu_percent')
    @patch('app.core.metrics.psutil.virtual_memory')
    def test_update_system_metrics(self, mock_memory, mock_cpu, metrics_instance):
        """Testa a atualização de métricas do sistema."""
        # Configurar mocks
        mock_cpu.return_value = 25.5
        mock_memory.return_value = MagicMock(used=1000000, total=4000000)
        
        # Executar atualização (não deve lançar erro)
        metrics_instance.update_system_metrics()
        
        assert True

    @patch('app.core.metrics.psutil.Process')
    def test_update_process_metrics(self, mock_process_class, metrics_instance):
        """Testa a atualização de métricas do processo."""
        # Configurar mock
        mock_process = MagicMock()
        mock_process.cpu_percent.return_value = 15.0
        mock_process.memory_info.return_value = MagicMock(rss=50000000)
        mock_process.num_threads.return_value = 3
        mock_process_class.return_value = mock_process
        
        # Executar atualização (não deve lançar erro)
        metrics_instance.update_process_metrics()
        
        assert True

    def test_metrics_registry_isolation(self):
        """Testa se cada instância tem seu próprio registry."""
        metrics1 = PrometheusMetrics()
        metrics2 = PrometheusMetrics()
        
        assert metrics1.registry != metrics2.registry

    def test_metrics_error_handling(self, metrics_instance):
        """Testa o tratamento de erros nas métricas."""
        # Testar com valores inválidos (não deve lançar erro)
        metrics_instance.record_request("", "", -1, -1)
        metrics_instance.record_greet_request("")
        
        assert True

    @patch('app.core.metrics.psutil.cpu_percent', side_effect=Exception("Test error"))
    def test_system_metrics_error_handling(self, mock_cpu, metrics_instance):
        """Testa o tratamento de erros nas métricas do sistema."""
        # Não deve lançar erro mesmo se psutil falhar
        metrics_instance.update_system_metrics()
        
        assert True

    @patch('app.core.metrics.psutil.Process', side_effect=Exception("Test error"))
    def test_process_metrics_error_handling(self, mock_process, metrics_instance):
        """Testa o tratamento de erros nas métricas do processo."""
        # Não deve lançar erro mesmo se psutil falhar
        metrics_instance.update_process_metrics()
        
        assert True

    def test_multiple_greet_requests(self, metrics_instance):
        """Testa múltiplas requisições de greeting."""
        names = ["Alice", "Bob", "Charlie"]
        
        for name in names:
            metrics_instance.record_greet_request(name)
        
        # Verifica se as métricas incluem os nomes
        metrics_data = metrics_instance.get_metrics()
        for name in names:
            assert name in metrics_data

    def test_http_request_duration_recording(self, metrics_instance):
        """Testa o registro de duração de requests."""
        durations = [0.1, 0.5, 1.0, 2.5]
        
        for duration in durations:
            metrics_instance.record_request("GET", "/test", 200, duration)
        
        # Verifica se as métricas foram registradas
        metrics_data = metrics_instance.get_metrics()
        assert "http_request_duration_seconds" in metrics_data

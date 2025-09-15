"""Prometheus metrics collector config."""

import time
import psutil
import platform
from typing import Dict, Any
from prometheus_client import Counter, Histogram, Gauge, Info, generate_latest, CONTENT_TYPE_LATEST
from prometheus_client.core import CollectorRegistry


class PrometheusMetrics:
    """Prometheus metrics collector config."""
    
    def __init__(self):
        """Constructor."""
        self.registry = CollectorRegistry()
        self._init_metrics()
        self._last_cpu_times = None
        self._last_cpu_check = time.time()
    
    def _init_metrics(self) -> None:
        """Init all Prometheus metrics."""
        # Métricas da aplicação
        self.http_requests_total = Counter(
            'http_requests_total',
            'HTTP requests total',
            ['method', 'endpoint', 'status'],
            registry=self.registry
        )
        
        self.http_request_duration_seconds = Histogram(
            'http_request_duration_seconds',
            'HTTP request duration in seconds',
            ['method', 'endpoint'],
            registry=self.registry
        )
        
        self.app_info = Info(
            'app_info',
            'App info',
            registry=self.registry
        )
        
        # Métricas do sistema
        self.system_cpu_usage = Gauge(
            'system_cpu_usage_percent',
            'System CPU usage percent',
            registry=self.registry
        )
        
        self.system_memory_usage = Gauge(
            'system_memory_usage_bytes',
            'System memory usage in bytes',
            registry=self.registry
        )
        
        self.system_memory_total = Gauge(
            'system_memory_total_bytes',
            'System memory total in bytes',
            registry=self.registry
        )
        
        self.system_disk_usage = Gauge(
            'system_disk_usage_bytes',
            'System disk usage in bytes',
            ['device'],
            registry=self.registry
        )
        
        self.system_disk_total = Gauge(
            'system_disk_total_bytes',
            'System disk total in bytes',
            ['device'],
            registry=self.registry
        )
        
        self.system_load_average = Gauge(
            'system_load_average',
            'System load average',
            ['period'],
            registry=self.registry
        )
        
        self.system_uptime = Gauge(
            'system_uptime_seconds',
            'System uptime in seconds',
            registry=self.registry
        )
        
        # Métricas do processo
        self.process_cpu_usage = Gauge(
            'process_cpu_usage_percent',
            'Process CPU usage percent',
            registry=self.registry
        )
        
        self.process_memory_usage = Gauge(
            'process_memory_usage_bytes',
            'Process memory usage in bytes',
            registry=self.registry
        )
        
        self.process_open_fds = Gauge(
            'process_open_file_descriptors',
            'Number of open file descriptors',
            registry=self.registry
        )
        
        self.process_threads = Gauge(
            'process_threads_total',
            'Number of threads total',
            registry=self.registry
        )
        
        # App metrics
        self.greet_requests_total = Counter(
            'greet_requests_total',
            'Total greeting requests',
            ['name'],
            registry=self.registry
        )
        
        self.health_checks_total = Counter(
            'health_checks_total',
            'Total health check requests',
            registry=self.registry
        )
    
    def set_app_info(self, app_name: str, version: str, environment: str) -> None:
        self.app_info.info({
            'name': app_name,
            'version': version,
            'environment': environment,
            'python_version': platform.python_version(),
            'platform': platform.platform(),
            'architecture': platform.machine(),
        })
    
    def update_system_metrics(self) -> None:
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=None)
            self.system_cpu_usage.set(cpu_percent)
            
            # Memory usage
            memory = psutil.virtual_memory()
            self.system_memory_usage.set(memory.used)
            self.system_memory_total.set(memory.total)
            
            # Disk usage
            for partition in psutil.disk_partitions():
                try:
                    disk_usage = psutil.disk_usage(partition.mountpoint)
                    device_name = partition.device.replace('/', '_').strip('_')
                    self.system_disk_usage.labels(device=device_name).set(disk_usage.used)
                    self.system_disk_total.labels(device=device_name).set(disk_usage.total)
                except (PermissionError, FileNotFoundError):
                    continue
            
            # Load average (only Unix systems)
            try:
                load_avg = psutil.getloadavg()
                self.system_load_average.labels(period='1m').set(load_avg[0])
                self.system_load_average.labels(period='5m').set(load_avg[1])
                self.system_load_average.labels(period='15m').set(load_avg[2])
            except AttributeError:
                # getloadavg is not available at Windows
                pass
            
            # System uptime
            boot_time = psutil.boot_time()
            uptime = time.time() - boot_time
            self.system_uptime.set(uptime)
            
        except Exception:
            # Handle psutil errors gracefully
            pass
    
    def update_process_metrics(self) -> None:
        try:
            process = psutil.Process()
            
            # CPU usage
            cpu_percent = process.cpu_percent()
            self.process_cpu_usage.set(cpu_percent)
            
            # Memory usage
            memory_info = process.memory_info()
            self.process_memory_usage.set(memory_info.rss)
            
            # Open file descriptors
            try:
                num_fds = process.num_fds()
                self.process_open_fds.set(num_fds)
            except AttributeError:
                # num_fds is not available at Windows
                pass
            
            # Número de threads
            num_threads = process.num_threads()
            self.process_threads.set(num_threads)
            
        except Exception:
            # Handle psutil errors gracefully
            pass
    
    def record_request(self, method: str, endpoint: str, status_code: int, duration: float) -> None:
        """Record HTTP request metrics."""
        self.http_requests_total.labels(
            method=method,
            endpoint=endpoint,
            status=str(status_code)
        ).inc()
        
        self.http_request_duration_seconds.labels(
            method=method,
            endpoint=endpoint
        ).observe(duration)
    
    def record_greet_request(self, name: str) -> None:
        """Record greeting request metrics."""
        self.greet_requests_total.labels(name=name).inc()
    
    def record_health_check(self) -> None:
        """Record health check request metrics."""
        self.health_checks_total.inc()
    
    def get_metrics(self) -> str:
        """Get all metrics in Prometheus format."""
        # Update system and process metrics before generating output
        self.update_system_metrics()
        self.update_process_metrics()
        
        return generate_latest(self.registry).decode('utf-8')
    
    def get_content_type(self) -> str:
        """Get the content type of the metrics in Prometheus format."""
        return CONTENT_TYPE_LATEST


metrics = PrometheusMetrics()

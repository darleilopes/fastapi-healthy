"""App configuration."""

from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """App config and settings."""
    
    # App
    app_name: str = Field(default="FastAPI Healthy", description="App name")
    app_version: str = Field(default="1.0.0", description="App version")
    debug: bool = Field(default=False, description="Debug mode")
    
    # Server
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8000, description="Server port")
    
    # Path
    api_v1_prefix: str = Field(default="/api/v1", description="API v1 prefix")    
    metrics_path: str = Field(default="/metrics", description="Prometheus metrics path")
    health_path: str = Field(default="/healthz", description="Health check path")

    # Others
    default_greeting_name: str = Field(default="you!!", description="Standard greeting name to use when no name is provided")
    environment: str = Field(default="development", description="Env name")
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

settings = Settings()

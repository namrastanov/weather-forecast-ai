"""Centralized configuration management."""

from pydantic_settings import BaseSettings
from pydantic import Field, field_validator
from typing import Optional
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    app_name: str = "weather-forecast-ai"
    environment: str = Field(default="development")
    debug: bool = False
    
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_key: Optional[str] = None
    
    database_url: str = Field(default="sqlite:///./weather.db")
    redis_url: str = Field(default="redis://localhost:6379/0")
    
    model_path: str = "./models"
    cache_ttl: int = 3600
    max_forecast_days: int = 14
    
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    @field_validator("environment")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        """Validate environment value."""
        allowed = {"development", "staging", "production"}
        if v.lower() not in allowed:
            raise ValueError(f"Environment must be one of: {allowed}")
        return v.lower()

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level."""
        allowed = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if v.upper() not in allowed:
            raise ValueError(f"Log level must be one of: {allowed}")
        return v.upper()

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False
    }


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()

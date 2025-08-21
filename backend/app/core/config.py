"""
FastAPI Application Configuration

Extends the existing configuration system with FastAPI-specific settings.
"""

from typing import List, Optional
from pydantic import Field

from backend.config import Settings as BaseSettings, get_settings as get_base_settings


class FastAPISettings(BaseSettings):
    """
    FastAPI-specific configuration extending the base settings
    """
    
    # FastAPI application settings
    VERSION: str = Field(default="1.0.0", description="Application version")
    HOST: str = Field(default="0.0.0.0", description="Server host")
    PORT: int = Field(default=8000, description="Server port")
    RELOAD: bool = Field(default=True, description="Enable auto-reload")
    
    # API settings
    API_PREFIX: str = Field(default="/api", description="API prefix path")
    TITLE: str = Field(default="Top 5 Sharpe Ratio Stock API", description="API title")
    DESCRIPTION: str = Field(default="API for analyzing top performing stocks by Sharpe ratio", description="API description")
    
    # CORS settings
    ALLOWED_HOSTS: List[str] = Field(
        default=["*"], 
        description="Allowed CORS hosts"
    )
    ALLOWED_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:8000"],
        description="Allowed CORS origins"
    )
    ALLOWED_METHODS: List[str] = Field(
        default=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        description="Allowed HTTP methods"
    )
    ALLOWED_HEADERS: List[str] = Field(
        default=["*"],
        description="Allowed headers"
    )
    
    # Additional API configuration
    DOCS_URL: Optional[str] = Field(default="/docs", description="Swagger UI URL")
    REDOC_URL: Optional[str] = Field(default="/redoc", description="ReDoc URL")
    OPENAPI_URL: Optional[str] = Field(default="/openapi.json", description="OpenAPI JSON URL")
    
    class Config(BaseSettings.Config):
        env_prefix = "STOCK_"


class FastAPIDevelopmentSettings(FastAPISettings):
    """Development-specific FastAPI settings"""
    RELOAD: bool = True
    DOCS_URL: Optional[str] = "/docs"
    REDOC_URL: Optional[str] = "/redoc"
    OPENAPI_URL: Optional[str] = "/openapi.json"


class FastAPIProductionSettings(FastAPISettings):
    """Production-specific FastAPI settings"""
    RELOAD: bool = False
    DOCS_URL: Optional[str] = None  # Disable docs in production
    REDOC_URL: Optional[str] = None
    ALLOWED_HOSTS: List[str] = Field(default_factory=lambda: ["your-domain.com"])
    ALLOWED_ORIGINS: List[str] = Field(default_factory=lambda: ["https://your-domain.com"])


def get_settings() -> FastAPISettings:
    """
    Get FastAPI settings instance based on environment
    
    Returns:
        Configured FastAPI settings instance
    """
    base_settings = get_base_settings()
    
    if base_settings.is_production():
        return FastAPIProductionSettings()
    else:
        return FastAPIDevelopmentSettings()


# Global settings instance
settings = get_settings()
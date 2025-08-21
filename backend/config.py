"""
Configuration Management

Central configuration management for the stock data service with support for
environment variables, validation, and different deployment environments.

Features:
- Environment-based configuration
- Configuration validation with Pydantic
- Support for development, testing, and production environments
- Logging configuration
- Cache and API settings
"""

import logging
import os
from enum import Enum
from pathlib import Path
from typing import Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class Environment(str, Enum):
    """Deployment environment types"""
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"


class LogLevel(str, Enum):
    """Logging levels"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class Settings(BaseSettings):
    """
    Application settings with environment variable support
    
    All settings can be overridden via environment variables with the prefix 'STOCK_'
    For example: STOCK_ENVIRONMENT=production
    """
    
    # Application settings
    environment: Environment = Field(default=Environment.DEVELOPMENT, description="Deployment environment")
    debug: bool = Field(default=True, description="Enable debug mode")
    log_level: LogLevel = Field(default=LogLevel.INFO, description="Logging level")
    
    # Data service settings
    cache_dir: str = Field(default="data/cache", description="Cache directory path")
    default_ttl_hours: int = Field(default=24, description="Default cache TTL in hours")
    enable_cache: bool = Field(default=True, description="Enable data caching")
    
    # API and retry settings
    max_retries: int = Field(default=5, description="Maximum API retry attempts")
    request_timeout: int = Field(default=30, description="API request timeout in seconds")
    max_concurrent_requests: int = Field(default=10, description="Maximum concurrent API requests")
    
    # Data validation settings
    min_data_points: int = Field(default=252, description="Minimum data points required")
    min_data_years: float = Field(default=3.0, description="Minimum years of data required")
    
    # S&P 500 settings
    sp500_csv_path: Optional[str] = Field(default=None, description="Custom S&P 500 CSV path")
    validate_sp500_count: bool = Field(default=True, description="Validate S&P 500 stock count")
    
    # Performance settings
    batch_size: int = Field(default=50, description="Batch size for processing tickers")
    max_memory_usage_mb: int = Field(default=1024, description="Maximum memory usage in MB")
    
    # Monitoring and health
    enable_metrics: bool = Field(default=True, description="Enable performance metrics collection")
    health_check_interval: int = Field(default=300, description="Health check interval in seconds")
    
    # Security settings
    rate_limit_enabled: bool = Field(default=True, description="Enable API rate limiting")
    rate_limit_calls_per_minute: int = Field(default=300, description="API calls per minute limit")
    
    class Config:
        env_prefix = "STOCK_"
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
    
    @field_validator('cache_dir')
    def validate_cache_dir(cls, v):
        """Create cache directory if it doesn't exist"""
        if v:
            cache_path = Path(v)
            cache_path.mkdir(parents=True, exist_ok=True)
            # Verify we can write to the directory
            test_file = cache_path / ".test_write"
            try:
                test_file.touch()
                test_file.unlink()
            except OSError as e:
                raise ValueError(f"Cannot write to cache directory {v}: {e}")
        return v
    
    @field_validator('default_ttl_hours')
    def validate_ttl(cls, v):
        """Validate TTL is reasonable"""
        if v <= 0:
            raise ValueError("TTL must be positive")
        if v > 168:  # 1 week
            raise ValueError("TTL cannot exceed 168 hours (1 week)")
        return v
    
    @field_validator('max_retries')
    def validate_max_retries(cls, v):
        """Validate retry count is reasonable"""
        if v < 0:
            raise ValueError("Max retries cannot be negative")
        if v > 10:
            raise ValueError("Max retries should not exceed 10")
        return v
    
    @field_validator('min_data_years')
    def validate_min_data_years(cls, v):
        """Validate minimum data years is reasonable"""
        if v <= 0:
            raise ValueError("Minimum data years must be positive")
        if v > 10:
            raise ValueError("Minimum data years should not exceed 10")
        return v
    
    @field_validator('batch_size')
    def validate_batch_size(cls, v):
        """Validate batch size is reasonable"""
        if v <= 0:
            raise ValueError("Batch size must be positive")
        if v > 500:
            raise ValueError("Batch size should not exceed 500")
        return v
    
    @field_validator('sp500_csv_path')
    def validate_sp500_csv_path(cls, v):
        """Validate S&P 500 CSV path if provided"""
        if v and not Path(v).exists():
            raise ValueError(f"S&P 500 CSV file not found: {v}")
        return v
    
    def is_development(self) -> bool:
        """Check if running in development environment"""
        return self.environment == Environment.DEVELOPMENT
    
    def is_testing(self) -> bool:
        """Check if running in testing environment"""
        return self.environment == Environment.TESTING
    
    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.environment == Environment.PRODUCTION
    
    def get_log_level(self) -> int:
        """Get numeric log level for Python logging"""
        return getattr(logging, self.log_level.value)
    
    def configure_logging(self):
        """Configure application logging based on settings"""
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        
        if self.is_development():
            # More detailed logging for development
            log_format = "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
        
        logging.basicConfig(
            level=self.get_log_level(),
            format=log_format,
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
        # Set specific logger levels
        if not self.is_development():
            # Reduce noise in production
            logging.getLogger("urllib3").setLevel(logging.WARNING)
            logging.getLogger("requests").setLevel(logging.WARNING)
            logging.getLogger("yfinance").setLevel(logging.WARNING)
        
        logger = logging.getLogger(__name__)
        logger.info(f"Logging configured for {self.environment} environment at {self.log_level} level")


class DevelopmentSettings(Settings):
    """Development environment specific settings"""
    
    environment: Environment = Environment.DEVELOPMENT
    debug: bool = True
    log_level: LogLevel = LogLevel.DEBUG
    default_ttl_hours: int = 1  # Shorter cache for development
    max_retries: int = 3  # Fewer retries for faster development
    enable_metrics: bool = True


class TestingSettings(Settings):
    """Testing environment specific settings"""
    
    environment: Environment = Environment.TESTING
    debug: bool = True
    log_level: LogLevel = LogLevel.WARNING
    enable_cache: bool = False  # Disable cache for testing
    max_retries: int = 1  # Minimal retries for faster tests
    validate_sp500_count: bool = False  # Allow smaller test datasets
    enable_metrics: bool = False


class ProductionSettings(Settings):
    """Production environment specific settings"""
    
    environment: Environment = Environment.PRODUCTION
    debug: bool = False
    log_level: LogLevel = LogLevel.INFO
    default_ttl_hours: int = 24  # Standard cache duration
    max_retries: int = 5  # Full retry logic
    enable_metrics: bool = True
    rate_limit_enabled: bool = True


def get_settings() -> Settings:
    """
    Get settings instance based on environment
    
    Returns:
        Configured settings instance for the current environment
    """
    env = os.getenv("STOCK_ENVIRONMENT", "development").lower()
    
    if env == "testing":
        settings = TestingSettings()
    elif env == "production":
        settings = ProductionSettings()
    else:
        settings = DevelopmentSettings()
    
    # Configure logging
    settings.configure_logging()
    
    return settings


def create_env_file(output_path: str = ".env.sample"):
    """
    Create a sample environment file with all available settings
    
    Args:
        output_path: Path to create the sample env file
    """
    sample_content = """# Stock Data Service Configuration
# Copy this file to .env and customize for your environment

# Application Environment
STOCK_ENVIRONMENT=development
STOCK_DEBUG=true
STOCK_LOG_LEVEL=INFO

# Data Service Settings
STOCK_CACHE_DIR=data/cache
STOCK_DEFAULT_TTL_HOURS=24
STOCK_ENABLE_CACHE=true

# API and Retry Settings
STOCK_MAX_RETRIES=5
STOCK_REQUEST_TIMEOUT=30
STOCK_MAX_CONCURRENT_REQUESTS=10

# Data Validation Settings
STOCK_MIN_DATA_POINTS=252
STOCK_MIN_DATA_YEARS=3.0

# S&P 500 Settings
STOCK_SP500_CSV_PATH=data/sp500.csv
STOCK_VALIDATE_SP500_COUNT=true

# Performance Settings
STOCK_BATCH_SIZE=50
STOCK_MAX_MEMORY_USAGE_MB=1024

# Monitoring and Health
STOCK_ENABLE_METRICS=true
STOCK_HEALTH_CHECK_INTERVAL=300

# Security Settings
STOCK_RATE_LIMIT_ENABLED=true
STOCK_RATE_LIMIT_CALLS_PER_MINUTE=300
"""
    
    with open(output_path, 'w') as f:
        f.write(sample_content)
    
    print(f"Sample environment file created at {output_path}")


# Global settings instance
settings = get_settings()


# Export commonly used settings
__all__ = [
    'Settings',
    'DevelopmentSettings', 
    'TestingSettings',
    'ProductionSettings',
    'Environment',
    'LogLevel',
    'get_settings',
    'create_env_file',
    'settings'
]
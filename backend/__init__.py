"""
Stock Data Backend Package

This package provides a robust data fetching and caching layer for stock market data,
specifically designed for S&P 500 Sharpe ratio analysis.

Key Components:
- YFinanceAdapter: Low-level Yahoo Finance API wrapper with retry logic
- DataService: High-level service layer with business logic and validation
- Configuration: Environment-based configuration management

Features:
- Exponential backoff retry logic with jitter
- On-disk Parquet caching with TTL support
- Comprehensive data quality validation
- S&P 500 universe integration
- Health monitoring and statistics
- Production-ready error handling and logging
"""

from .config import settings, get_settings, Environment, LogLevel
from .data_service import DataService, DataServiceConfig, StockDataResult, DataQualityResult
from .yfinance_adapter import YFinanceAdapter, YFinanceAdapterError, CacheManager

__version__ = "1.0.0"

__all__ = [
    # Main classes
    'DataService',
    'YFinanceAdapter',
    'CacheManager',
    
    # Configuration
    'settings',
    'get_settings',
    'Environment',
    'LogLevel',
    
    # Data models
    'DataServiceConfig',
    'StockDataResult', 
    'DataQualityResult',
    
    # Exceptions
    'YFinanceAdapterError'
]
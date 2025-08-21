"""
Backend package for Top 5 Sharpe Ratio application

This package provides a comprehensive backend for S&P 500 Sharpe ratio analysis,
combining robust data fetching capabilities with financial calculation utilities.

Key Components:
- YFinanceAdapter: Low-level Yahoo Finance API wrapper with retry logic
- DataService: High-level service layer with business logic and validation
- Configuration: Environment-based configuration management
- Sharpe Utilities: Core financial calculation functions

Features:
- Exponential backoff retry logic with jitter
- On-disk Parquet caching with TTL support
- Comprehensive data quality validation
- S&P 500 universe integration
- Health monitoring and statistics
- Production-ready error handling and logging
- Complete Sharpe ratio calculation suite
"""

# Data fetching and management
from .config import settings, get_settings, Environment, LogLevel
from .data_service import DataService, DataServiceConfig, StockDataResult, DataQualityResult
from .yfinance_adapter import YFinanceAdapter, YFinanceAdapterError, CacheManager

# Sharpe ratio calculations
from .sharpe_utils import (
    calculate_daily_returns,
    calculate_sharpe_ratio,
    has_sufficient_data,
    validate_risk_free_rate,
    batch_calculate_sharpe_ratios,
    sharpe_from_returns,
    SharpeCalculationError
)

__version__ = "1.0.0"

__all__ = [
    # Data management classes
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
    
    # Sharpe ratio utilities
    'calculate_daily_returns',
    'calculate_sharpe_ratio', 
    'has_sufficient_data',
    'validate_risk_free_rate',
    'batch_calculate_sharpe_ratios',
    'sharpe_from_returns',
    
    # Exceptions
    'YFinanceAdapterError',
    'SharpeCalculationError'
]
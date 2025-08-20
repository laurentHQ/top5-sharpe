"""
Backend package for Top 5 Sharpe Ratio application

This package contains the core financial calculation utilities and will house
the FastAPI application and related backend services.
"""

from .sharpe_utils import (
    calculate_daily_returns,
    calculate_sharpe_ratio,
    has_sufficient_data,
    validate_risk_free_rate,
    batch_calculate_sharpe_ratios,
    sharpe_from_returns,
    SharpeCalculationError
)

__all__ = [
    'calculate_daily_returns',
    'calculate_sharpe_ratio', 
    'has_sufficient_data',
    'validate_risk_free_rate',
    'batch_calculate_sharpe_ratios',
    'sharpe_from_returns',
    'SharpeCalculationError'
]
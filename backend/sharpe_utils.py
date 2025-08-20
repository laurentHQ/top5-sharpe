"""
Sharpe Ratio Calculation Engine

This module provides pure functions for calculating Sharpe ratios from stock price data.
The implementation handles edge cases like missing data, insufficient history, and 
provides configurable risk-free rate parameters.

Mathematical Foundation:
- Daily log returns: r_t = ln(P_t / P_{t-1})
- Annualized Sharpe ratio: (mean_daily_return - daily_rf_rate) / std_daily_return * sqrt(252)
- Risk-free rate conversion: annual_rf -> daily_rf = annual_rf / 252

Key Features:
- Robust NaN handling for missing price data
- Configurable risk-free rate with validation
- Partial data flagging for insufficient history (< 3 years)
- Pure functions with no side effects
- Comprehensive input validation
"""

import numpy as np
import pandas as pd
from typing import Union, Tuple, Optional
import warnings


class SharpeCalculationError(Exception):
    """Custom exception for Sharpe ratio calculation errors"""
    pass


def calculate_daily_returns(prices: Union[pd.Series, np.ndarray], 
                          method: str = 'log') -> np.ndarray:
    """
    Calculate daily returns from price series using log returns method.
    
    Log returns are preferred for financial analysis as they:
    - Are time-additive (can sum across periods)
    - Better handle compounding effects
    - Are more symmetric around zero
    
    Args:
        prices: Series of daily closing prices (pandas Series or numpy array)
        method: Return calculation method, currently only 'log' supported
        
    Returns:
        numpy array of daily log returns (length = len(prices) - 1)
        
    Raises:
        SharpeCalculationError: If prices are invalid or method unsupported
        
    Example:
        >>> prices = pd.Series([100, 101, 99, 102])
        >>> returns = calculate_daily_returns(prices)
        >>> len(returns) == len(prices) - 1
        True
    """
    if method != 'log':
        raise SharpeCalculationError(f"Unsupported return method: {method}")
    
    # Convert to numpy array for consistent handling
    if isinstance(prices, pd.Series):
        price_array = prices.values
    else:
        price_array = np.asarray(prices)
    
    # Validate input
    if len(price_array) < 2:
        raise SharpeCalculationError("At least 2 price points required for return calculation")
    
    # Check for non-positive prices which would cause log return issues
    if np.any(price_array <= 0):
        raise SharpeCalculationError("All prices must be positive for log return calculation")
    
    # Calculate log returns: ln(P_t / P_{t-1})
    # Handle NaN values by preserving them in the output
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)  # Suppress log(0) warnings
        log_returns = np.log(price_array[1:] / price_array[:-1])
    
    return log_returns


def has_sufficient_data(prices: Union[pd.Series, np.ndarray], 
                       min_years: float = 3.0,
                       trading_days_per_year: int = 252) -> bool:
    """
    Check if price series has sufficient data for reliable Sharpe ratio calculation.
    
    Args:
        prices: Series of daily closing prices
        min_years: Minimum years of data required (default: 3.0)
        trading_days_per_year: Trading days per year for conversion (default: 252)
        
    Returns:
        True if sufficient data available, False otherwise
        
    Example:
        >>> prices = pd.Series(np.random.randn(1000))  # ~4 years of data
        >>> has_sufficient_data(prices)
        True
        >>> short_prices = pd.Series(np.random.randn(500))  # ~2 years
        >>> has_sufficient_data(short_prices)
        False
    """
    if isinstance(prices, pd.Series):
        valid_prices = prices.dropna()
    else:
        price_array = np.asarray(prices)
        valid_prices = price_array[~np.isnan(price_array)]
    
    min_observations = int(min_years * trading_days_per_year)
    return len(valid_prices) >= min_observations


def calculate_sharpe_ratio(prices: Union[pd.Series, np.ndarray],
                          risk_free_rate: float = 0.015,
                          min_years: float = 3.0,
                          trading_days_per_year: int = 252) -> Tuple[float, bool]:
    """
    Calculate annualized Sharpe ratio from daily price series.
    
    The Sharpe ratio measures risk-adjusted returns by comparing excess returns
    (above risk-free rate) to volatility. Higher values indicate better 
    risk-adjusted performance.
    
    Formula: 
    - Daily returns: r_t = ln(P_t / P_{t-1})
    - Daily risk-free rate: rf_daily = annual_rf / 252
    - Daily excess returns: excess_t = r_t - rf_daily
    - Annualized Sharpe: mean(excess_daily) / std(r_daily) * sqrt(252)
    
    Args:
        prices: Series of daily closing prices
        risk_free_rate: Annual risk-free rate (default: 1.5%)
        min_years: Minimum years of data for full calculation (default: 3.0)
        trading_days_per_year: Trading days per year (default: 252)
        
    Returns:
        Tuple of (sharpe_ratio, is_partial_data)
        - sharpe_ratio: Annualized Sharpe ratio (float, may be NaN)
        - is_partial_data: True if less than min_years of data
        
    Raises:
        SharpeCalculationError: If calculation cannot be performed
        
    Example:
        >>> np.random.seed(42)
        >>> prices = pd.Series(100 * np.exp(np.cumsum(np.random.randn(1000) * 0.01)))
        >>> sharpe, partial = calculate_sharpe_ratio(prices)
        >>> isinstance(sharpe, float)
        True
        >>> isinstance(partial, bool)  
        True
    """
    # Validate risk-free rate
    if not (0 <= risk_free_rate <= 0.3):
        raise SharpeCalculationError(f"Risk-free rate {risk_free_rate} outside valid range [0, 0.3]")
    
    # Check data sufficiency
    is_partial_data = not has_sufficient_data(prices, min_years, trading_days_per_year)
    
    try:
        # Calculate daily returns
        daily_returns = calculate_daily_returns(prices)
        
        # Remove NaN returns for calculation
        valid_returns = daily_returns[~np.isnan(daily_returns)]
        
        if len(valid_returns) == 0:
            return np.nan, is_partial_data
        
        # Convert annual risk-free rate to daily
        daily_rf_rate = risk_free_rate / trading_days_per_year
        
        # Calculate excess returns
        excess_returns = valid_returns - daily_rf_rate
        
        # Calculate Sharpe ratio components
        mean_excess_return = np.mean(excess_returns)
        return_volatility = np.std(valid_returns, ddof=1)  # Use sample std (n-1)
        
        # Handle zero volatility case
        if return_volatility == 0:
            # If all returns are identical, Sharpe is undefined (or infinite if excess > 0)
            if mean_excess_return > 0:
                return np.inf, is_partial_data
            elif mean_excess_return < 0:
                return -np.inf, is_partial_data
            else:
                return np.nan, is_partial_data
        
        # Calculate annualized Sharpe ratio
        annualization_factor = np.sqrt(trading_days_per_year)
        sharpe_ratio = (mean_excess_return / return_volatility) * annualization_factor
        
        return sharpe_ratio, is_partial_data
        
    except SharpeCalculationError:
        # Re-raise our custom exceptions
        raise
    except Exception as e:
        # Wrap unexpected errors
        raise SharpeCalculationError(f"Sharpe calculation failed: {str(e)}")


def validate_risk_free_rate(risk_free_rate: float) -> None:
    """
    Validate risk-free rate parameter.
    
    Args:
        risk_free_rate: Annual risk-free rate to validate
        
    Raises:
        SharpeCalculationError: If rate is outside valid range [0, 0.3]
        
    Example:
        >>> validate_risk_free_rate(0.015)  # 1.5% - valid
        >>> validate_risk_free_rate(-0.01)  # Raises error
        Traceback (most recent call last):
        ...
        SharpeCalculationError: Risk-free rate -0.01 outside valid range [0, 0.3]
    """
    if not isinstance(risk_free_rate, (int, float)):
        raise SharpeCalculationError(f"Risk-free rate must be numeric, got {type(risk_free_rate)}")
    
    if not (0 <= risk_free_rate <= 0.3):
        raise SharpeCalculationError(f"Risk-free rate {risk_free_rate} outside valid range [0, 0.3]")


def batch_calculate_sharpe_ratios(price_data: dict,
                                risk_free_rate: float = 0.015,
                                min_years: float = 3.0) -> dict:
    """
    Calculate Sharpe ratios for multiple stocks in batch.
    
    Args:
        price_data: Dictionary mapping tickers to price series
        risk_free_rate: Annual risk-free rate (default: 1.5%)
        min_years: Minimum years of data for full calculation
        
    Returns:
        Dictionary mapping tickers to (sharpe_ratio, is_partial_data) tuples
        
    Example:
        >>> np.random.seed(42)
        >>> data = {
        ...     'AAPL': pd.Series(100 * np.exp(np.cumsum(np.random.randn(1000) * 0.01))),
        ...     'MSFT': pd.Series(100 * np.exp(np.cumsum(np.random.randn(500) * 0.01)))
        ... }
        >>> results = batch_calculate_sharpe_ratios(data)
        >>> len(results) == 2
        True
        >>> all(isinstance(v, tuple) and len(v) == 2 for v in results.values())
        True
    """
    # Validate risk-free rate once for all calculations
    validate_risk_free_rate(risk_free_rate)
    
    results = {}
    
    for ticker, prices in price_data.items():
        try:
            sharpe_ratio, is_partial = calculate_sharpe_ratio(
                prices, risk_free_rate, min_years
            )
            results[ticker] = (sharpe_ratio, is_partial)
        except SharpeCalculationError:
            # Store failed calculations as NaN with partial flag
            results[ticker] = (np.nan, True)
    
    return results


# Convenience functions for common use cases
def sharpe_from_returns(returns: Union[pd.Series, np.ndarray],
                       risk_free_rate: float = 0.015,
                       trading_days_per_year: int = 252) -> float:
    """
    Calculate Sharpe ratio directly from return series (not prices).
    
    Args:
        returns: Series of daily returns (not prices!)
        risk_free_rate: Annual risk-free rate
        trading_days_per_year: Trading days per year for annualization
        
    Returns:
        Annualized Sharpe ratio
    """
    validate_risk_free_rate(risk_free_rate)
    
    if isinstance(returns, pd.Series):
        valid_returns = returns.dropna().values
    else:
        return_array = np.asarray(returns)
        valid_returns = return_array[~np.isnan(return_array)]
    
    if len(valid_returns) == 0:
        return np.nan
    
    daily_rf_rate = risk_free_rate / trading_days_per_year
    excess_returns = valid_returns - daily_rf_rate
    
    mean_excess = np.mean(excess_returns)
    vol_returns = np.std(valid_returns, ddof=1)
    
    if vol_returns == 0:
        return np.inf if mean_excess > 0 else (-np.inf if mean_excess < 0 else np.nan)
    
    return (mean_excess / vol_returns) * np.sqrt(trading_days_per_year)
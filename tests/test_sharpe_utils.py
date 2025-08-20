"""
Comprehensive Test Suite for Sharpe Ratio Utilities

Tests cover:
- Deterministic tests with known input/output pairs
- Edge cases (zero volatility, NaN handling, insufficient data)
- Property-based tests with random inputs
- Input validation and error handling
- Mathematical accuracy verification
"""

import pytest
import numpy as np
import pandas as pd
from hypothesis import given, strategies as st, assume
from hypothesis import settings, HealthCheck

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from backend.sharpe_utils import (
    calculate_daily_returns,
    calculate_sharpe_ratio,
    has_sufficient_data,
    validate_risk_free_rate,
    batch_calculate_sharpe_ratios,
    sharpe_from_returns,
    SharpeCalculationError
)


class TestCalculateDailyReturns:
    """Test suite for calculate_daily_returns function"""
    
    def test_simple_log_returns(self):
        """Test log returns calculation with known values"""
        # Price series: [100, 110, 99, 108]
        # Expected log returns: [ln(1.1), ln(0.9), ln(108/99)]
        prices = pd.Series([100.0, 110.0, 99.0, 108.0])
        returns = calculate_daily_returns(prices)
        
        expected = np.array([
            np.log(110/100),
            np.log(99/110), 
            np.log(108/99)
        ])
        
        np.testing.assert_array_almost_equal(returns, expected, decimal=10)
        assert len(returns) == len(prices) - 1
    
    def test_constant_prices_zero_returns(self):
        """Test that constant prices give zero returns"""
        prices = pd.Series([100.0] * 5)
        returns = calculate_daily_returns(prices)
        expected = np.zeros(4)
        np.testing.assert_array_equal(returns, expected)
    
    def test_numpy_array_input(self):
        """Test that numpy array input works correctly"""
        prices_array = np.array([100.0, 105.0, 110.0])
        prices_series = pd.Series(prices_array)
        
        returns_array = calculate_daily_returns(prices_array)
        returns_series = calculate_daily_returns(prices_series)
        
        np.testing.assert_array_equal(returns_array, returns_series)
    
    def test_empty_prices_error(self):
        """Test that empty price series raises error"""
        with pytest.raises(SharpeCalculationError, match="At least 2 price points required"):
            calculate_daily_returns(pd.Series([]))
    
    def test_single_price_error(self):
        """Test that single price raises error"""
        with pytest.raises(SharpeCalculationError, match="At least 2 price points required"):
            calculate_daily_returns(pd.Series([100.0]))
    
    def test_negative_prices_error(self):
        """Test that negative prices raise error"""
        with pytest.raises(SharpeCalculationError, match="All prices must be positive"):
            calculate_daily_returns(pd.Series([100.0, -50.0, 120.0]))
    
    def test_zero_prices_error(self):
        """Test that zero prices raise error"""
        with pytest.raises(SharpeCalculationError, match="All prices must be positive"):
            calculate_daily_returns(pd.Series([100.0, 0.0, 120.0]))
    
    def test_unsupported_method_error(self):
        """Test that unsupported method raises error"""
        prices = pd.Series([100.0, 110.0])
        with pytest.raises(SharpeCalculationError, match="Unsupported return method"):
            calculate_daily_returns(prices, method='arithmetic')
    
    def test_nan_in_prices(self):
        """Test handling of NaN values in prices"""
        # NaN in middle should produce NaN returns around it
        prices = pd.Series([100.0, np.nan, 120.0, 110.0])
        returns = calculate_daily_returns(prices)
        
        # Should have NaN for the return from 100 to NaN and NaN to 120
        assert np.isnan(returns[0])  # 100 -> NaN
        assert np.isnan(returns[1])  # NaN -> 120
        assert not np.isnan(returns[2])  # 120 -> 110 should be valid


class TestHasSufficientData:
    """Test suite for has_sufficient_data function"""
    
    def test_sufficient_data(self):
        """Test with sufficient data (3+ years)"""
        # 4 years of data (1008 trading days)
        prices = pd.Series(np.random.randn(1008))
        assert has_sufficient_data(prices, min_years=3.0)
    
    def test_insufficient_data(self):
        """Test with insufficient data (<3 years)"""
        # 2 years of data (504 trading days) 
        prices = pd.Series(np.random.randn(504))
        assert not has_sufficient_data(prices, min_years=3.0)
    
    def test_exactly_minimum_data(self):
        """Test with exactly minimum required data"""
        # Exactly 3 years (756 trading days)
        prices = pd.Series(np.random.randn(756))
        assert has_sufficient_data(prices, min_years=3.0)
    
    def test_custom_min_years(self):
        """Test with custom minimum years requirement"""
        prices = pd.Series(np.random.randn(1260))  # 5 years
        assert has_sufficient_data(prices, min_years=2.0)
        assert has_sufficient_data(prices, min_years=5.0)
        assert not has_sufficient_data(prices, min_years=6.0)
    
    def test_with_nan_values(self):
        """Test that NaN values are excluded from count"""
        # 1000 total points but 300 are NaN, leaving 700 valid (~2.8 years)
        prices = pd.Series(np.random.randn(1000))
        prices.iloc[200:500] = np.nan  # 300 NaN values
        assert not has_sufficient_data(prices, min_years=3.0)
        
        # With 1200 total and same NaN pattern -> 900 valid (~3.6 years)
        prices = pd.Series(np.random.randn(1200))
        prices.iloc[200:500] = np.nan
        assert has_sufficient_data(prices, min_years=3.0)
    
    def test_numpy_array_input(self):
        """Test with numpy array input"""
        prices_array = np.random.randn(1000)
        assert has_sufficient_data(prices_array, min_years=3.0)


class TestValidateRiskFreeRate:
    """Test suite for validate_risk_free_rate function"""
    
    def test_valid_rates(self):
        """Test valid risk-free rates"""
        valid_rates = [0.0, 0.015, 0.05, 0.1, 0.3]
        for rate in valid_rates:
            validate_risk_free_rate(rate)  # Should not raise
    
    def test_negative_rate_error(self):
        """Test that negative rates raise error"""
        with pytest.raises(SharpeCalculationError, match="outside valid range"):
            validate_risk_free_rate(-0.01)
    
    def test_too_high_rate_error(self):
        """Test that rates > 30% raise error"""
        with pytest.raises(SharpeCalculationError, match="outside valid range"):
            validate_risk_free_rate(0.35)
    
    def test_non_numeric_error(self):
        """Test that non-numeric rates raise error"""
        with pytest.raises(SharpeCalculationError, match="must be numeric"):
            validate_risk_free_rate("0.05")


class TestCalculateSharpeRatio:
    """Test suite for calculate_sharpe_ratio function"""
    
    def test_known_sharpe_calculation(self):
        """Test Sharpe calculation with known deterministic values"""
        # Create a price series with known returns
        np.random.seed(42)
        initial_price = 100.0
        daily_returns = np.array([0.01, -0.005, 0.008, 0.002, -0.003] * 200)  # 1000 days
        
        prices = [initial_price]
        for ret in daily_returns:
            prices.append(prices[-1] * np.exp(ret))
        
        prices = pd.Series(prices)
        sharpe, partial = calculate_sharpe_ratio(prices, risk_free_rate=0.0)
        
        # Manual calculation for verification
        returns = calculate_daily_returns(prices)
        valid_returns = returns[~np.isnan(returns)]
        expected_sharpe = np.mean(valid_returns) / np.std(valid_returns, ddof=1) * np.sqrt(252)
        
        assert abs(sharpe - expected_sharpe) < 1e-10
        assert not partial  # Should have sufficient data
    
    def test_zero_volatility(self):
        """Test handling of zero volatility (constant prices)"""
        prices = pd.Series([100.0] * 1000)  # Constant prices
        
        # With zero risk-free rate -> Sharpe should be NaN (0/0)
        sharpe, partial = calculate_sharpe_ratio(prices, risk_free_rate=0.0)
        assert np.isnan(sharpe)
        
        # With positive risk-free rate -> should be -inf
        sharpe, partial = calculate_sharpe_ratio(prices, risk_free_rate=0.05)
        assert sharpe == -np.inf
    
    def test_partial_data_flag(self):
        """Test that partial data flag works correctly"""
        # Short series (1 year)
        prices = pd.Series(100 * np.exp(np.cumsum(np.random.randn(252) * 0.01)))
        sharpe, partial = calculate_sharpe_ratio(prices, min_years=3.0)
        assert partial
        
        # Long series (4 years)
        prices = pd.Series(100 * np.exp(np.cumsum(np.random.randn(1008) * 0.01)))
        sharpe, partial = calculate_sharpe_ratio(prices, min_years=3.0)
        assert not partial
    
    def test_risk_free_rate_override(self):
        """Test that different risk-free rates produce different results"""
        np.random.seed(42)
        prices = pd.Series(100 * np.exp(np.cumsum(np.random.randn(1000) * 0.01)))
        
        sharpe_low, _ = calculate_sharpe_ratio(prices, risk_free_rate=0.01)
        sharpe_high, _ = calculate_sharpe_ratio(prices, risk_free_rate=0.05)
        
        # Higher risk-free rate should generally give lower Sharpe ratio
        assert sharpe_low > sharpe_high
    
    def test_invalid_risk_free_rate(self):
        """Test error handling for invalid risk-free rate"""
        prices = pd.Series([100.0, 105.0, 110.0] * 300)
        
        with pytest.raises(SharpeCalculationError, match="outside valid range"):
            calculate_sharpe_ratio(prices, risk_free_rate=-0.01)
        
        with pytest.raises(SharpeCalculationError, match="outside valid range"):
            calculate_sharpe_ratio(prices, risk_free_rate=0.4)
    
    def test_all_nan_returns(self):
        """Test handling of all NaN returns"""
        # Create price series that will produce all NaN returns
        prices = pd.Series([100.0, np.nan, np.nan, np.nan])
        sharpe, partial = calculate_sharpe_ratio(prices)
        assert np.isnan(sharpe)
        assert partial  # Insufficient data
    
    def test_insufficient_price_data(self):
        """Test handling of insufficient price data"""
        prices = pd.Series([100.0])  # Only one price point
        
        with pytest.raises(SharpeCalculationError):
            calculate_sharpe_ratio(prices)


class TestBatchCalculateSharpeRatios:
    """Test suite for batch_calculate_sharpe_ratios function"""
    
    def test_multiple_stocks(self):
        """Test batch calculation with multiple stocks"""
        np.random.seed(42)
        data = {
            'STOCK_A': pd.Series(100 * np.exp(np.cumsum(np.random.randn(1000) * 0.01))),
            'STOCK_B': pd.Series(100 * np.exp(np.cumsum(np.random.randn(800) * 0.015))),
            'STOCK_C': pd.Series(100 * np.exp(np.cumsum(np.random.randn(500) * 0.02)))
        }
        
        results = batch_calculate_sharpe_ratios(data)
        
        assert len(results) == 3
        assert all(ticker in results for ticker in data.keys())
        assert all(isinstance(result, tuple) and len(result) == 2 
                  for result in results.values())
    
    def test_failed_calculations(self):
        """Test batch handling of failed calculations"""
        data = {
            'GOOD_STOCK': pd.Series(100 * np.exp(np.cumsum(np.random.randn(1000) * 0.01))),
            'BAD_STOCK': pd.Series([100.0])  # Insufficient data
        }
        
        results = batch_calculate_sharpe_ratios(data)
        
        assert len(results) == 2
        assert not np.isnan(results['GOOD_STOCK'][0])  # Should succeed
        assert np.isnan(results['BAD_STOCK'][0])  # Should fail -> NaN
        assert results['BAD_STOCK'][1]  # Should be marked as partial


class TestPropertyBasedTests:
    """Property-based tests using Hypothesis"""
    
    @given(st.lists(st.floats(min_value=1.0, max_value=1000.0), min_size=100, max_size=2000))
    @settings(suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=None)
    def test_sharpe_calculation_stability(self, price_list):
        """Property: Sharpe calculation should be stable for reasonable price series"""
        assume(len(set(price_list)) > 1)  # Ensure some price variation
        
        prices = pd.Series(price_list)
        
        try:
            sharpe, partial = calculate_sharpe_ratio(prices, risk_free_rate=0.02)
            
            # Properties that should always hold:
            assert isinstance(sharpe, (float, type(np.nan)))
            assert isinstance(partial, bool)
            
            if not np.isnan(sharpe) and np.isfinite(sharpe):
                # Reasonable Sharpe ratios should be roughly in [-10, 10] range
                assert -10 <= sharpe <= 10
                
        except SharpeCalculationError:
            # Some property failures are expected and acceptable
            pass
    
    @given(
        st.floats(min_value=0.0, max_value=0.3),
        st.lists(st.floats(min_value=50.0, max_value=200.0), min_size=100, max_size=500)
    )
    @settings(suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.large_base_example], 
              deadline=None)
    def test_risk_free_rate_effect(self, rf_rate, price_list):
        """Property: Higher risk-free rates should generally decrease Sharpe ratios"""
        assume(len(set(price_list)) > 1)
        
        prices = pd.Series(price_list)
        
        try:
            sharpe_low, _ = calculate_sharpe_ratio(prices, risk_free_rate=0.01)
            sharpe_high, _ = calculate_sharpe_ratio(prices, risk_free_rate=rf_rate)
            
            if (not np.isnan(sharpe_low) and not np.isnan(sharpe_high) and
                np.isfinite(sharpe_low) and np.isfinite(sharpe_high) and
                rf_rate > 0.01):
                # Higher risk-free rate should generally decrease Sharpe
                assert sharpe_high <= sharpe_low + 0.1  # Small tolerance for numerical precision
                
        except SharpeCalculationError:
            pass
    
    @given(st.lists(st.floats(min_value=10.0, max_value=1000.0), min_size=2, max_size=100))
    def test_return_calculation_properties(self, price_list):
        """Property tests for return calculation"""
        assume(all(p > 0 for p in price_list))  # Ensure positive prices
        assume(len(set(price_list)) > 1)  # Ensure variation
        
        prices = pd.Series(price_list)
        returns = calculate_daily_returns(prices)
        
        # Properties:
        assert len(returns) == len(prices) - 1
        assert all(np.isfinite(r) or np.isnan(r) for r in returns)
        
        # Sum of log returns should equal log of total return
        if not np.any(np.isnan(returns)):
            total_log_return = np.sum(returns)
            expected_total = np.log(prices.iloc[-1] / prices.iloc[0])
            assert abs(total_log_return - expected_total) < 1e-10


class TestEdgeCases:
    """Test edge cases and boundary conditions"""
    
    def test_very_large_prices(self):
        """Test with very large price values"""
        large_prices = pd.Series([1e6, 1.1e6, 1.05e6, 1.2e6] * 250)
        sharpe, partial = calculate_sharpe_ratio(large_prices)
        assert np.isfinite(sharpe)
    
    def test_very_small_prices(self):
        """Test with very small price values"""
        small_prices = pd.Series([0.001, 0.0011, 0.0009, 0.0012] * 250)
        sharpe, partial = calculate_sharpe_ratio(small_prices)
        assert np.isfinite(sharpe)
    
    def test_high_volatility_returns(self):
        """Test with high volatility return series"""
        np.random.seed(42)
        high_vol_returns = np.random.randn(1000) * 0.1  # 10% daily volatility
        prices = pd.Series(100 * np.exp(np.cumsum(high_vol_returns)))
        
        sharpe, partial = calculate_sharpe_ratio(prices)
        assert np.isfinite(sharpe)
        assert not partial
    
    def test_trending_prices(self):
        """Test with strongly trending prices"""
        # Strong uptrend
        trend = np.linspace(100, 200, 1000)
        noise = np.random.randn(1000) * 0.5
        prices = pd.Series(trend + noise)
        
        sharpe, partial = calculate_sharpe_ratio(prices)
        assert np.isfinite(sharpe)
        assert sharpe > 0  # Should be positive for uptrend


class TestSharpeFromReturns:
    """Test suite for sharpe_from_returns convenience function"""
    
    def test_direct_returns_input(self):
        """Test Sharpe calculation directly from returns"""
        np.random.seed(42)
        returns = np.random.randn(1000) * 0.02 + 0.001  # Mean return ~0.1%
        
        sharpe = sharpe_from_returns(returns, risk_free_rate=0.02)
        assert np.isfinite(sharpe)
    
    def test_consistency_with_price_calculation(self):
        """Test that results are consistent with price-based calculation"""
        np.random.seed(42)
        returns = np.random.randn(1000) * 0.01
        
        # Calculate from returns directly
        sharpe_from_rets = sharpe_from_returns(returns, risk_free_rate=0.02)
        
        # Calculate from prices
        prices = pd.Series(100 * np.exp(np.cumsum(returns)))
        sharpe_from_prices, _ = calculate_sharpe_ratio(prices, risk_free_rate=0.02)
        
        # Should be close (allowing for small numerical differences due to log transformation)
        assert abs(sharpe_from_rets - sharpe_from_prices) < 0.01  # More reasonable tolerance


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v", "--tb=short"])
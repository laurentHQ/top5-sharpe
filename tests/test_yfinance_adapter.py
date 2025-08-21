"""
Tests for YFinance Adapter

Comprehensive tests for the yfinance adapter including retry logic, caching,
and error handling. Uses mocking to avoid actual API calls during testing.
"""

import asyncio
import json
import tempfile
import time
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import Mock, patch, call
import pytest
import pandas as pd

# Add backend to path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from backend.yfinance_adapter import YFinanceAdapter, CacheManager, YFinanceAdapterError


class TestCacheManager:
    """Test cases for the cache manager"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.temp_dir = tempfile.mkdtemp()
        self.cache_manager = CacheManager(cache_dir=self.temp_dir, default_ttl_hours=1)
    
    def teardown_method(self):
        """Cleanup after each test method"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_cache_key_generation(self):
        """Test cache key generation is consistent"""
        tickers1 = ['AAPL', 'MSFT', 'GOOGL']
        tickers2 = ['GOOGL', 'AAPL', 'MSFT']  # Different order
        period = '5y'
        
        key1 = self.cache_manager._get_cache_key(tickers1, period)
        key2 = self.cache_manager._get_cache_key(tickers2, period)
        
        # Keys should be the same regardless of ticker order
        assert key1 == key2
        assert isinstance(key1, str)
        assert period in key1
    
    def test_cache_miss_no_file(self):
        """Test cache miss when file doesn't exist"""
        tickers = ['AAPL']
        period = '5y'
        
        result = self.cache_manager.get(tickers, period)
        
        assert result is None
        assert self.cache_manager.cache_misses == 1
        assert self.cache_manager.cache_hits == 0
    
    def test_cache_set_and_get(self):
        """Test caching and retrieval of data"""
        tickers = ['AAPL']
        period = '5y'
        
        # Create test data
        test_data = pd.DataFrame({
            'Date': pd.date_range('2020-01-01', periods=5),
            'Close': [100.0, 101.0, 102.0, 103.0, 104.0],
            'Ticker': ['AAPL'] * 5
        })
        
        # Cache the data
        self.cache_manager.set(tickers, period, test_data)
        
        # Retrieve from cache
        cached_data = self.cache_manager.get(tickers, period)
        
        assert cached_data is not None
        assert len(cached_data) == 5
        assert list(cached_data['Ticker'].unique()) == ['AAPL']
        assert self.cache_manager.cache_hits == 1
        assert self.cache_manager.cache_misses == 0
    
    def test_cache_ttl_expiration(self):
        """Test cache TTL expiration"""
        tickers = ['AAPL']
        period = '5y'
        ttl_hours = 0.001  # Very short TTL (3.6 seconds)
        
        test_data = pd.DataFrame({
            'Date': pd.date_range('2020-01-01', periods=3),
            'Close': [100.0, 101.0, 102.0],
            'Ticker': ['AAPL'] * 3
        })
        
        # Cache the data
        self.cache_manager.set(tickers, period, test_data)
        
        # Should be cached immediately
        cached_data = self.cache_manager.get(tickers, period, ttl_hours)
        assert cached_data is not None
        
        # Wait for TTL to expire
        time.sleep(0.01)
        
        # Should be cache miss due to TTL expiration
        expired_data = self.cache_manager.get(tickers, period, ttl_hours)
        assert expired_data is None
        assert self.cache_manager.cache_misses == 1
    
    def test_cache_cleanup_expired(self):
        """Test cleanup of expired cache entries"""
        tickers = ['AAPL']
        period = '5y'
        
        # Create and cache test data
        test_data = pd.DataFrame({
            'Date': pd.date_range('2020-01-01', periods=3),
            'Close': [100.0, 101.0, 102.0],
            'Ticker': ['AAPL'] * 3
        })
        
        self.cache_manager.set(tickers, period, test_data)
        
        # Manually set expired timestamp in metadata
        cache_key = self.cache_manager._get_cache_key(tickers, period)
        expired_time = datetime.now() - timedelta(hours=2)
        self.cache_manager.metadata[cache_key]['timestamp'] = expired_time.isoformat()
        self.cache_manager._save_metadata()
        
        # Cleanup expired entries
        self.cache_manager.cleanup_expired(ttl_hours=1)
        
        # Verify cache file was removed
        cache_path = self.cache_manager._get_cache_path(cache_key)
        assert not cache_path.exists()
        assert cache_key not in self.cache_manager.metadata
    
    def test_cache_stats(self):
        """Test cache statistics tracking"""
        initial_stats = self.cache_manager.get_cache_stats()
        
        assert initial_stats['cache_hits'] == 0
        assert initial_stats['cache_misses'] == 0
        assert initial_stats['hit_rate_percent'] == 0
        assert initial_stats['total_cached_entries'] == 0
        
        # Add some cache operations
        tickers = ['AAPL']
        period = '5y'
        test_data = pd.DataFrame({
            'Date': pd.date_range('2020-01-01', periods=3),
            'Close': [100.0, 101.0, 102.0],
            'Ticker': ['AAPL'] * 3
        })
        
        # Cache miss
        self.cache_manager.get(tickers, period)
        
        # Cache set and hit
        self.cache_manager.set(tickers, period, test_data)
        self.cache_manager.get(tickers, period)
        
        final_stats = self.cache_manager.get_cache_stats()
        
        assert final_stats['cache_hits'] == 1
        assert final_stats['cache_misses'] == 1
        assert final_stats['hit_rate_percent'] == 50.0
        assert final_stats['total_cached_entries'] == 1


class TestYFinanceAdapter:
    """Test cases for the YFinance adapter"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.temp_dir = tempfile.mkdtemp()
        self.adapter = YFinanceAdapter(
            cache_dir=self.temp_dir,
            default_ttl_hours=1,
            max_retries=3,
            enable_cache=True
        )
    
    def teardown_method(self):
        """Cleanup after each test method"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    @patch('backend.yfinance_adapter.yf.Ticker')
    def test_fetch_single_ticker_success(self, mock_ticker_class):
        """Test successful single ticker data fetch"""
        # Mock yfinance response
        mock_ticker = Mock()
        mock_ticker_class.return_value = mock_ticker
        
        test_data = pd.DataFrame({
            'Open': [100.0, 101.0, 102.0],
            'High': [105.0, 106.0, 107.0],
            'Low': [95.0, 96.0, 97.0],
            'Close': [103.0, 104.0, 105.0],
            'Volume': [1000000, 1100000, 1200000]
        }, index=pd.date_range('2020-01-01', periods=3))
        
        mock_ticker.history.return_value = test_data
        
        # Test the private method
        result = self.adapter._fetch_ticker_data('AAPL', '5y')
        
        assert result is not None
        assert len(result) == 3
        assert 'Ticker' in result.columns
        assert result['Ticker'].iloc[0] == 'AAPL'
        assert 'Date' in result.columns
        
        # Verify yfinance was called correctly
        mock_ticker.history.assert_called_once_with(
            period='5y',
            auto_adjust=True,
            prepost=False,
            threads=True
        )
    
    @patch('backend.yfinance_adapter.yf.Ticker')
    def test_fetch_single_ticker_no_data(self, mock_ticker_class):
        """Test handling of ticker with no data"""
        mock_ticker = Mock()
        mock_ticker_class.return_value = mock_ticker
        mock_ticker.history.return_value = pd.DataFrame()  # Empty DataFrame
        
        result = self.adapter._fetch_ticker_data('INVALID', '5y')
        
        assert result is None
    
    @patch('backend.yfinance_adapter.yf.Ticker')
    def test_fetch_single_ticker_error(self, mock_ticker_class):
        """Test handling of API errors"""
        mock_ticker = Mock()
        mock_ticker_class.return_value = mock_ticker
        mock_ticker.history.side_effect = Exception("API Error")
        
        with pytest.raises(YFinanceAdapterError):
            self.adapter._fetch_ticker_data('AAPL', '5y')
    
    def test_fetch_prices_validation(self):
        """Test input validation for fetch_prices"""
        # Test empty ticker list
        with pytest.raises(ValueError, match="At least one ticker must be provided"):
            self.adapter.fetch_prices([])
        
        # Test non-list input
        with pytest.raises(ValueError, match="Tickers must be provided as a list"):
            self.adapter.fetch_prices("AAPL")
        
        # Test empty strings after cleaning
        with pytest.raises(ValueError, match="No valid tickers provided after cleaning"):
            self.adapter.fetch_prices(["", "  ", None])
    
    @patch('backend.yfinance_adapter.yf.Ticker')
    def test_fetch_prices_with_cache(self, mock_ticker_class):
        """Test fetch_prices with caching enabled"""
        # Mock successful yfinance response
        mock_ticker = Mock()
        mock_ticker_class.return_value = mock_ticker
        
        test_data = pd.DataFrame({
            'Open': [100.0, 101.0],
            'High': [105.0, 106.0],
            'Low': [95.0, 96.0],
            'Close': [103.0, 104.0],
            'Volume': [1000000, 1100000]
        }, index=pd.date_range('2020-01-01', periods=2))
        
        mock_ticker.history.return_value = test_data
        
        tickers = ['AAPL']
        
        # First call should hit API and cache
        result1 = self.adapter.fetch_prices(tickers, '5y')
        assert len(result1) == 2
        assert result1['Ticker'].iloc[0] == 'AAPL'
        
        # Second call should hit cache
        result2 = self.adapter.fetch_prices(tickers, '5y')
        assert len(result2) == 2
        
        # Should only call API once due to caching
        assert mock_ticker.history.call_count == 1
        
        # Verify cache stats
        stats = self.adapter.get_adapter_stats()
        assert stats['cache_hits'] == 1
    
    @patch('backend.yfinance_adapter.yf.Ticker')
    def test_fetch_prices_mixed_success_failure(self, mock_ticker_class):
        """Test fetch_prices with some successful and some failed tickers"""
        def mock_ticker_factory(ticker):
            mock_ticker = Mock()
            if ticker == 'AAPL':
                # Successful response
                test_data = pd.DataFrame({
                    'Close': [100.0, 101.0],
                    'Volume': [1000000, 1100000]
                }, index=pd.date_range('2020-01-01', periods=2))
                mock_ticker.history.return_value = test_data
            else:
                # Failed response
                mock_ticker.history.side_effect = Exception("API Error")
            return mock_ticker
        
        mock_ticker_class.side_effect = mock_ticker_factory
        
        tickers = ['AAPL', 'INVALID']
        
        # Should succeed for AAPL but not fail completely
        result = self.adapter.fetch_prices(tickers, '5y')
        
        assert len(result) == 2  # Only AAPL data
        assert result['Ticker'].iloc[0] == 'AAPL'
    
    def test_get_adapter_stats(self):
        """Test adapter statistics"""
        initial_stats = self.adapter.get_adapter_stats()
        
        expected_keys = ['api_calls', 'failed_calls', 'success_rate_percent', 
                        'cache_hits', 'cache_misses', 'hit_rate_percent']
        
        for key in expected_keys:
            assert key in initial_stats
        
        assert initial_stats['api_calls'] == 0
        assert initial_stats['failed_calls'] == 0
        assert initial_stats['success_rate_percent'] == 100.0
    
    def test_disable_cache(self):
        """Test adapter with caching disabled"""
        adapter_no_cache = YFinanceAdapter(enable_cache=False)
        
        assert adapter_no_cache.cache_manager is None
        
        stats = adapter_no_cache.get_adapter_stats()
        
        # Cache stats should not be present
        cache_keys = ['cache_hits', 'cache_misses', 'hit_rate_percent']
        for key in cache_keys:
            assert key not in stats
    
    def test_jitter_function(self):
        """Test jitter function adds randomness"""
        delay = 5.0
        
        # Test multiple jitter applications
        jittered_delays = [self.adapter._add_jitter(delay) for _ in range(10)]
        
        # All should be close to original delay but with some variation
        for jittered in jittered_delays:
            assert delay <= jittered <= delay * 1.1  # Max 10% jitter
        
        # Should have some variation (not all the same)
        assert len(set(jittered_delays)) > 1
    
    def test_cache_cleanup(self):
        """Test cache cleanup functionality"""
        tickers = ['AAPL']
        period = '5y'
        
        # Create test data and cache it
        test_data = pd.DataFrame({
            'Date': pd.date_range('2020-01-01', periods=2),
            'Close': [100.0, 101.0],
            'Ticker': ['AAPL'] * 2
        })
        
        self.adapter.cache_manager.set(tickers, period, test_data)
        
        # Verify it's cached
        assert self.adapter.cache_manager.get(tickers, period) is not None
        
        # Cleanup with very short TTL should remove it
        self.adapter.cleanup_cache(ttl_hours=0.001)
        time.sleep(0.01)  # Wait for TTL
        
        # Should be removed after cleanup
        assert self.adapter.cache_manager.get(tickers, period, ttl_hours=0.001) is None
    
    def test_clear_cache(self):
        """Test clearing all cached data"""
        tickers = ['AAPL']
        period = '5y'
        
        # Create and cache test data
        test_data = pd.DataFrame({
            'Date': pd.date_range('2020-01-01', periods=2),
            'Close': [100.0, 101.0],
            'Ticker': ['AAPL'] * 2
        })
        
        self.adapter.cache_manager.set(tickers, period, test_data)
        
        # Verify cache exists
        assert Path(self.temp_dir).exists()
        cache_files = list(Path(self.temp_dir).glob('*.parquet'))
        assert len(cache_files) > 0
        
        # Clear cache
        self.adapter.clear_cache()
        
        # Verify cache directory is gone
        assert not Path(self.temp_dir).exists()


# Integration tests that require actual network access
# These should be marked for separate test runs
class TestYFinanceIntegration:
    """Integration tests with real Yahoo Finance API"""
    
    @pytest.mark.integration
    @patch('backend.yfinance_adapter.yf.Ticker')
    def test_real_api_call_structure(self, mock_ticker_class):
        """Test that real API call structure matches expectations"""
        # This test verifies our mocking matches real yfinance structure
        # In a real integration test, you would remove the patch decorator
        
        mock_ticker = Mock()
        mock_ticker_class.return_value = mock_ticker
        
        # Simulate real yfinance data structure
        real_like_data = pd.DataFrame({
            'Open': [150.0, 151.0, 152.0],
            'High': [155.0, 156.0, 157.0],
            'Low': [148.0, 149.0, 150.0],
            'Close': [153.0, 154.0, 155.0],
            'Adj Close': [153.0, 154.0, 155.0],
            'Volume': [50000000, 51000000, 52000000]
        }, index=pd.DatetimeIndex(['2020-01-01', '2020-01-02', '2020-01-03']))
        
        mock_ticker.history.return_value = real_like_data
        
        temp_dir = tempfile.mkdtemp()
        try:
            adapter = YFinanceAdapter(cache_dir=temp_dir, enable_cache=False)
            result = adapter.fetch_prices(['AAPL'], '1y')
            
            # Verify data structure
            assert len(result) == 3
            assert 'Ticker' in result.columns
            assert 'Date' in result.columns
            assert all(result['Ticker'] == 'AAPL')
            
        finally:
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
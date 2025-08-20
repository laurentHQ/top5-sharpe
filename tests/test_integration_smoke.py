"""
Integration Smoke Tests

Basic smoke tests to verify the main components work together.
These tests use mocked data to avoid external API dependencies.
"""

import tempfile
from pathlib import Path
from unittest.mock import Mock, patch
import pytest
import pandas as pd

# Add backend to path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from backend import DataService, DataServiceConfig
from backend.yfinance_adapter import YFinanceAdapter


class TestIntegrationSmoke:
    """Smoke tests for integration between components"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.temp_dir = tempfile.mkdtemp()
        self.config = DataServiceConfig(
            cache_dir=self.temp_dir,
            default_ttl_hours=1,
            enable_cache=True
        )
    
    def teardown_method(self):
        """Cleanup after each test method"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    @patch('backend.data_service.yf.Ticker')
    @patch('backend.data_service.get_sp500_tickers')
    def test_full_pipeline_smoke(self, mock_get_sp500_tickers, mock_ticker_class):
        """Test full pipeline from service to adapter to cache"""
        # Mock S&P 500 tickers
        mock_get_sp500_tickers.return_value = ['AAPL', 'MSFT']
        
        # Mock yfinance responses
        def mock_ticker_factory(ticker):
            mock_ticker = Mock()
            
            # Create realistic test data
            base_price = 100 if ticker == 'AAPL' else 200
            test_data = pd.DataFrame({
                'Open': [base_price + i for i in range(300)],
                'High': [base_price + i + 5 for i in range(300)],
                'Low': [base_price + i - 5 for i in range(300)],
                'Close': [base_price + i + 2 for i in range(300)],
                'Volume': [1000000 + i * 1000 for i in range(300)]
            }, index=pd.date_range('2020-01-01', periods=300))
            
            mock_ticker.history.return_value = test_data
            return mock_ticker
        
        mock_ticker_class.side_effect = mock_ticker_factory
        
        # Create service and fetch data
        service = DataService(self.config)
        
        # Test 1: Get individual stock data
        result = service.get_stock_data(['AAPL'], period='1y', validate_quality=True)
        
        assert result.success is True
        assert result.data is not None
        assert len(result.data) == 300
        assert result.cache_hit is False  # First call should not be cached
        assert len(result.quality_results) == 1
        assert result.quality_results[0].is_valid is True
        
        # Test 2: Same request should hit cache
        result2 = service.get_stock_data(['AAPL'], period='1y')
        
        assert result2.success is True
        assert result2.cache_hit is True
        
        # Test 3: Get S&P 500 data (limited)
        sp500_result = service.get_sp500_data(period='1y', max_tickers=2)
        
        assert sp500_result.success is True
        assert sp500_result.data is not None
        assert len(sp500_result.data) == 600  # 300 * 2 tickers
        assert len(sp500_result.failed_tickers) == 0
    
    @patch('backend.yfinance_adapter.yf.Ticker')
    def test_adapter_retry_and_cache_smoke(self, mock_ticker_class):
        """Test adapter retry logic and caching work together"""
        call_count = 0
        
        def failing_then_succeeding_ticker(ticker):
            nonlocal call_count
            call_count += 1
            
            mock_ticker = Mock()
            
            if call_count <= 2:
                # Fail first two calls
                mock_ticker.history.side_effect = Exception("API temporarily unavailable")
            else:
                # Succeed on third call
                test_data = pd.DataFrame({
                    'Close': [100.0, 101.0, 102.0],
                    'Volume': [1000000, 1100000, 1200000]
                }, index=pd.date_range('2020-01-01', periods=3))
                mock_ticker.history.return_value = test_data
            
            return mock_ticker
        
        mock_ticker_class.side_effect = failing_then_succeeding_ticker
        
        # Create adapter with low retry count for faster testing
        adapter = YFinanceAdapter(
            cache_dir=self.temp_dir,
            max_retries=3,
            enable_cache=True
        )
        
        # Should succeed after retries
        result = adapter.fetch_prices(['AAPL'], '1y')
        
        assert len(result) == 3
        assert result['Ticker'].iloc[0] == 'AAPL'
        
        # Verify retry logic was used (should have 3 calls)
        assert call_count == 3
        
        # Second call should hit cache and not increment call count
        result2 = adapter.fetch_prices(['AAPL'], '1y')
        assert len(result2) == 3
        assert call_count == 3  # No additional API calls
    
    def test_service_health_check_smoke(self):
        """Test service health check returns expected structure"""
        service = DataService(self.config)
        health = service.get_service_health()
        
        # Check required health fields
        required_fields = [
            'service_name', 'timestamp', 'status', 'config',
            'api_calls', 'failed_calls', 'success_rate_percent'
        ]
        
        for field in required_fields:
            assert field in health
        
        assert health['service_name'] == 'DataService'
        assert health['status'] == 'healthy'
        assert isinstance(health['config'], dict)
    
    @patch('backend.data_service.yf.Ticker')
    def test_data_quality_validation_smoke(self, mock_ticker_class):
        """Test data quality validation with various data scenarios"""
        def mock_ticker_factory(ticker):
            mock_ticker = Mock()
            
            if ticker == 'GOOD_STOCK':
                # Good quality data
                test_data = pd.DataFrame({
                    'Open': range(100, 500),
                    'High': range(105, 505),
                    'Low': range(95, 495),
                    'Close': range(103, 503),
                    'Volume': range(1000000, 1400000)
                }, index=pd.date_range('2020-01-01', periods=400))
                
            elif ticker == 'BAD_STOCK':
                # Poor quality data (too few points, missing values)
                test_data = pd.DataFrame({
                    'Open': [100.0, 101.0, None, 103.0],
                    'High': [105.0, 106.0, 107.0, None],
                    'Low': [95.0, 96.0, 97.0, 98.0],
                    'Close': [103.0, 104.0, 105.0, 106.0],
                    'Volume': [1000000, 1100000, 1200000, 1300000]
                }, index=pd.date_range('2023-01-01', periods=4))
                
            else:
                # Empty data
                test_data = pd.DataFrame()
            
            mock_ticker.history.return_value = test_data
            return mock_ticker
        
        mock_ticker_class.side_effect = mock_ticker_factory
        
        service = DataService(self.config)
        
        # Test good stock
        good_result = service.get_stock_data(['GOOD_STOCK'], validate_quality=True)
        assert good_result.success is True
        assert len(good_result.quality_results) == 1
        assert good_result.quality_results[0].is_valid is True
        
        # Test bad stock
        bad_result = service.get_stock_data(['BAD_STOCK'], validate_quality=True)
        assert bad_result.success is True
        assert len(bad_result.quality_results) == 1
        assert bad_result.quality_results[0].is_valid is False
        assert len(bad_result.quality_results[0].issues) > 0
        
        # Test invalid stock
        invalid_result = service.get_stock_data(['INVALID_STOCK'])
        assert invalid_result.success is False
        assert 'INVALID_STOCK' in invalid_result.failed_tickers
    
    def test_cache_performance_smoke(self):
        """Test cache performance characteristics"""
        adapter = YFinanceAdapter(
            cache_dir=self.temp_dir,
            enable_cache=True
        )
        
        # Create test data
        test_data = pd.DataFrame({
            'Date': pd.date_range('2020-01-01', periods=1000),
            'Close': range(1000),
            'Volume': range(1000000, 2000000),
            'Ticker': ['TEST'] * 1000
        })
        
        tickers = ['TEST']
        period = '5y'
        
        # Cache the data
        adapter.cache_manager.set(tickers, period, test_data)
        
        # Verify it's cached and retrieve it
        cached_data = adapter.cache_manager.get(tickers, period)
        
        assert cached_data is not None
        assert len(cached_data) == 1000
        
        # Check cache stats
        stats = adapter.cache_manager.get_cache_stats()
        assert stats['cache_hits'] == 1
        assert stats['hit_rate_percent'] == 100.0
        assert stats['total_cached_entries'] == 1
        
        # Test cache cleanup
        adapter.cache_manager.cleanup_expired(ttl_hours=0.001)
        
        # Should still be there (not expired yet)
        assert adapter.cache_manager.get(tickers, period) is not None


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
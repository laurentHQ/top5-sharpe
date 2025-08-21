"""
Tests for Data Service

Comprehensive tests for the data service layer including business logic,
validation, and integration with the yfinance adapter and S&P 500 loader.
"""

import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import pytest
import pandas as pd

# Add backend to path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from backend.data_service import DataService, DataServiceConfig, StockDataResult, DataQualityResult


class TestDataServiceConfig:
    """Test cases for data service configuration"""
    
    def test_default_config(self):
        """Test default configuration values"""
        config = DataServiceConfig()
        
        assert config.cache_dir == "data/cache"
        assert config.default_ttl_hours == 24
        assert config.enable_cache is True
        assert config.max_retries == 5
        assert config.min_data_points == 252
        assert config.min_data_years == 3.0
    
    def test_config_validation(self):
        """Test configuration validation"""
        # Test invalid TTL
        with pytest.raises(ValueError, match="TTL must be between 1 and 168 hours"):
            DataServiceConfig(default_ttl_hours=0)
        
        with pytest.raises(ValueError, match="TTL must be between 1 and 168 hours"):
            DataServiceConfig(default_ttl_hours=200)
    
    def test_config_with_custom_cache_dir(self):
        """Test configuration with custom cache directory"""
        temp_dir = tempfile.mkdtemp()
        try:
            config = DataServiceConfig(cache_dir=temp_dir)
            assert config.cache_dir == temp_dir
            assert Path(temp_dir).exists()
        finally:
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)


class TestDataQualityResult:
    """Test cases for data quality result model"""
    
    def test_data_quality_result_creation(self):
        """Test creating data quality result"""
        result = DataQualityResult(
            ticker="AAPL",
            is_valid=True,
            data_points=1000,
            date_range_days=1000,
            date_range_years=2.74,
            first_date=datetime(2020, 1, 1),
            last_date=datetime(2022, 9, 27),
            issues=[]
        )
        
        assert result.ticker == "AAPL"
        assert result.is_valid is True
        assert result.data_points == 1000
        assert len(result.issues) == 0
    
    def test_data_quality_result_with_issues(self):
        """Test data quality result with validation issues"""
        issues = ["Insufficient data points", "Missing volume data"]
        
        result = DataQualityResult(
            ticker="BADSTOCK",
            is_valid=False,
            data_points=100,
            date_range_days=100,
            date_range_years=0.27,
            first_date=datetime(2023, 1, 1),
            last_date=datetime(2023, 4, 11),
            issues=issues
        )
        
        assert result.is_valid is False
        assert len(result.issues) == 2
        assert "Insufficient data points" in result.issues


class TestStockDataResult:
    """Test cases for stock data result model"""
    
    def test_stock_data_result_success(self):
        """Test successful stock data result"""
        test_data = pd.DataFrame({
            'Date': pd.date_range('2020-01-01', periods=5),
            'Close': [100.0, 101.0, 102.0, 103.0, 104.0],
            'Ticker': ['AAPL'] * 5
        })
        
        result = StockDataResult(
            success=True,
            data=test_data,
            failed_tickers=[],
            cache_hit=True,
            fetch_duration_seconds=1.5
        )
        
        assert result.success is True
        assert result.data is not None
        assert len(result.data) == 5
        assert len(result.failed_tickers) == 0
        assert result.cache_hit is True
        assert result.fetch_duration_seconds == 1.5
    
    def test_stock_data_result_failure(self):
        """Test failed stock data result"""
        result = StockDataResult(
            success=False,
            data=None,
            failed_tickers=['INVALID1', 'INVALID2'],
            cache_hit=False,
            fetch_duration_seconds=10.0
        )
        
        assert result.success is False
        assert result.data is None
        assert len(result.failed_tickers) == 2
        assert result.cache_hit is False


class TestDataService:
    """Test cases for the data service"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.temp_dir = tempfile.mkdtemp()
        self.config = DataServiceConfig(
            cache_dir=self.temp_dir,
            default_ttl_hours=1,
            min_data_points=10,  # Lower for testing
            min_data_years=0.1   # Lower for testing
        )
    
    def teardown_method(self):
        """Cleanup after each test method"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    @patch('backend.data_service.SP500Loader')
    @patch('backend.data_service.YFinanceAdapter')
    def test_service_initialization(self, mock_adapter_class, mock_sp500_loader_class):
        """Test service initialization"""
        service = DataService(self.config)
        
        assert service.config == self.config
        mock_adapter_class.assert_called_once()
        mock_sp500_loader_class.assert_called_once()
    
    @patch('backend.data_service.SP500Loader')
    @patch('backend.data_service.YFinanceAdapter')
    def test_get_stock_data_success(self, mock_adapter_class, mock_sp500_loader_class):
        """Test successful stock data retrieval"""
        # Mock the adapter
        mock_adapter = Mock()
        mock_adapter_class.return_value = mock_adapter
        
        # Create test data
        test_data = pd.DataFrame({
            'Date': pd.date_range('2020-01-01', periods=500),  # Sufficient data
            'Open': range(100, 600),
            'High': range(105, 605),
            'Low': range(95, 595),
            'Close': range(103, 603),
            'Volume': range(1000000, 1500000),
            'Ticker': ['AAPL'] * 500
        })
        
        mock_adapter.fetch_prices.return_value = test_data
        mock_adapter.cache_manager = None  # Disable cache for this test
        
        service = DataService(self.config)
        result = service.get_stock_data(['AAPL'], '5y')
        
        assert result.success is True
        assert result.data is not None
        assert len(result.data) == 500
        assert len(result.failed_tickers) == 0
        assert result.fetch_duration_seconds > 0
    
    @patch('backend.data_service.SP500Loader')
    @patch('backend.data_service.YFinanceAdapter')
    def test_get_stock_data_with_validation(self, mock_adapter_class, mock_sp500_loader_class):
        """Test stock data retrieval with quality validation"""
        mock_adapter = Mock()
        mock_adapter_class.return_value = mock_adapter
        
        # Create test data with quality issues
        test_data = pd.DataFrame({
            'Date': pd.date_range('2023-01-01', periods=50),  # Insufficient data
            'Open': [100.0] * 50,
            'High': [None] * 50,  # Missing high prices
            'Low': [95.0] * 50,
            'Close': [103.0] * 50,
            'Volume': [1000000] * 50,
            'Ticker': ['BADSTOCK'] * 50
        })
        
        mock_adapter.fetch_prices.return_value = test_data
        mock_adapter.cache_manager = None
        
        service = DataService(self.config)
        result = service.get_stock_data(['BADSTOCK'], '5y', validate_quality=True)
        
        assert result.success is True
        assert len(result.quality_results) == 1
        
        quality_result = result.quality_results[0]
        assert quality_result.ticker == 'BADSTOCK'
        assert quality_result.is_valid is False  # Should fail validation
        assert len(quality_result.issues) > 0
    
    def test_validate_data_quality_good_data(self):
        """Test data quality validation with good data"""
        service = DataService(self.config)
        
        # Create good quality data
        good_data = pd.DataFrame({
            'Date': pd.date_range('2020-01-01', periods=400),
            'Open': range(100, 500),
            'High': range(105, 505),
            'Low': range(95, 495),
            'Close': range(103, 503),
            'Volume': range(1000000, 1400000),
            'Ticker': ['AAPL'] * 400
        })
        
        results = service._validate_data_quality(good_data)
        
        assert len(results) == 1
        result = results[0]
        assert result.ticker == 'AAPL'
        assert result.is_valid is True
        assert result.data_points == 400
        assert len(result.issues) == 0
    
    def test_validate_data_quality_bad_data(self):
        """Test data quality validation with problematic data"""
        service = DataService(self.config)
        
        # Create problematic data
        bad_data = pd.DataFrame({
            'Date': pd.date_range('2023-01-01', periods=5),  # Too few points
            'Open': [100.0, 101.0, None, 103.0, 104.0],     # Missing values
            'High': [105.0, 106.0, 107.0, 108.0, 109.0],
            'Low': [95.0, 96.0, 97.0, 98.0, 99.0],
            'Close': [103.0, 104.0, 1000.0, 106.0, 107.0],  # Extreme movement
            'Volume': [1000000] * 5,
            'Ticker': ['BADSTOCK'] * 5
        })
        
        results = service._validate_data_quality(bad_data)
        
        assert len(results) == 1
        result = results[0]
        assert result.ticker == 'BADSTOCK'
        assert result.is_valid is False
        assert len(result.issues) >= 2  # Multiple issues
    
    @patch('backend.data_service.SP500Loader')
    @patch('backend.data_service.YFinanceAdapter')
    def test_get_sp500_data(self, mock_adapter_class, mock_sp500_loader_class):
        """Test S&P 500 data retrieval"""
        # Mock SP500 loader
        mock_sp500_loader = Mock()
        mock_sp500_loader_class.return_value = mock_sp500_loader
        mock_sp500_loader.get_tickers.return_value = ['AAPL', 'MSFT', 'GOOGL']
        
        # Mock adapter
        mock_adapter = Mock()
        mock_adapter_class.return_value = mock_adapter
        
        test_data = pd.DataFrame({
            'Date': pd.date_range('2020-01-01', periods=300),
            'Close': list(range(100, 200)) * 3,
            'Ticker': ['AAPL'] * 100 + ['MSFT'] * 100 + ['GOOGL'] * 100
        })
        
        mock_adapter.fetch_prices.return_value = test_data
        mock_adapter.cache_manager = None
        
        service = DataService(self.config)
        result = service.get_sp500_data(period='1y', max_tickers=3)
        
        assert result.success is True
        assert result.data is not None
        mock_sp500_loader.get_tickers.assert_called_once()
        mock_adapter.fetch_prices.assert_called_once_with(['AAPL', 'MSFT', 'GOOGL'], '1y', True, None)
    
    @patch('backend.data_service.SP500Loader')
    @patch('backend.data_service.YFinanceAdapter')
    def test_get_service_health(self, mock_adapter_class, mock_sp500_loader_class):
        """Test service health monitoring"""
        # Mock SP500 loader
        mock_sp500_loader = Mock()
        mock_sp500_loader_class.return_value = mock_sp500_loader
        mock_sp500_loader.get_tickers.return_value = ['AAPL', 'MSFT']
        mock_sp500_loader.csv_path = Path('data/sp500.csv')
        
        # Mock adapter
        mock_adapter = Mock()
        mock_adapter_class.return_value = mock_adapter
        mock_adapter.get_adapter_stats.return_value = {
            'api_calls': 10,
            'failed_calls': 1,
            'success_rate_percent': 90.0,
            'cache_hits': 5,
            'cache_misses': 3
        }
        mock_adapter.cache_manager = Mock()
        mock_adapter.cache_manager.cache_dir = Path(self.temp_dir)
        
        service = DataService(self.config)
        health = service.get_service_health()
        
        assert health['service_name'] == 'DataService'
        assert 'timestamp' in health
        assert health['status'] == 'healthy'
        assert health['api_calls'] == 10
        assert health['sp500_loaded'] is True
        assert health['sp500_ticker_count'] == 2
    
    @patch.dict('os.environ', {
        'STOCK_CACHE_DIR': '/tmp/test_cache',
        'STOCK_DEFAULT_TTL_HOURS': '12',
        'STOCK_ENABLE_CACHE': 'false',
        'STOCK_MAX_RETRIES': '3'
    })
    @patch('backend.data_service.SP500Loader')
    @patch('backend.data_service.YFinanceAdapter')
    def test_from_env_creation(self, mock_adapter_class, mock_sp500_loader_class):
        """Test creating service from environment variables"""
        service = DataService.from_env()
        
        assert service.config.cache_dir == '/tmp/test_cache'
        assert service.config.default_ttl_hours == 12
        assert service.config.enable_cache is False
        assert service.config.max_retries == 3
    
    @patch('backend.data_service.SP500Loader')
    @patch('backend.data_service.YFinanceAdapter')
    def test_cache_cleanup(self, mock_adapter_class, mock_sp500_loader_class):
        """Test cache cleanup functionality"""
        mock_adapter = Mock()
        mock_adapter_class.return_value = mock_adapter
        
        service = DataService(self.config)
        service.cleanup_cache(ttl_hours=12)
        
        mock_adapter.cleanup_cache.assert_called_once_with(12)
    
    @patch('backend.data_service.SP500Loader')
    @patch('backend.data_service.YFinanceAdapter')
    def test_clear_cache(self, mock_adapter_class, mock_sp500_loader_class):
        """Test clearing all cached data"""
        mock_adapter = Mock()
        mock_adapter_class.return_value = mock_adapter
        
        service = DataService(self.config)
        service.clear_cache()
        
        mock_adapter.clear_cache.assert_called_once()
    
    @patch('backend.data_service.SP500Loader')
    @patch('backend.data_service.YFinanceAdapter')
    def test_get_stock_data_adapter_failure(self, mock_adapter_class, mock_sp500_loader_class):
        """Test handling of adapter failures"""
        mock_adapter = Mock()
        mock_adapter_class.return_value = mock_adapter
        mock_adapter.fetch_prices.side_effect = Exception("API Error")
        
        service = DataService(self.config)
        result = service.get_stock_data(['AAPL'], '5y')
        
        assert result.success is False
        assert result.data is None
        assert 'AAPL' in result.failed_tickers
        assert result.fetch_duration_seconds > 0
    
    @patch('backend.data_service.SP500Loader')
    @patch('backend.data_service.YFinanceAdapter')
    def test_get_stock_data_empty_result(self, mock_adapter_class, mock_sp500_loader_class):
        """Test handling of empty data from adapter"""
        mock_adapter = Mock()
        mock_adapter_class.return_value = mock_adapter
        mock_adapter.fetch_prices.return_value = pd.DataFrame()  # Empty DataFrame
        mock_adapter.cache_manager = None
        
        service = DataService(self.config)
        result = service.get_stock_data(['INVALID'], '5y')
        
        assert result.success is False
        assert result.data is None
        assert 'INVALID' in result.failed_tickers


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
"""
Tests for Configuration Management

Tests for the configuration system including environment variable handling,
validation, and different environment configurations.
"""

import os
import tempfile
from pathlib import Path
from unittest.mock import patch
import pytest

# Add backend to path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from backend.config import (
    Settings, DevelopmentSettings, TestingSettings, ProductionSettings,
    Environment, LogLevel, get_settings, create_env_file
)


class TestSettings:
    """Test cases for base settings"""
    
    def test_default_settings(self):
        """Test default settings values"""
        settings = Settings()
        
        assert settings.environment == Environment.DEVELOPMENT
        assert settings.debug is True
        assert settings.log_level == LogLevel.INFO
        assert settings.cache_dir == "data/cache"
        assert settings.default_ttl_hours == 24
        assert settings.enable_cache is True
        assert settings.max_retries == 5
    
    def test_settings_with_custom_cache_dir(self):
        """Test settings with custom cache directory"""
        temp_dir = tempfile.mkdtemp()
        try:
            settings = Settings(cache_dir=temp_dir)
            assert settings.cache_dir == temp_dir
            assert Path(temp_dir).exists()
        finally:
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)
    
    def test_cache_dir_validation_invalid_path(self):
        """Test cache directory validation with invalid path"""
        # Try to create cache in a non-writable location (like root on Unix systems)
        with patch('pathlib.Path.mkdir') as mock_mkdir:
            mock_mkdir.side_effect = OSError("Permission denied")
            
            with patch('pathlib.Path.touch') as mock_touch:
                mock_touch.side_effect = OSError("Permission denied")
                
                with pytest.raises(ValueError, match="Cannot write to cache directory"):
                    Settings(cache_dir="/root/cannot_write_here")
    
    def test_ttl_validation(self):
        """Test TTL validation"""
        # Test negative TTL
        with pytest.raises(ValueError, match="TTL must be positive"):
            Settings(default_ttl_hours=-1)
        
        # Test zero TTL
        with pytest.raises(ValueError, match="TTL must be positive"):
            Settings(default_ttl_hours=0)
        
        # Test excessive TTL
        with pytest.raises(ValueError, match="TTL cannot exceed 168 hours"):
            Settings(default_ttl_hours=200)
    
    def test_max_retries_validation(self):
        """Test max retries validation"""
        # Test negative retries
        with pytest.raises(ValueError, match="Max retries cannot be negative"):
            Settings(max_retries=-1)
        
        # Test excessive retries
        with pytest.raises(ValueError, match="Max retries should not exceed 10"):
            Settings(max_retries=15)
    
    def test_min_data_years_validation(self):
        """Test minimum data years validation"""
        # Test negative years
        with pytest.raises(ValueError, match="Minimum data years must be positive"):
            Settings(min_data_years=-1)
        
        # Test zero years
        with pytest.raises(ValueError, match="Minimum data years must be positive"):
            Settings(min_data_years=0)
        
        # Test excessive years
        with pytest.raises(ValueError, match="Minimum data years should not exceed 10"):
            Settings(min_data_years=15)
    
    def test_batch_size_validation(self):
        """Test batch size validation"""
        # Test negative batch size
        with pytest.raises(ValueError, match="Batch size must be positive"):
            Settings(batch_size=-1)
        
        # Test zero batch size
        with pytest.raises(ValueError, match="Batch size must be positive"):
            Settings(batch_size=0)
        
        # Test excessive batch size
        with pytest.raises(ValueError, match="Batch size should not exceed 500"):
            Settings(batch_size=1000)
    
    def test_sp500_csv_path_validation_nonexistent(self):
        """Test S&P 500 CSV path validation with non-existent file"""
        with pytest.raises(ValueError, match="S&P 500 CSV file not found"):
            Settings(sp500_csv_path="/nonexistent/file.csv")
    
    def test_sp500_csv_path_validation_exists(self):
        """Test S&P 500 CSV path validation with existing file"""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as temp_file:
            temp_file.write(b"ticker,name,sector\nAAPL,Apple Inc,Technology")
            temp_path = temp_file.name
        
        try:
            settings = Settings(sp500_csv_path=temp_path)
            assert settings.sp500_csv_path == temp_path
        finally:
            os.unlink(temp_path)
    
    def test_environment_check_methods(self):
        """Test environment check methods"""
        dev_settings = Settings(environment=Environment.DEVELOPMENT)
        test_settings = Settings(environment=Environment.TESTING)
        prod_settings = Settings(environment=Environment.PRODUCTION)
        
        assert dev_settings.is_development() is True
        assert dev_settings.is_testing() is False
        assert dev_settings.is_production() is False
        
        assert test_settings.is_development() is False
        assert test_settings.is_testing() is True
        assert test_settings.is_production() is False
        
        assert prod_settings.is_development() is False
        assert prod_settings.is_testing() is False
        assert prod_settings.is_production() is True
    
    def test_get_log_level(self):
        """Test log level conversion to numeric values"""
        import logging
        
        settings_debug = Settings(log_level=LogLevel.DEBUG)
        settings_info = Settings(log_level=LogLevel.INFO)
        settings_warning = Settings(log_level=LogLevel.WARNING)
        settings_error = Settings(log_level=LogLevel.ERROR)
        settings_critical = Settings(log_level=LogLevel.CRITICAL)
        
        assert settings_debug.get_log_level() == logging.DEBUG
        assert settings_info.get_log_level() == logging.INFO
        assert settings_warning.get_log_level() == logging.WARNING
        assert settings_error.get_log_level() == logging.ERROR
        assert settings_critical.get_log_level() == logging.CRITICAL
    
    @patch('logging.basicConfig')
    def test_configure_logging_development(self, mock_basic_config):
        """Test logging configuration for development"""
        settings = Settings(environment=Environment.DEVELOPMENT, log_level=LogLevel.DEBUG)
        settings.configure_logging()
        
        mock_basic_config.assert_called_once()
        call_args = mock_basic_config.call_args
        assert call_args[1]['level'] == settings.get_log_level()
        assert "filename" in call_args[1]['format']  # Development has more detailed format
    
    @patch('logging.basicConfig')
    def test_configure_logging_production(self, mock_basic_config):
        """Test logging configuration for production"""
        settings = Settings(environment=Environment.PRODUCTION, log_level=LogLevel.INFO)
        settings.configure_logging()
        
        mock_basic_config.assert_called_once()
        call_args = mock_basic_config.call_args
        assert call_args[1]['level'] == settings.get_log_level()
        assert "filename" not in call_args[1]['format']  # Production has simpler format


class TestEnvironmentSpecificSettings:
    """Test cases for environment-specific settings"""
    
    def test_development_settings(self):
        """Test development-specific settings"""
        settings = DevelopmentSettings()
        
        assert settings.environment == Environment.DEVELOPMENT
        assert settings.debug is True
        assert settings.log_level == LogLevel.DEBUG
        assert settings.default_ttl_hours == 1  # Shorter cache for development
        assert settings.max_retries == 3
    
    def test_testing_settings(self):
        """Test testing-specific settings"""
        settings = TestingSettings()
        
        assert settings.environment == Environment.TESTING
        assert settings.debug is True
        assert settings.log_level == LogLevel.WARNING
        assert settings.enable_cache is False  # Disabled for testing
        assert settings.max_retries == 1
        assert settings.validate_sp500_count is False
        assert settings.enable_metrics is False
    
    def test_production_settings(self):
        """Test production-specific settings"""
        settings = ProductionSettings()
        
        assert settings.environment == Environment.PRODUCTION
        assert settings.debug is False
        assert settings.log_level == LogLevel.INFO
        assert settings.default_ttl_hours == 24
        assert settings.max_retries == 5
        assert settings.enable_metrics is True
        assert settings.rate_limit_enabled is True


class TestGetSettings:
    """Test cases for the get_settings function"""
    
    @patch.dict(os.environ, {'STOCK_ENVIRONMENT': 'development'})
    @patch('backend.config.DevelopmentSettings')
    def test_get_settings_development(self, mock_dev_settings):
        """Test getting development settings from environment"""
        mock_instance = mock_dev_settings.return_value
        mock_instance.configure_logging = lambda: None
        
        result = get_settings()
        
        mock_dev_settings.assert_called_once()
        assert result == mock_instance
    
    @patch.dict(os.environ, {'STOCK_ENVIRONMENT': 'testing'})
    @patch('backend.config.TestingSettings')
    def test_get_settings_testing(self, mock_test_settings):
        """Test getting testing settings from environment"""
        mock_instance = mock_test_settings.return_value
        mock_instance.configure_logging = lambda: None
        
        result = get_settings()
        
        mock_test_settings.assert_called_once()
        assert result == mock_instance
    
    @patch.dict(os.environ, {'STOCK_ENVIRONMENT': 'production'})
    @patch('backend.config.ProductionSettings')
    def test_get_settings_production(self, mock_prod_settings):
        """Test getting production settings from environment"""
        mock_instance = mock_prod_settings.return_value
        mock_instance.configure_logging = lambda: None
        
        result = get_settings()
        
        mock_prod_settings.assert_called_once()
        assert result == mock_instance
    
    @patch.dict(os.environ, {}, clear=True)  # Clear environment
    @patch('backend.config.DevelopmentSettings')
    def test_get_settings_default(self, mock_dev_settings):
        """Test getting default (development) settings when no environment set"""
        mock_instance = mock_dev_settings.return_value
        mock_instance.configure_logging = lambda: None
        
        result = get_settings()
        
        mock_dev_settings.assert_called_once()
        assert result == mock_instance
    
    @patch.dict(os.environ, {'STOCK_ENVIRONMENT': 'invalid'})
    @patch('backend.config.DevelopmentSettings')
    def test_get_settings_invalid_environment(self, mock_dev_settings):
        """Test getting default settings when invalid environment specified"""
        mock_instance = mock_dev_settings.return_value
        mock_instance.configure_logging = lambda: None
        
        result = get_settings()
        
        mock_dev_settings.assert_called_once()
        assert result == mock_instance


class TestEnvironmentVariableSupport:
    """Test cases for environment variable support"""
    
    @patch.dict(os.environ, {
        'STOCK_CACHE_DIR': '/custom/cache',
        'STOCK_DEFAULT_TTL_HOURS': '48',
        'STOCK_ENABLE_CACHE': 'false',
        'STOCK_MAX_RETRIES': '10',
        'STOCK_LOG_LEVEL': 'ERROR'
    })
    def test_settings_from_environment_variables(self):
        """Test loading settings from environment variables"""
        temp_dir = tempfile.mkdtemp()
        try:
            with patch.dict(os.environ, {'STOCK_CACHE_DIR': temp_dir}):
                settings = Settings()
                
                assert settings.cache_dir == temp_dir
                assert settings.default_ttl_hours == 48
                assert settings.enable_cache is False
                assert settings.max_retries == 10
                assert settings.log_level == LogLevel.ERROR
        finally:
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)
    
    @patch.dict(os.environ, {
        'STOCK_BATCH_SIZE': '100',
        'STOCK_MAX_MEMORY_USAGE_MB': '2048',
        'STOCK_RATE_LIMIT_CALLS_PER_MINUTE': '600'
    })
    def test_performance_settings_from_environment(self):
        """Test performance-related settings from environment"""
        settings = Settings()
        
        assert settings.batch_size == 100
        assert settings.max_memory_usage_mb == 2048
        assert settings.rate_limit_calls_per_minute == 600


class TestCreateEnvFile:
    """Test cases for creating environment file"""
    
    def test_create_env_file(self):
        """Test creating sample environment file"""
        temp_file = tempfile.mktemp(suffix='.env')
        try:
            create_env_file(temp_file)
            
            assert Path(temp_file).exists()
            
            with open(temp_file, 'r') as f:
                content = f.read()
            
            # Check that key settings are present
            assert 'STOCK_ENVIRONMENT=' in content
            assert 'STOCK_CACHE_DIR=' in content
            assert 'STOCK_DEFAULT_TTL_HOURS=' in content
            assert 'STOCK_ENABLE_CACHE=' in content
            assert '# Stock Data Service Configuration' in content
        finally:
            if Path(temp_file).exists():
                os.unlink(temp_file)


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
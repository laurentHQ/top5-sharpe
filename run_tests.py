#!/usr/bin/env python3
"""
Test Runner for YFinance Adapter

Simple test runner that can be used without pytest installation.
Runs basic import and smoke tests to verify the implementation works.
"""

import sys
import traceback
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent))


def test_imports():
    """Test that all modules can be imported successfully"""
    print("Testing imports...")
    
    try:
        from backend import DataService, YFinanceAdapter, settings
        from backend.yfinance_adapter import CacheManager
        from backend.data_service import DataServiceConfig, StockDataResult
        from backend.config import Environment, LogLevel
        print("✓ All imports successful")
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        traceback.print_exc()
        return False


def test_basic_initialization():
    """Test basic component initialization"""
    print("Testing initialization...")
    
    try:
        from backend import DataService, DataServiceConfig
        import tempfile
        
        # Test config creation
        temp_dir = tempfile.mkdtemp()
        config = DataServiceConfig(cache_dir=temp_dir)
        print(f"✓ Config created: cache_dir={config.cache_dir}")
        
        # Test service creation
        service = DataService(config)
        print("✓ DataService initialized")
        
        # Test health check
        health = service.get_service_health()
        print(f"✓ Health check: {health['service_name']} is {health['status']}")
        
        # Cleanup
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)
        
        return True
    except Exception as e:
        print(f"✗ Initialization failed: {e}")
        traceback.print_exc()
        return False


def test_cache_manager():
    """Test cache manager functionality"""
    print("Testing cache manager...")
    
    try:
        from backend.yfinance_adapter import CacheManager
        import tempfile
        import pandas as pd
        
        temp_dir = tempfile.mkdtemp()
        cache_manager = CacheManager(cache_dir=temp_dir, default_ttl_hours=1)
        
        # Test cache operations
        tickers = ['TEST']
        period = '1y'
        test_data = pd.DataFrame({
            'Date': pd.date_range('2020-01-01', periods=5),
            'Close': [100.0, 101.0, 102.0, 103.0, 104.0],
            'Ticker': ['TEST'] * 5
        })
        
        # Should be cache miss initially
        cached_data = cache_manager.get(tickers, period)
        assert cached_data is None, "Expected cache miss"
        print("✓ Cache miss works")
        
        # Cache the data
        cache_manager.set(tickers, period, test_data)
        print("✓ Data cached")
        
        # Should be cache hit now
        cached_data = cache_manager.get(tickers, period)
        assert cached_data is not None, "Expected cache hit"
        assert len(cached_data) == 5, "Expected 5 rows of cached data"
        print("✓ Cache hit works")
        
        # Test stats
        stats = cache_manager.get_cache_stats()
        assert stats['cache_hits'] == 1, "Expected 1 cache hit"
        assert stats['cache_misses'] == 1, "Expected 1 cache miss"
        print(f"✓ Cache stats: {stats['hit_rate_percent']}% hit rate")
        
        # Cleanup
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)
        
        return True
    except Exception as e:
        print(f"✗ Cache manager test failed: {e}")
        traceback.print_exc()
        return False


def test_configuration():
    """Test configuration system"""
    print("Testing configuration...")
    
    try:
        from backend.config import Settings, Environment, LogLevel, get_settings
        
        # Test default settings
        settings = Settings()
        assert settings.environment == Environment.DEVELOPMENT
        assert settings.default_ttl_hours == 24
        print("✓ Default settings work")
        
        # Test custom settings
        custom_settings = Settings(
            environment=Environment.PRODUCTION,
            default_ttl_hours=12,
            enable_cache=False
        )
        assert custom_settings.environment == Environment.PRODUCTION
        assert custom_settings.default_ttl_hours == 12
        assert custom_settings.enable_cache is False
        print("✓ Custom settings work")
        
        # Test environment detection
        assert custom_settings.is_production() is True
        assert custom_settings.is_development() is False
        print("✓ Environment detection works")
        
        # Test log level conversion
        import logging
        debug_settings = Settings(log_level=LogLevel.DEBUG)
        assert debug_settings.get_log_level() == logging.DEBUG
        print("✓ Log level conversion works")
        
        return True
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("YFinance Adapter Test Runner")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_basic_initialization,
        test_cache_manager,
        test_configuration
    ]
    
    passed = 0
    total = len(tests)
    
    for test_func in tests:
        print(f"\n--- {test_func.__name__} ---")
        try:
            if test_func():
                passed += 1
                print("✓ PASSED")
            else:
                print("✗ FAILED")
        except Exception as e:
            print(f"✗ FAILED with exception: {e}")
    
    print("\n" + "=" * 40)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
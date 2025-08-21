#!/usr/bin/env python3
"""
Demo script for YFinance Adapter

This script demonstrates the yfinance adapter functionality including:
- Data fetching with retry logic
- Caching with TTL
- Data quality validation
- Performance monitoring

Run with: python demo_adapter.py
"""

import logging
import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent))

from backend import DataService, DataServiceConfig

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def demo_basic_functionality():
    """Demonstrate basic adapter functionality"""
    logger.info("=== Demo: Basic Functionality ===")
    
    # Create service with development settings
    config = DataServiceConfig(
        cache_dir="demo_cache",
        default_ttl_hours=1,
        enable_cache=True,
        min_data_points=100,  # Lower for demo
        min_data_years=1.0    # Lower for demo
    )
    
    service = DataService(config)
    
    # Test individual stock
    logger.info("Fetching data for AAPL...")
    result = service.get_stock_data(['AAPL'], period='6mo', validate_quality=True)
    
    if result.success:
        logger.info(f"✓ Successfully fetched {len(result.data)} data points")
        logger.info(f"✓ Cache hit: {result.cache_hit}")
        logger.info(f"✓ Fetch duration: {result.fetch_duration_seconds:.2f}s")
        
        if result.quality_results:
            quality = result.quality_results[0]
            logger.info(f"✓ Data quality - Valid: {quality.is_valid}, Points: {quality.data_points}")
            if quality.issues:
                logger.warning(f"⚠ Quality issues: {', '.join(quality.issues)}")
    else:
        logger.error(f"✗ Failed to fetch data: {result.failed_tickers}")
    
    return service


def demo_caching():
    """Demonstrate caching functionality"""
    logger.info("\n=== Demo: Caching ===")
    
    config = DataServiceConfig(cache_dir="demo_cache", default_ttl_hours=1)
    service = DataService(config)
    
    # First call (should miss cache)
    logger.info("First call (cache miss expected)...")
    result1 = service.get_stock_data(['MSFT'], period='3mo')
    
    if result1.success:
        logger.info(f"✓ First call: {result1.cache_hit=}, Duration: {result1.fetch_duration_seconds:.2f}s")
    
    # Second call (should hit cache)
    logger.info("Second call (cache hit expected)...")
    result2 = service.get_stock_data(['MSFT'], period='3mo')
    
    if result2.success:
        logger.info(f"✓ Second call: {result2.cache_hit=}, Duration: {result2.fetch_duration_seconds:.2f}s")
    
    # Show cache statistics
    stats = service.adapter.get_adapter_stats()
    logger.info(f"✓ Cache stats: {stats.get('hit_rate_percent', 0)}% hit rate")


def demo_batch_processing():
    """Demonstrate batch processing"""
    logger.info("\n=== Demo: Batch Processing ===")
    
    config = DataServiceConfig(cache_dir="demo_cache")
    service = DataService(config)
    
    # Test multiple stocks
    tickers = ['AAPL', 'MSFT', 'GOOGL']
    logger.info(f"Fetching data for {len(tickers)} tickers: {', '.join(tickers)}")
    
    result = service.get_stock_data(tickers, period='1mo')
    
    if result.success:
        successful = len(set(result.data['Ticker'].unique())) if result.data is not None else 0
        logger.info(f"✓ Successfully fetched data for {successful}/{len(tickers)} tickers")
        logger.info(f"✓ Total data points: {len(result.data) if result.data is not None else 0}")
        
        if result.failed_tickers:
            logger.warning(f"⚠ Failed tickers: {', '.join(result.failed_tickers)}")
    else:
        logger.error("✗ Batch processing failed")


def demo_service_health():
    """Demonstrate service health monitoring"""
    logger.info("\n=== Demo: Service Health ===")
    
    config = DataServiceConfig(cache_dir="demo_cache")
    service = DataService(config)
    
    health = service.get_service_health()
    
    logger.info(f"✓ Service: {health['service_name']}")
    logger.info(f"✓ Status: {health['status']}")
    logger.info(f"✓ API calls: {health['api_calls']}")
    logger.info(f"✓ Success rate: {health['success_rate_percent']}%")
    
    if 'sp500_loaded' in health:
        logger.info(f"✓ S&P 500 loaded: {health['sp500_loaded']}")
        if health.get('sp500_ticker_count'):
            logger.info(f"✓ S&P 500 tickers: {health['sp500_ticker_count']}")


def demo_error_handling():
    """Demonstrate error handling"""
    logger.info("\n=== Demo: Error Handling ===")
    
    config = DataServiceConfig(cache_dir="demo_cache", max_retries=2)
    service = DataService(config)
    
    # Test with invalid ticker
    logger.info("Testing invalid ticker...")
    result = service.get_stock_data(['INVALID_TICKER_XYZ123'], period='1mo')
    
    if not result.success:
        logger.info(f"✓ Correctly handled invalid ticker: {result.failed_tickers}")
    
    # Test with mix of valid and invalid
    logger.info("Testing mixed valid/invalid tickers...")
    result = service.get_stock_data(['AAPL', 'INVALID123', 'MSFT'], period='1mo')
    
    if result.success:
        successful = len(set(result.data['Ticker'].unique())) if result.data is not None else 0
        logger.info(f"✓ Partial success: {successful} valid, {len(result.failed_tickers)} failed")
    elif result.failed_tickers:
        logger.info(f"✓ All failed as expected: {result.failed_tickers}")


def main():
    """Run all demos"""
    logger.info("Starting YFinance Adapter Demo")
    logger.info("=" * 50)
    
    try:
        # Run demos
        service = demo_basic_functionality()
        demo_caching()
        demo_batch_processing()
        demo_service_health()
        demo_error_handling()
        
        # Cleanup
        logger.info("\n=== Cleanup ===")
        logger.info("Cleaning up cache...")
        service.clear_cache()
        logger.info("✓ Cache cleared")
        
    except KeyboardInterrupt:
        logger.info("\nDemo interrupted by user")
    except Exception as e:
        logger.error(f"Demo failed with error: {e}")
        raise
    
    logger.info("\n" + "=" * 50)
    logger.info("Demo completed!")


if __name__ == "__main__":
    main()
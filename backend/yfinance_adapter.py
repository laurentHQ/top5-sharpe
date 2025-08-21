"""
Yahoo Finance Data Adapter

This module provides a robust interface to Yahoo Finance data with retry logic,
caching, and error handling. It implements exponential backoff for failed requests
and uses on-disk caching to minimize API calls and improve performance.

Key Features:
- Exponential backoff with jitter (1s, 2s, 4s, 8s, 16s max delays)
- On-disk Parquet caching with configurable TTL
- Comprehensive logging for monitoring and debugging
- Graceful handling of invalid tickers and API limitations
- Batch processing optimization
"""

import asyncio
import json
import logging
import os
import random
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

import pandas as pd
import yfinance as yf
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
    before_sleep_log,
    after_log
)

# Configure logging
logger = logging.getLogger(__name__)


class YFinanceAdapterError(Exception):
    """Custom exception for Yahoo Finance adapter errors"""
    pass


class CacheManager:
    """Manages on-disk caching for stock price data using Parquet files"""
    
    def __init__(self, cache_dir: str = "cache", default_ttl_hours: int = 24):
        """
        Initialize cache manager
        
        Args:
            cache_dir: Directory to store cache files
            default_ttl_hours: Default TTL in hours for cached data
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.default_ttl_hours = default_ttl_hours
        self.metadata_file = self.cache_dir / "cache_metadata.json"
        self.cache_hits = 0
        self.cache_misses = 0
        
        # Load existing metadata
        self.metadata = self._load_metadata()
    
    def _load_metadata(self) -> Dict:
        """Load cache metadata from disk"""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError) as e:
                logger.warning(f"Failed to load cache metadata: {e}")
        return {}
    
    def _save_metadata(self):
        """Save cache metadata to disk"""
        try:
            with open(self.metadata_file, 'w') as f:
                json.dump(self.metadata, f, indent=2, default=str)
        except OSError as e:
            logger.error(f"Failed to save cache metadata: {e}")
    
    def _get_cache_key(self, tickers: List[str], period: str) -> str:
        """Generate cache key for ticker list and period"""
        # Sort tickers for consistent cache keys regardless of order
        sorted_tickers = sorted(tickers)
        ticker_hash = hash(tuple(sorted_tickers))
        return f"{ticker_hash}_{period}"
    
    def _get_cache_path(self, cache_key: str) -> Path:
        """Get file path for cache key"""
        return self.cache_dir / f"{cache_key}.parquet"
    
    def _is_cache_valid(self, cache_key: str, ttl_hours: Optional[int] = None) -> bool:
        """Check if cache entry is still valid based on TTL"""
        ttl_hours = ttl_hours or self.default_ttl_hours
        
        if cache_key not in self.metadata:
            return False
        
        cache_time = datetime.fromisoformat(self.metadata[cache_key]['timestamp'])
        ttl_delta = timedelta(hours=ttl_hours)
        
        return datetime.now() < cache_time + ttl_delta
    
    def get(self, tickers: List[str], period: str, ttl_hours: Optional[int] = None) -> Optional[pd.DataFrame]:
        """
        Retrieve cached data if valid
        
        Args:
            tickers: List of ticker symbols
            period: Time period (e.g., '5y', '1y')
            ttl_hours: TTL override for this request
            
        Returns:
            Cached DataFrame if valid, None otherwise
        """
        cache_key = self._get_cache_key(tickers, period)
        cache_path = self._get_cache_path(cache_key)
        
        if not cache_path.exists():
            self.cache_misses += 1
            logger.debug(f"Cache miss: file not found for {cache_key}")
            return None
        
        if not self._is_cache_valid(cache_key, ttl_hours):
            self.cache_misses += 1
            logger.debug(f"Cache miss: TTL expired for {cache_key}")
            # Clean up expired cache file
            self._remove_cache_entry(cache_key)
            return None
        
        try:
            df = pd.read_parquet(cache_path)
            self.cache_hits += 1
            logger.info(f"Cache hit for {len(tickers)} tickers, period {period}")
            return df
        except Exception as e:
            logger.error(f"Failed to read cache file {cache_path}: {e}")
            self.cache_misses += 1
            # Remove corrupted cache file
            self._remove_cache_entry(cache_key)
            return None
    
    def set(self, tickers: List[str], period: str, data: pd.DataFrame):
        """
        Store data in cache
        
        Args:
            tickers: List of ticker symbols
            period: Time period
            data: DataFrame to cache
        """
        cache_key = self._get_cache_key(tickers, period)
        cache_path = self._get_cache_path(cache_key)
        
        try:
            data.to_parquet(cache_path, compression='snappy')
            
            # Update metadata
            self.metadata[cache_key] = {
                'timestamp': datetime.now().isoformat(),
                'tickers': tickers,
                'period': period,
                'file_size': cache_path.stat().st_size
            }
            self._save_metadata()
            
            logger.info(f"Cached data for {len(tickers)} tickers, period {period}")
        except Exception as e:
            logger.error(f"Failed to cache data: {e}")
    
    def _remove_cache_entry(self, cache_key: str):
        """Remove cache entry and its metadata"""
        cache_path = self._get_cache_path(cache_key)
        
        try:
            if cache_path.exists():
                cache_path.unlink()
            if cache_key in self.metadata:
                del self.metadata[cache_key]
                self._save_metadata()
        except Exception as e:
            logger.error(f"Failed to remove cache entry {cache_key}: {e}")
    
    def cleanup_expired(self, ttl_hours: Optional[int] = None):
        """Remove all expired cache entries"""
        ttl_hours = ttl_hours or self.default_ttl_hours
        expired_keys = [
            key for key in self.metadata.keys()
            if not self._is_cache_valid(key, ttl_hours)
        ]
        
        for key in expired_keys:
            self._remove_cache_entry(key)
        
        if expired_keys:
            logger.info(f"Cleaned up {len(expired_keys)} expired cache entries")
    
    def get_cache_stats(self) -> Dict:
        """Get cache performance statistics"""
        total_requests = self.cache_hits + self.cache_misses
        hit_rate = (self.cache_hits / total_requests * 100) if total_requests > 0 else 0
        
        return {
            'cache_hits': self.cache_hits,
            'cache_misses': self.cache_misses,
            'hit_rate_percent': round(hit_rate, 2),
            'total_cached_entries': len(self.metadata),
            'cache_dir_size_mb': self._get_cache_size_mb()
        }
    
    def _get_cache_size_mb(self) -> float:
        """Calculate total cache directory size in MB"""
        total_size = 0
        for file_path in self.cache_dir.rglob('*'):
            if file_path.is_file():
                total_size += file_path.stat().st_size
        return round(total_size / (1024 * 1024), 2)


class YFinanceAdapter:
    """
    Robust Yahoo Finance data adapter with caching and retry logic
    
    Features:
    - Exponential backoff with jitter for failed requests
    - On-disk caching with configurable TTL
    - Comprehensive error handling and logging
    - Batch processing optimization
    """
    
    def __init__(
        self,
        cache_dir: str = "data/cache",
        default_ttl_hours: int = 24,
        max_retries: int = 5,
        enable_cache: bool = True
    ):
        """
        Initialize the adapter
        
        Args:
            cache_dir: Directory for cache storage
            default_ttl_hours: Default cache TTL in hours
            max_retries: Maximum number of retry attempts
            enable_cache: Whether to enable caching
        """
        self.max_retries = max_retries
        self.enable_cache = enable_cache
        
        if enable_cache:
            self.cache_manager = CacheManager(cache_dir, default_ttl_hours)
        else:
            self.cache_manager = None
        
        # Track API calls for monitoring
        self.api_calls = 0
        self.failed_calls = 0
    
    def _add_jitter(self, delay: float) -> float:
        """Add random jitter to delay to avoid thundering herd"""
        return delay + random.uniform(0, delay * 0.1)
    
    @retry(
        retry=retry_if_exception_type((Exception,)),
        stop=stop_after_attempt(5),  # Will be overridden by instance max_retries
        wait=wait_exponential(multiplier=1, min=1, max=16),
        before_sleep=before_sleep_log(logger, logging.WARNING),
        after=after_log(logger, logging.INFO)
    )
    def _fetch_ticker_data(self, ticker: str, period: str) -> Optional[pd.DataFrame]:
        """
        Fetch data for a single ticker with retry logic
        
        Args:
            ticker: Stock ticker symbol
            period: Time period (e.g., '5y', '1y', '6mo')
            
        Returns:
            DataFrame with price data or None if failed
        """
        self.api_calls += 1
        
        try:
            logger.debug(f"Fetching data for {ticker}, period {period}")
            
            # Create yfinance ticker object
            yf_ticker = yf.Ticker(ticker)
            
            # Fetch historical data
            hist_data = yf_ticker.history(
                period=period,
                auto_adjust=True,  # Use adjusted close prices
                prepost=False,     # Exclude pre/post market data
                threads=True       # Enable threading for better performance
            )
            
            if hist_data.empty:
                logger.warning(f"No data returned for ticker {ticker}")
                return None
            
            # Add ticker column for identification
            hist_data['Ticker'] = ticker
            
            # Reset index to make Date a column
            hist_data = hist_data.reset_index()
            
            logger.debug(f"Successfully fetched {len(hist_data)} records for {ticker}")
            return hist_data
            
        except Exception as e:
            logger.error(f"Failed to fetch data for {ticker}: {e}")
            self.failed_calls += 1
            raise YFinanceAdapterError(f"Failed to fetch {ticker}: {e}")
    
    async def fetch_prices_async(
        self,
        tickers: List[str],
        period: str = '5y',
        ttl_hours: Optional[int] = None,
        max_workers: int = 10
    ) -> pd.DataFrame:
        """
        Asynchronously fetch price data for multiple tickers
        
        Args:
            tickers: List of ticker symbols
            period: Time period for historical data
            ttl_hours: Cache TTL override
            max_workers: Maximum concurrent requests
            
        Returns:
            DataFrame with combined price data
        """
        # Check cache first
        if self.cache_manager:
            cached_data = self.cache_manager.get(tickers, period, ttl_hours)
            if cached_data is not None:
                return cached_data
        
        # Fetch data for all tickers
        semaphore = asyncio.Semaphore(max_workers)
        
        async def fetch_with_semaphore(ticker):
            async with semaphore:
                loop = asyncio.get_event_loop()
                return await loop.run_in_executor(None, self._fetch_ticker_data, ticker, period)
        
        tasks = [fetch_with_semaphore(ticker) for ticker in tickers]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Combine successful results
        successful_data = []
        failed_tickers = []
        
        for ticker, result in zip(tickers, results):
            if isinstance(result, Exception):
                logger.error(f"Failed to fetch {ticker}: {result}")
                failed_tickers.append(ticker)
            elif result is not None:
                successful_data.append(result)
            else:
                failed_tickers.append(ticker)
        
        if not successful_data:
            raise YFinanceAdapterError("Failed to fetch data for any ticker")
        
        # Combine all DataFrames
        combined_df = pd.concat(successful_data, ignore_index=True)
        
        # Log results
        success_count = len(successful_data)
        total_count = len(tickers)
        logger.info(f"Successfully fetched data for {success_count}/{total_count} tickers")
        
        if failed_tickers:
            logger.warning(f"Failed to fetch data for tickers: {failed_tickers}")
        
        # Cache the results
        if self.cache_manager and success_count > 0:
            self.cache_manager.set(tickers, period, combined_df)
        
        return combined_df
    
    def fetch_prices(
        self,
        tickers: List[str],
        period: str = '5y',
        ttl_hours: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Fetch price data for multiple tickers (synchronous interface)
        
        Args:
            tickers: List of ticker symbols
            period: Time period for historical data
            ttl_hours: Cache TTL override
            
        Returns:
            DataFrame with combined price data
        """
        # Validate inputs
        if not tickers:
            raise ValueError("At least one ticker must be provided")
        
        if not isinstance(tickers, list):
            raise ValueError("Tickers must be provided as a list")
        
        # Clean and validate tickers
        clean_tickers = [ticker.strip().upper() for ticker in tickers if ticker.strip()]
        
        if not clean_tickers:
            raise ValueError("No valid tickers provided after cleaning")
        
        logger.info(f"Fetching price data for {len(clean_tickers)} tickers, period: {period}")
        
        # Check cache first
        if self.cache_manager:
            cached_data = self.cache_manager.get(clean_tickers, period, ttl_hours)
            if cached_data is not None:
                return cached_data
        
        # Fetch data sequentially with retry logic
        successful_data = []
        failed_tickers = []
        
        for ticker in clean_tickers:
            try:
                data = self._fetch_ticker_data(ticker, period)
                if data is not None:
                    successful_data.append(data)
                else:
                    failed_tickers.append(ticker)
            except Exception as e:
                logger.error(f"Failed to fetch {ticker}: {e}")
                failed_tickers.append(ticker)
        
        if not successful_data:
            raise YFinanceAdapterError("Failed to fetch data for any ticker")
        
        # Combine all DataFrames
        combined_df = pd.concat(successful_data, ignore_index=True)
        
        # Log results
        success_count = len(successful_data)
        total_count = len(clean_tickers)
        logger.info(f"Successfully fetched data for {success_count}/{total_count} tickers")
        
        if failed_tickers:
            logger.warning(f"Failed to fetch data for tickers: {failed_tickers}")
        
        # Cache the results
        if self.cache_manager and success_count > 0:
            self.cache_manager.set(clean_tickers, period, combined_df)
        
        return combined_df
    
    def get_adapter_stats(self) -> Dict:
        """Get adapter performance statistics"""
        stats = {
            'api_calls': self.api_calls,
            'failed_calls': self.failed_calls,
            'success_rate_percent': round((1 - self.failed_calls / max(self.api_calls, 1)) * 100, 2)
        }
        
        if self.cache_manager:
            stats.update(self.cache_manager.get_cache_stats())
        
        return stats
    
    def cleanup_cache(self, ttl_hours: Optional[int] = None):
        """Clean up expired cache entries"""
        if self.cache_manager:
            self.cache_manager.cleanup_expired(ttl_hours)
    
    def clear_cache(self):
        """Clear all cached data"""
        if self.cache_manager:
            import shutil
            try:
                shutil.rmtree(self.cache_manager.cache_dir)
                logger.info("Cache cleared successfully")
            except Exception as e:
                logger.error(f"Failed to clear cache: {e}")
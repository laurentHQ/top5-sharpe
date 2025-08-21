"""
Data Service Layer

This module provides a high-level service interface for stock data operations,
wrapping the YFinance adapter and providing additional business logic, validation,
and monitoring capabilities.

Features:
- Stock data retrieval with automatic caching
- Data validation and quality checks
- Health monitoring and statistics
- Configuration management
- Integration with S&P 500 universe
"""

import logging
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pandas as pd
from pydantic import BaseModel, Field, field_validator

from .yfinance_adapter import YFinanceAdapter, YFinanceAdapterError

# Add parent directory to path to import data modules
import sys
sys.path.append(str(Path(__file__).parent.parent))
from data.sp500_loader import SP500Loader, get_sp500_tickers

# Configure logging
logger = logging.getLogger(__name__)


class DataServiceConfig(BaseModel):
    """Configuration for the data service"""
    
    # Cache settings
    cache_dir: str = Field(default="data/cache", description="Cache directory path")
    default_ttl_hours: int = Field(default=24, description="Default cache TTL in hours")
    enable_cache: bool = Field(default=True, description="Enable caching")
    
    # API settings
    max_retries: int = Field(default=5, description="Maximum retry attempts")
    request_timeout: int = Field(default=30, description="Request timeout in seconds")
    max_concurrent_requests: int = Field(default=10, description="Maximum concurrent API requests")
    
    # Data validation settings
    min_data_points: int = Field(default=252, description="Minimum data points required (1 year)")
    min_data_years: float = Field(default=3.0, description="Minimum years of data required")
    
    # S&P 500 settings
    sp500_csv_path: Optional[str] = Field(default=None, description="Custom S&P 500 CSV path")
    validate_sp500_count: bool = Field(default=True, description="Validate S&P 500 stock count")
    
    @field_validator('cache_dir')
    def validate_cache_dir(cls, v):
        """Ensure cache directory is valid"""
        if v:
            Path(v).mkdir(parents=True, exist_ok=True)
        return v
    
    @field_validator('default_ttl_hours')
    def validate_ttl(cls, v):
        """Validate TTL is reasonable"""
        if v <= 0 or v > 168:  # Max 1 week
            raise ValueError("TTL must be between 1 and 168 hours")
        return v


class DataQualityResult(BaseModel):
    """Result of data quality validation"""
    
    ticker: str
    is_valid: bool
    data_points: int
    date_range_days: int
    date_range_years: float
    first_date: datetime
    last_date: datetime
    issues: List[str] = []


class StockDataResult(BaseModel):
    """Result container for stock data operations"""
    
    success: bool
    data: Optional[pd.DataFrame] = None
    failed_tickers: List[str] = []
    quality_results: List[DataQualityResult] = []
    cache_hit: bool = False
    fetch_duration_seconds: float = 0.0
    
    class Config:
        arbitrary_types_allowed = True


class DataService:
    """
    High-level data service for stock price operations
    
    Provides business logic layer on top of the YFinance adapter with
    validation, monitoring, and integration with S&P 500 universe.
    """
    
    def __init__(self, config: Optional[DataServiceConfig] = None):
        """
        Initialize data service
        
        Args:
            config: Service configuration, uses defaults if not provided
        """
        self.config = config or DataServiceConfig()
        
        # Initialize adapter
        self.adapter = YFinanceAdapter(
            cache_dir=self.config.cache_dir,
            default_ttl_hours=self.config.default_ttl_hours,
            max_retries=self.config.max_retries,
            enable_cache=self.config.enable_cache
        )
        
        # Initialize S&P 500 loader
        self.sp500_loader = SP500Loader(
            csv_path=self.config.sp500_csv_path,
            validate_count=self.config.validate_sp500_count
        )
        
        logger.info("Data service initialized with config: %s", self.config.dict())
    
    def get_stock_data(
        self,
        tickers: List[str],
        period: str = '5y',
        validate_quality: bool = True,
        ttl_hours: Optional[int] = None
    ) -> StockDataResult:
        """
        Get stock price data with validation and quality checks
        
        Args:
            tickers: List of ticker symbols
            period: Time period (e.g., '5y', '1y')
            validate_quality: Whether to perform data quality validation
            ttl_hours: Cache TTL override
            
        Returns:
            StockDataResult with data and metadata
        """
        start_time = datetime.now()
        
        try:
            logger.info(f"Fetching stock data for {len(tickers)} tickers, period: {period}")
            
            # Check if we have cached data
            cache_hit = False
            if self.adapter.cache_manager:
                cached_data = self.adapter.cache_manager.get(tickers, period, ttl_hours)
                if cached_data is not None:
                    cache_hit = True
            
            # Fetch data through adapter
            data = self.adapter.fetch_prices(tickers, period, ttl_hours)
            
            # Determine which tickers failed
            successful_tickers = data['Ticker'].unique().tolist() if not data.empty else []
            failed_tickers = [t for t in tickers if t not in successful_tickers]
            
            # Perform data quality validation if requested
            quality_results = []
            if validate_quality and not data.empty:
                quality_results = self._validate_data_quality(data)
            
            duration = (datetime.now() - start_time).total_seconds()
            
            result = StockDataResult(
                success=not data.empty,
                data=data if not data.empty else None,
                failed_tickers=failed_tickers,
                quality_results=quality_results,
                cache_hit=cache_hit,
                fetch_duration_seconds=duration
            )
            
            logger.info(
                f"Data fetch completed: {len(successful_tickers)} successful, "
                f"{len(failed_tickers)} failed, duration: {duration:.2f}s, "
                f"cache_hit: {cache_hit}"
            )
            
            return result
            
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            logger.error(f"Data fetch failed after {duration:.2f}s: {e}")
            
            return StockDataResult(
                success=False,
                failed_tickers=tickers,
                fetch_duration_seconds=duration
            )
    
    def _validate_data_quality(self, data: pd.DataFrame) -> List[DataQualityResult]:
        """
        Validate data quality for each ticker
        
        Args:
            data: DataFrame with stock price data
            
        Returns:
            List of data quality results
        """
        results = []
        
        for ticker in data['Ticker'].unique():
            ticker_data = data[data['Ticker'] == ticker].copy()
            
            # Calculate metrics
            data_points = len(ticker_data)
            if data_points == 0:
                continue
                
            first_date = ticker_data['Date'].min()
            last_date = ticker_data['Date'].max()
            date_range_days = (last_date - first_date).days
            date_range_years = date_range_days / 365.25
            
            # Validate quality
            issues = []
            is_valid = True
            
            # Check minimum data points
            if data_points < self.config.min_data_points:
                issues.append(f"Insufficient data points: {data_points} < {self.config.min_data_points}")
                is_valid = False
            
            # Check minimum years of data
            if date_range_years < self.config.min_data_years:
                issues.append(f"Insufficient data years: {date_range_years:.2f} < {self.config.min_data_years}")
                is_valid = False
            
            # Check for missing values in critical columns
            critical_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            for col in critical_columns:
                if col in ticker_data.columns:
                    null_count = ticker_data[col].isnull().sum()
                    if null_count > 0:
                        issues.append(f"Missing values in {col}: {null_count}")
                        if null_count > data_points * 0.05:  # > 5% missing
                            is_valid = False
            
            # Check for unrealistic price movements (>50% single day change)
            if 'Close' in ticker_data.columns:
                returns = ticker_data['Close'].pct_change().abs()
                extreme_moves = (returns > 0.5).sum()
                if extreme_moves > 0:
                    issues.append(f"Extreme price movements detected: {extreme_moves}")
                    if extreme_moves > 5:  # More than 5 extreme moves
                        is_valid = False
            
            result = DataQualityResult(
                ticker=ticker,
                is_valid=is_valid,
                data_points=data_points,
                date_range_days=date_range_days,
                date_range_years=date_range_years,
                first_date=first_date,
                last_date=last_date,
                issues=issues
            )
            
            results.append(result)
            
            if issues:
                level = logging.WARNING if is_valid else logging.ERROR
                logger.log(level, f"Data quality issues for {ticker}: {', '.join(issues)}")
        
        return results
    
    def get_sp500_data(
        self,
        period: str = '5y',
        validate_quality: bool = True,
        ttl_hours: Optional[int] = None,
        max_tickers: Optional[int] = None
    ) -> StockDataResult:
        """
        Get stock data for all S&P 500 tickers
        
        Args:
            period: Time period for data
            validate_quality: Whether to perform data quality validation
            ttl_hours: Cache TTL override
            max_tickers: Limit number of tickers (for testing/dev)
            
        Returns:
            StockDataResult with S&P 500 data
        """
        try:
            # Get S&P 500 tickers
            tickers = self.sp500_loader.get_tickers()
            
            if max_tickers:
                tickers = tickers[:max_tickers]
            
            logger.info(f"Fetching S&P 500 data for {len(tickers)} tickers")
            
            # Use the standard get_stock_data method
            return self.get_stock_data(tickers, period, validate_quality, ttl_hours)
            
        except Exception as e:
            logger.error(f"Failed to fetch S&P 500 data: {e}")
            return StockDataResult(
                success=False,
                failed_tickers=[],
                fetch_duration_seconds=0.0
            )
    
    def get_service_health(self) -> Dict:
        """
        Get service health and statistics
        
        Returns:
            Dictionary with service health information
        """
        adapter_stats = self.adapter.get_adapter_stats()
        
        # Get cache directory size and file count
        cache_info = {}
        if self.adapter.cache_manager:
            cache_dir = Path(self.adapter.cache_manager.cache_dir)
            if cache_dir.exists():
                cache_files = list(cache_dir.glob('*.parquet'))
                cache_info = {
                    'cache_files_count': len(cache_files),
                    'cache_dir_exists': True,
                    'cache_dir_path': str(cache_dir)
                }
            else:
                cache_info = {
                    'cache_files_count': 0,
                    'cache_dir_exists': False,
                    'cache_dir_path': str(cache_dir)
                }
        
        # Get S&P 500 loader status
        sp500_status = {}
        try:
            tickers = self.sp500_loader.get_tickers()
            sp500_status = {
                'sp500_loaded': True,
                'sp500_ticker_count': len(tickers),
                'sp500_csv_path': str(self.sp500_loader.csv_path)
            }
        except Exception as e:
            sp500_status = {
                'sp500_loaded': False,
                'sp500_error': str(e),
                'sp500_csv_path': str(self.sp500_loader.csv_path)
            }
        
        health = {
            'service_name': 'DataService',
            'timestamp': datetime.now().isoformat(),
            'status': 'healthy',
            'config': self.config.dict(),
            **adapter_stats,
            **cache_info,
            **sp500_status
        }
        
        return health
    
    def cleanup_cache(self, ttl_hours: Optional[int] = None):
        """Clean up expired cache entries"""
        self.adapter.cleanup_cache(ttl_hours)
    
    def clear_cache(self):
        """Clear all cached data"""
        self.adapter.clear_cache()
    
    @classmethod
    def from_env(cls) -> 'DataService':
        """
        Create DataService instance from environment variables
        
        Environment variables:
        - DATA_CACHE_DIR: Cache directory path
        - DATA_TTL_HOURS: Default TTL in hours  
        - DATA_ENABLE_CACHE: Enable caching (true/false)
        - DATA_MAX_RETRIES: Maximum retry attempts
        - DATA_MIN_DATA_POINTS: Minimum data points required
        - DATA_MIN_DATA_YEARS: Minimum years of data required
        - SP500_CSV_PATH: Custom S&P 500 CSV path
        
        Returns:
            Configured DataService instance
        """
        config = DataServiceConfig(
            cache_dir=os.getenv('DATA_CACHE_DIR', 'data/cache'),
            default_ttl_hours=int(os.getenv('DATA_TTL_HOURS', '24')),
            enable_cache=os.getenv('DATA_ENABLE_CACHE', 'true').lower() == 'true',
            max_retries=int(os.getenv('DATA_MAX_RETRIES', '5')),
            min_data_points=int(os.getenv('DATA_MIN_DATA_POINTS', '252')),
            min_data_years=float(os.getenv('DATA_MIN_DATA_YEARS', '3.0')),
            sp500_csv_path=os.getenv('SP500_CSV_PATH')
        )
        
        return cls(config)
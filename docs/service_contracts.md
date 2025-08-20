# Service Contracts & Interface Specifications

## Overview

This document defines the precise interface contracts between the adapter, Sharpe utilities, and API services for the Top 5 Sharpe Ratio application.

## Service Interface Hierarchy

```
API Services (FastAPI)
    ↓ uses
Business Logic Services (StockRanker, PerformanceAnalyzer)
    ↓ uses  
Data Services (YahooFinanceAdapter, DataCache, SharpeCalculator)
    ↓ uses
Foundation Services (SP500Loader)
```

## 1. YahooFinanceAdapter Interface

### Contract Definition
```python
from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from dataclasses import dataclass
from datetime import datetime

class PriceDataSource(ABC):
    """Abstract interface for price data providers."""
    
    @abstractmethod
    async def fetch_price_data(
        self, 
        ticker: str, 
        period: str = "5y"
    ) -> PriceData:
        """Fetch historical price data for a single ticker."""
        pass
    
    @abstractmethod
    async def fetch_bulk_data(
        self, 
        tickers: List[str], 
        period: str = "5y"
    ) -> Dict[str, PriceData]:
        """Fetch price data for multiple tickers concurrently."""
        pass
    
    @abstractmethod
    def get_health_status(self) -> ServiceHealth:
        """Return current service health and connectivity."""
        pass

@dataclass
class PriceData:
    """Price data structure returned by adapters."""
    ticker: str
    dates: List[datetime]
    close_prices: List[float]
    adjusted_close: List[float]
    volume: List[int]
    data_quality: float  # 0.0-1.0 completeness score
    fetch_timestamp: datetime
    source: str  # "yahoo", "alpha_vantage", etc.

@dataclass
class ServiceHealth:
    """Service health status."""
    is_healthy: bool
    last_successful_call: Optional[datetime]
    error_rate: float  # 0.0-1.0
    average_response_time: float  # milliseconds
    rate_limit_remaining: Optional[int]
```

### Implementation Contract
```python
class YahooFinanceAdapter(PriceDataSource):
    """Yahoo Finance implementation of price data interface."""
    
    def __init__(self, config: AdapterConfig):
        self.session = aiohttp.ClientSession()
        self.retry_config = config.retry_config
        self.circuit_breaker = CircuitBreaker(
            failure_threshold=config.failure_threshold,
            recovery_timeout=config.recovery_timeout
        )
    
    async def fetch_price_data(self, ticker: str, period: str = "5y") -> PriceData:
        """
        Fetch price data with retry logic and circuit breaker.
        
        Args:
            ticker: Stock symbol (e.g., 'AAPL')
            period: Time period ('1y', '2y', '5y', '10y')
            
        Returns:
            PriceData with quality score and metadata
            
        Raises:
            DataSourceError: When data cannot be retrieved
            ValidationError: When ticker format is invalid
        """
        # Implementation with error handling and retries
        pass
    
    async def fetch_bulk_data(
        self, 
        tickers: List[str], 
        period: str = "5y"
    ) -> Dict[str, PriceData]:
        """
        Concurrent fetch with rate limiting.
        
        Args:
            tickers: List of stock symbols
            period: Time period for all symbols
            
        Returns:
            Dict mapping ticker -> PriceData
            Failed fetches omitted from result
        """
        # Implementation with semaphore for rate limiting
        pass
```

## 2. SharpeCalculator Interface

### Contract Definition
```python
from typing import List, Optional
import numpy as np

class PerformanceCalculator(ABC):
    """Abstract interface for performance metrics calculation."""
    
    @abstractmethod
    def calculate_sharpe_ratio(
        self, 
        price_data: PriceData, 
        risk_free_rate: float = 0.015
    ) -> SharpeMetrics:
        """Calculate Sharpe ratio and related metrics."""
        pass
    
    @abstractmethod
    def calculate_bulk_metrics(
        self, 
        price_data_dict: Dict[str, PriceData],
        risk_free_rate: float = 0.015
    ) -> Dict[str, SharpeMetrics]:
        """Calculate metrics for multiple stocks efficiently."""
        pass

@dataclass
class SharpeMetrics:
    """Comprehensive performance metrics."""
    ticker: str
    name: str  # From SP500 universe
    sector: str  # From SP500 universe
    sharpe_ratio: float
    annualized_return: float
    volatility: float  # Annualized standard deviation
    max_drawdown: float
    data_points: int
    data_start_date: datetime
    data_end_date: datetime
    partial: bool = False  # True if <3 years of data
    calculation_timestamp: datetime
    
    def __post_init__(self):
        """Validate calculated metrics."""
        if not -10.0 <= self.sharpe_ratio <= 10.0:
            raise ValidationError(f"Invalid Sharpe ratio: {self.sharpe_ratio}")
        if self.volatility < 0:
            raise ValidationError(f"Negative volatility: {self.volatility}")
```

### Implementation Contract
```python
class SharpeCalculator(PerformanceCalculator):
    """Vectorized implementation of Sharpe ratio calculations."""
    
    def __init__(self, config: CalculatorConfig):
        self.min_data_points = config.min_data_points  # Default: 252 (1 year)
        self.trading_days_per_year = 252
        
    def calculate_sharpe_ratio(
        self, 
        price_data: PriceData, 
        risk_free_rate: float = 0.015
    ) -> SharpeMetrics:
        """
        Calculate Sharpe ratio using daily returns.
        
        Formula: (mean_daily_return - daily_rf_rate) / std_daily_return * sqrt(252)
        
        Args:
            price_data: Historical price data
            risk_free_rate: Annual risk-free rate
            
        Returns:
            SharpeMetrics with all calculated fields
            
        Raises:
            InsufficientDataError: <1 year of data
            CalculationError: NaN/Inf results
        """
        # Vectorized calculation implementation
        daily_returns = np.diff(price_data.adjusted_close) / price_data.adjusted_close[:-1]
        daily_rf_rate = risk_free_rate / 252
        
        excess_returns = daily_returns - daily_rf_rate
        sharpe_ratio = np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(252)
        
        # Additional validation and metadata
        pass
```

## 3. DataCache Interface

### Contract Definition
```python
from typing import Optional, Dict, Any
from datetime import timedelta

class CacheProvider(ABC):
    """Abstract cache interface supporting multiple storage tiers."""
    
    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        """Retrieve value by key from cache."""
        pass
    
    @abstractmethod  
    async def set(
        self, 
        key: str, 
        value: Any, 
        ttl: Optional[timedelta] = None
    ) -> bool:
        """Store value with optional TTL."""
        pass
    
    @abstractmethod
    async def get_many(self, keys: List[str]) -> Dict[str, Any]:
        """Bulk retrieval for multiple keys."""
        pass
    
    @abstractmethod
    def get_stats(self) -> CacheStats:
        """Return cache performance statistics."""
        pass

@dataclass
class CacheStats:
    """Cache performance metrics."""
    hits: int
    misses: int  
    hit_rate: float
    memory_usage: int  # bytes
    disk_usage: int  # bytes
    entry_count: int
    oldest_entry: Optional[datetime]
```

### Implementation Contract
```python
class DataCache(CacheProvider):
    """Multi-tier cache with memory + disk storage."""
    
    def __init__(self, config: CacheConfig):
        self.memory_cache = LRUCache(maxsize=config.memory_entries)
        self.disk_cache_path = config.disk_path
        self.default_ttl = config.default_ttl
        
    async def get(self, key: str) -> Optional[Any]:
        """
        Multi-tier cache lookup: memory -> disk -> None.
        
        Args:
            key: Cache key (formatted by service layer)
            
        Returns:
            Cached value or None if not found/expired
        """
        # Check memory cache first
        if value := self.memory_cache.get(key):
            return value
            
        # Check disk cache
        if value := await self._load_from_disk(key):
            # Promote to memory cache
            self.memory_cache[key] = value
            return value
            
        return None
    
    async def set(
        self, 
        key: str, 
        value: Any, 
        ttl: Optional[timedelta] = None
    ) -> bool:
        """
        Store in both memory and disk caches.
        
        Args:
            key: Cache key
            value: Data to cache (must be serializable)
            ttl: Time to live, uses default if None
            
        Returns:
            True if successfully stored
        """
        ttl = ttl or self.default_ttl
        
        # Store in memory with TTL
        self.memory_cache.set(key, value, ttl)
        
        # Async store to disk
        await self._save_to_disk(key, value, ttl)
        
        return True
```

## 4. StockRanker Interface (Business Logic)

### Contract Definition
```python
class StockRanker:
    """Orchestrates the complete stock ranking workflow."""
    
    def __init__(
        self,
        data_adapter: PriceDataSource,
        calculator: PerformanceCalculator, 
        cache: CacheProvider,
        universe_loader: SP500Loader
    ):
        self.data_adapter = data_adapter
        self.calculator = calculator  
        self.cache = cache
        self.universe_loader = universe_loader
        
    async def get_top_stocks(
        self,
        count: int = 5,
        period: str = "5y", 
        risk_free_rate: float = 0.015,
        universe: str = "sp500",
        min_data_years: int = 3
    ) -> TopStocksResponse:
        """
        Main orchestration method for ranking workflow.
        
        Args:
            count: Number of top stocks to return
            period: Time period for analysis
            risk_free_rate: Annual risk-free rate
            universe: Stock universe identifier  
            min_data_years: Minimum years of data required
            
        Returns:
            TopStocksResponse with ranked stocks and metadata
            
        Raises:
            ValidationError: Invalid parameters
            ServiceUnavailableError: External services down
        """
        # 1. Load stock universe
        universe_stocks = await self.universe_loader.get_universe(universe)
        
        # 2. Check cache for existing calculations
        cache_results = await self._check_cache(universe_stocks, period)
        
        # 3. Fetch missing price data
        missing_tickers = self._identify_missing_data(cache_results)
        if missing_tickers:
            price_data = await self.data_adapter.fetch_bulk_data(
                missing_tickers, period
            )
            await self._update_cache(price_data)
        
        # 4. Calculate Sharpe ratios for all stocks
        all_metrics = await self._calculate_all_metrics(
            universe_stocks, risk_free_rate, min_data_years
        )
        
        # 5. Rank and filter results
        top_stocks = self._rank_and_filter(all_metrics, count)
        
        # 6. Build response with metadata
        return self._build_response(top_stocks, universe_stocks)
```

## 5. API Service Contracts

### FastAPI Endpoint Specifications

```python
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field

class TopStocksRequest(BaseModel):
    """Request parameters with validation."""
    count: int = Field(default=5, ge=1, le=50)
    period: str = Field(default="5y", regex="^(1y|2y|5y|10y)$")
    rf: float = Field(default=0.015, ge=0.0, le=0.1)
    universe: str = Field(default="sp500", regex="^(sp500|nasdaq100|russell1000)$")
    min_data_years: int = Field(default=3, ge=1, le=10)

class TopStocksResponse(BaseModel):
    """Standardized response format."""
    stocks: List[SharpeMetrics]
    metadata: ResponseMetadata
    execution_time_ms: int
    cache_hit_rate: float
    request_id: str

class ResponseMetadata(BaseModel):
    """Response metadata for observability."""
    total_analyzed: int
    filtered_out: int
    data_freshness: datetime
    universe_size: int
    partial_data_count: int
    error_count: int
    warnings: List[str] = []

app = FastAPI(title="Top Sharpe Ratio API", version="1.0.0")

@app.get("/api/top-stocks", response_model=TopStocksResponse)
async def get_top_stocks(
    params: TopStocksRequest = Depends(),
    ranker: StockRanker = Depends(get_stock_ranker)
) -> TopStocksResponse:
    """
    Get top stocks by Sharpe ratio.
    
    Returns:
        List of top-performing stocks with calculated metrics
        
    Raises:
        HTTPException: 400 for validation errors, 500 for service errors
    """
    try:
        result = await ranker.get_top_stocks(**params.dict())
        return result
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ServiceUnavailableError as e:
        raise HTTPException(status_code=503, detail=str(e))
```

## 6. Error Handling Contracts

### Exception Hierarchy
```python
class ServiceError(Exception):
    """Base exception for all service errors."""
    pass

class DataSourceError(ServiceError):
    """Error fetching data from external source."""
    def __init__(self, source: str, ticker: str, original_error: Exception):
        self.source = source
        self.ticker = ticker  
        self.original_error = original_error
        super().__init__(f"Failed to fetch {ticker} from {source}: {original_error}")

class ValidationError(ServiceError):
    """Data validation error."""
    def __init__(self, field: str, value: Any, constraint: str):
        self.field = field
        self.value = value
        self.constraint = constraint
        super().__init__(f"Validation failed for {field}={value}: {constraint}")

class CalculationError(ServiceError):
    """Error in performance calculations."""
    pass

class InsufficientDataError(ServiceError):
    """Not enough data for reliable calculation."""
    def __init__(self, ticker: str, available_days: int, required_days: int):
        self.ticker = ticker
        self.available_days = available_days
        self.required_days = required_days
        super().__init__(
            f"{ticker}: insufficient data ({available_days} days, need {required_days})"
        )

class ServiceUnavailableError(ServiceError):
    """External service unavailable.""" 
    pass
```

## 7. Configuration Contracts

### Service Configuration
```python
@dataclass
class AdapterConfig:
    """YahooFinanceAdapter configuration."""
    base_url: str = "https://query1.finance.yahoo.com"
    timeout: float = 10.0
    max_concurrent: int = 10
    retry_config: RetryConfig = field(default_factory=RetryConfig)
    failure_threshold: float = 0.5
    recovery_timeout: float = 60.0

@dataclass  
class RetryConfig:
    """Retry configuration for external calls."""
    max_retries: int = 3
    base_delay: float = 1.0
    max_delay: float = 60.0
    exponential_base: float = 2.0
    
@dataclass
class CacheConfig:
    """Cache configuration."""
    memory_entries: int = 200
    disk_path: str = "/tmp/sharpe_cache"
    default_ttl: timedelta = field(default_factory=lambda: timedelta(hours=24))
    cleanup_interval: timedelta = field(default_factory=lambda: timedelta(hours=6))

@dataclass
class CalculatorConfig:
    """Performance calculator configuration."""
    min_data_points: int = 252  # 1 year
    trading_days_per_year: int = 252
    outlier_threshold: float = 0.5  # 50% daily change threshold
```

This service contract specification provides the foundation for implementing the Top 5 Sharpe Ratio application with clear interfaces, proper error handling, and comprehensive configuration management.
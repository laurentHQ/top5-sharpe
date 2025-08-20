"""
S&P 500 Universe Loader Module

This module provides functionality to load and validate the S&P 500 stock universe
from a deterministic CSV snapshot. The data is used as the foundation for 
Sharpe ratio calculations and stock analysis.

Data Source: GitHub datasets/s-and-p-500-companies (derived from Wikipedia)
Last Updated: August 2024
"""

import csv
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Optional


@dataclass
class SP500Stock:
    """Represents a single S&P 500 stock"""
    ticker: str
    name: str
    sector: str
    
    def __post_init__(self):
        """Validate ticker format after initialization"""
        if not self.is_valid_ticker(self.ticker):
            raise ValueError(f"Invalid ticker format: {self.ticker}")
    
    @staticmethod
    def is_valid_ticker(ticker: str) -> bool:
        """Validate ticker format: 1-5 uppercase letters, dots allowed for share classes"""
        if not ticker or not isinstance(ticker, str):
            return False
        # Allow patterns like BRK.B, BF.B, NWSA, etc.
        return bool(re.match(r'^[A-Z]{1,5}(\.[A-Z])?$', ticker.strip()))


class SP500LoaderError(Exception):
    """Custom exception for S&P 500 loader errors"""
    pass


class SP500Loader:
    """Loads and validates S&P 500 universe data"""
    
    def __init__(self, csv_path: Optional[str] = None, validate_count: bool = True):
        """
        Initialize loader with optional custom CSV path
        
        Args:
            csv_path: Custom path to SP500 CSV file. If None, uses default location.
            validate_count: Whether to validate stock count is in acceptable range (490-510)
        """
        if csv_path:
            self.csv_path = Path(csv_path)
        else:
            # Default to data/sp500.csv relative to this module
            module_dir = Path(__file__).parent
            self.csv_path = module_dir / "sp500.csv"
        
        self.validate_count = validate_count
    
    def load_sp500_universe(self) -> List[SP500Stock]:
        """
        Load S&P 500 universe from CSV file
        
        Returns:
            List of SP500Stock objects
            
        Raises:
            SP500LoaderError: If file not found, malformed, or validation fails
        """
        if not self.csv_path.exists():
            raise SP500LoaderError(f"S&P 500 data file not found: {self.csv_path}")
        
        try:
            stocks = []
            with open(self.csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                # Validate expected headers
                expected_headers = {'ticker', 'name', 'sector'}
                actual_headers = set(reader.fieldnames or [])
                if not expected_headers.issubset(actual_headers):
                    missing = expected_headers - actual_headers
                    raise SP500LoaderError(f"Missing required CSV headers: {missing}")
                
                for row_num, row in enumerate(reader, start=2):  # Start at 2 (after header)
                    try:
                        # Validate required fields are present and non-empty
                        ticker = row['ticker'].strip()
                        name = row['name'].strip()
                        sector = row['sector'].strip()
                        
                        if not ticker or not name or not sector:
                            raise SP500LoaderError(
                                f"Row {row_num}: Missing required data - "
                                f"ticker='{ticker}', name='{name}', sector='{sector}'"
                            )
                        
                        # Create stock object (validates ticker format)
                        stock = SP500Stock(ticker=ticker, name=name, sector=sector)
                        stocks.append(stock)
                        
                    except ValueError as e:
                        raise SP500LoaderError(f"Row {row_num}: {e}")
        
        except csv.Error as e:
            raise SP500LoaderError(f"CSV parsing error: {e}")
        except OSError as e:
            raise SP500LoaderError(f"File access error: {e}")
        
        # Validate stock count is within acceptable range
        if self.validate_count:
            stock_count = len(stocks)
            if not (490 <= stock_count <= 510):
                raise SP500LoaderError(
                    f"Stock count {stock_count} outside acceptable range (490-510)"
                )
        
        # Check for duplicate tickers
        tickers = [stock.ticker for stock in stocks]
        if len(tickers) != len(set(tickers)):
            duplicates = [t for t in set(tickers) if tickers.count(t) > 1]
            raise SP500LoaderError(f"Duplicate tickers found: {duplicates}")
        
        return stocks
    
    def get_tickers(self) -> List[str]:
        """
        Get list of all S&P 500 tickers
        
        Returns:
            List of ticker symbols
        """
        stocks = self.load_sp500_universe()
        return [stock.ticker for stock in stocks]
    
    def get_sectors(self) -> Dict[str, List[str]]:
        """
        Get stocks organized by sector
        
        Returns:
            Dictionary mapping sector names to lists of tickers
        """
        stocks = self.load_sp500_universe()
        sectors = {}
        
        for stock in stocks:
            if stock.sector not in sectors:
                sectors[stock.sector] = []
            sectors[stock.sector].append(stock.ticker)
        
        return sectors
    
    def get_stock_info(self, ticker: str) -> Optional[SP500Stock]:
        """
        Get information for a specific ticker
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            SP500Stock object if found, None otherwise
        """
        stocks = self.load_sp500_universe()
        ticker = ticker.upper().strip()
        
        for stock in stocks:
            if stock.ticker == ticker:
                return stock
        
        return None


# Convenience function for backward compatibility and simple usage
def load_sp500_universe(csv_path: Optional[str] = None) -> List[SP500Stock]:
    """
    Load S&P 500 universe data (convenience function)
    
    Args:
        csv_path: Optional custom path to CSV file
        
    Returns:
        List of SP500Stock objects
    """
    loader = SP500Loader(csv_path)
    return loader.load_sp500_universe()


# Additional convenience functions
def get_sp500_tickers(csv_path: Optional[str] = None) -> List[str]:
    """Get list of all S&P 500 ticker symbols"""
    loader = SP500Loader(csv_path)
    return loader.get_tickers()


def get_sp500_sectors(csv_path: Optional[str] = None) -> Dict[str, List[str]]:
    """Get S&P 500 stocks organized by sector"""
    loader = SP500Loader(csv_path)
    return loader.get_sectors()
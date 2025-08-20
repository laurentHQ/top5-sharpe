# 01 Foundation Data Tasks

Core data infrastructure tasks that establish the data foundation for the Sharpe ratio application. These tasks must be completed first as they provide the data sources for all subsequent analysis.

## Task Group Priority
**Phase**: Foundation
**Dependencies**: None (starting point)
**Blocks**: Backend API development, testing
**Estimated Duration**: 3-5 days

---

## Task 1: S&P 500 Universe & Snapshot CSV

```yaml
title: "Define S&P 500 universe & snapshot CSV"
repo: "github.com/laurentHQ/top5-sharpe"
branch: "feat/sp500-universe"
description: |
  Create a deterministic S&P 500 stock universe dataset as the foundation for Sharpe ratio calculations.
  This task establishes the data source that feeds all subsequent analysis and ranking operations.
acceptance_criteria:
  - "Add data/sp500.csv with ticker, name; 500±10 rows; deterministic snapshot"
  - "Loader reads CSV and exposes list via Python module"
cos: Standard
definition_of_done:
  - "CSV committed; loader unit test >=1"
  - "README notes snapshot source/date"
todo_list:
  planner:
    - "Analyze S&P 500 data requirements and source options"
    - "Define CSV schema: ticker (symbol), name (company), sector (optional)"
    - "Research reliable S&P 500 constituent sources (Wikipedia, SPDR, etc.)"
    - "Plan data validation strategy for ticker format and duplicates"
  data:
    - "Create data/ directory structure"
    - "Download current S&P 500 constituents from reliable source"
    - "Clean and format data: uppercase tickers, validate symbols"
    - "Create sp500.csv with headers: ticker,name,sector"
    - "Implement sp500_loader.py module with load_sp500_universe() function"
    - "Add schema validation: ticker format (^[A-Z]{1,5}$), required fields"
    - "Add error handling for file not found, malformed CSV"
  reviewer:
    - "Review CSV data quality and completeness"
    - "Validate loader module follows Python conventions"
    - "Check error handling coverage and edge cases"
    - "Verify no hardcoded paths or security issues"
  tester:
    - "Write unit tests for sp500_loader.load_sp500_universe()"
    - "Test CSV parsing with valid and invalid data"
    - "Test error handling for missing files and malformed CSV"
    - "Verify ticker count is within acceptable range (490-510)"
agent_sequence:
  - planner: {tooling: "Sequential MCP + tech-lead-orchestrator"}
  - data: {agent: "backend-developer", cmd: "create CSV + loader module with schema validation"}
  - reviewer: {agent: "code-reviewer", mode: "rigorous security-aware review"}
  - tester: {agent: "test-engineer", cmd: "write unit tests for loader"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

---

## Task 2: yfinance Adapter + Retries + Caching

```yaml
title: "Implement yfinance adapter + retries + caching"
repo: "github.com/laurentHQ/top5-sharpe"
branch: "feat/yf-adapter-cache"
description: |
  Build a robust data fetching layer that handles Yahoo Finance API calls with resilience patterns.
  Implements caching to minimize API calls and improve performance for repeated requests.
acceptance_criteria:
  - "Fetch 5y adjusted close for a list of tickers; backoff (exponential, max 5 retries)"
  - "On-disk cache (parquet or SQLite) with TTL configurable; cache hit rate logged"
cos: Standard
definition_of_done:
  - "Adapter module documented; integration smoke passes"
  - "Unit tests cover retry/backoff and cache TTL behavior"
todo_list:
  planner:
    - "Design yfinance adapter interface: fetch_prices(tickers, period='5y')"
    - "Plan exponential backoff strategy: 1s, 2s, 4s, 8s, 16s delays"
    - "Define cache schema and TTL strategy (default 1 day)"
    - "Plan error handling for network, API limits, invalid tickers"
  data:
    - "Install yfinance dependency with version pinning"
    - "Create yfinance_adapter.py module"
    - "Implement fetch_prices() with batch ticker handling"
    - "Add exponential backoff with jitter for failed requests"
    - "Implement on-disk cache using parquet files or SQLite"
    - "Add cache TTL validation and cleanup mechanisms"
    - "Add logging for cache hits/misses and retry attempts"
    - "Handle yfinance exceptions and rate limiting gracefully"
  backend:
    - "Create data_service.py to wrap adapter functionality"
    - "Implement get_stock_data() service method"
    - "Add configuration management for cache TTL and retry settings"
    - "Expose cache statistics and health monitoring"
  reviewer:
    - "Review retry logic and error handling robustness"
    - "Validate cache implementation and TTL handling"
    - "Check for resource leaks and proper file handling"
    - "Verify no sensitive data is logged or cached insecurely"
  tester:
    - "Mock yfinance for unit tests to avoid network calls"
    - "Test exponential backoff behavior with failing requests"
    - "Test cache hit/miss scenarios with TTL expiration"
    - "Benchmark performance with and without caching"
    - "Test batch processing with mixed valid/invalid tickers"
agent_sequence:
  - planner: {tooling: "Sequential MCP + tech-lead-orchestrator"}
  - data: {agent: "python-backend-expert", cmd: "build adapter with yfinance, cache, retry/backoff"}
  - backend: {agent: "backend-developer", cmd: "expose adapter via service layer"}
  - reviewer: {agent: "code-reviewer", mode: "rigorous security-aware review"}
  - tester: {agent: "test-engineer", cmd: "unit tests for cache+retry; record timings"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

---

## Task 3: Sharpe Engine Utilities

```yaml
title: "Sharpe engine utilities (calc, RF override, partial data)"
repo: "github.com/laurentHQ/top5-sharpe"
branch: "feat/sharpe-engine"
description: |
  Implement core financial calculations for Sharpe ratio analysis with proper handling of edge cases.
  This is the mathematical heart of the application that converts price data into risk-adjusted returns.
acceptance_criteria:
  - "Daily log returns; annualized Sharpe = mean/std*sqrt(252); RF default 0.015; override via arg"
  - "Handles NaNs; requires ≥3y else marks partial=true"
cos: Standard
definition_of_done:
  - "Pure functions with docstrings; 100% branch coverage for edge cases"
  - "Property-based tests for stability on random inputs"
todo_list:
  planner:
    - "Define Sharpe ratio calculation methodology and formula validation"
    - "Plan NaN handling strategy for missing price data"
    - "Design partial data flagging criteria (minimum 3 years of data)"
    - "Plan risk-free rate override mechanism and validation"
  backend:
    - "Create sharpe_utils.py module with pure functions"
    - "Implement calculate_daily_returns(prices) using log returns"
    - "Implement calculate_sharpe_ratio(returns, risk_free_rate=0.015)"
    - "Add annualization factor sqrt(252) for daily data"
    - "Handle NaN values in price series and returns calculation"
    - "Implement has_sufficient_data() to check 3-year minimum"
    - "Add input validation for risk_free_rate (0 <= rf <= 0.3)"
    - "Create comprehensive docstrings with mathematical formulas"
  tester:
    - "Write deterministic tests with known input/output pairs"
    - "Test Sharpe calculation with synthetic perfect data"
    - "Test NaN handling with missing price data scenarios"
    - "Property-based tests with random walk price series"
    - "Test edge cases: zero volatility, negative returns, empty data"
    - "Verify risk-free rate override functionality"
    - "Test partial data flagging with various data lengths"
  reviewer:
    - "Validate mathematical accuracy of Sharpe ratio implementation"
    - "Review NaN handling and edge case robustness"
    - "Check function purity and lack of side effects"
    - "Verify docstring accuracy and completeness"
agent_sequence:
  - planner: {tooling: "Sequential MCP + tech-lead-orchestrator"}
  - backend: {agent: "python-ml-specialist", cmd: "implement sharpe utils + RF override handling"}
  - tester: {agent: "test-engineer", cmd: "unit/property tests for sharpe utils"}
  - reviewer: {agent: "code-reviewer", mode: "rigorous security-aware review"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

---

## Task Group Dependencies

**Provides Foundation For:**
- Backend API endpoints (`/api/top-stocks`, `/api/price-series`)
- Frontend data visualization
- Testing and validation workflows
- Performance optimization tasks

**Quality Gates:**
- All unit tests must pass with ≥95% coverage
- Cache hit rate logging functional
- Data validation prevents invalid inputs
- Mathematical accuracy verified with known test cases

**Performance Targets:**
- S&P 500 data loading: <100ms
- yfinance cache warm hit: <50ms
- Sharpe calculation for 500 stocks: <2s
- Memory usage: <100MB for full dataset
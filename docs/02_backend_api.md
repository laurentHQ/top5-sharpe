# 02 Backend API Tasks

FastAPI application and endpoint implementation tasks. These tasks build the web API layer that exposes the Sharpe ratio analysis functionality to frontend clients.

## Task Group Priority
**Phase**: Backend Development
**Dependencies**: Foundation Data tasks (01_foundation_data.md)
**Blocks**: Frontend UI development, integration testing
**Estimated Duration**: 4-6 days

---

## Task 1: FastAPI Scaffold + Health Endpoint

```yaml
title: "FastAPI scaffold + /health"
repo: "github.com/laurentHQ/top5-sharpe"
branch: "feat/fastapi-scaffold"
description: |
  Create the foundational FastAPI application structure with health monitoring.
  Establishes the web framework foundation for all subsequent API endpoints.
acceptance_criteria:
  - "FastAPI app with GET /health returns {status:'ok', version}"
  - "Uvicorn dev server via make dev"
cos: Standard
definition_of_done:
  - "Basic project layout; lint passes"
  - "Docker runs /health successfully"
todo_list:
  planner:
    - "Design FastAPI application structure and organization"
    - "Plan health endpoint specification and response format"
    - "Define project layout: app/, tests/, requirements.txt"
    - "Plan development workflow and Makefile targets"
  backend:
    - "Create app/ directory structure with __init__.py"
    - "Implement main.py with FastAPI app instance"
    - "Add /health endpoint returning {status: 'ok', version: '0.1.0'}"
    - "Configure CORS middleware for development"
    - "Add basic logging configuration"
    - "Create requirements.txt with FastAPI, uvicorn dependencies"
  devops:
    - "Create Makefile with 'make dev' target for uvicorn"
    - "Add 'make install' target for pip install -r requirements.txt"
    - "Configure uvicorn with reload and host settings"
    - "Add basic .env support for configuration"
  tester:
    - "Create basic smoke test for /health endpoint"
    - "Test response format and status code 200"
    - "Verify server starts without errors"
  reviewer:
    - "Review FastAPI best practices and project structure"
    - "Validate security middleware configuration"
    - "Check error handling and logging setup"
agent_sequence:
  - planner: {tooling: "Sequential MCP + tech-lead-orchestrator"}
  - backend: {agent: "python-backend-expert", cmd: "create FastAPI app skeleton + /health"}
  - devops: {agent: "devops-specialist", cmd: "update Makefile to run server"}
  - tester: {agent: "test-engineer", cmd: "smoke test /health"}
  - reviewer: {agent: "code-reviewer", mode: "rigorous security-aware review"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

---

## Task 2: /api/top-stocks Endpoint + Models + Ranking

```yaml
title: "/api/top-stocks endpoint + models + ranking"
repo: "github.com/laurentHQ/top5-sharpe"
branch: "feat/api-top-stocks"
description: |
  Implement the core API endpoint that delivers ranked stocks by Sharpe ratio.
  This is the primary business logic endpoint that orchestrates data fetching, calculation, and ranking.
acceptance_criteria:
  - "GET /api/top-stocks?count=5&period=5y&rf=0.015&universe=sp500 returns JSON list with ticker, name, sharpe, last_price, ret_1y"
  - "Response time ≤5s cold, ≤2s warm for S&P500 universe"
cos: Standard
definition_of_done:
  - "Pydantic models; error handling for invalid params/timeouts"
  - "Integration test green on CI"
todo_list:
  planner:
    - "Design API contract for /api/top-stocks endpoint"
    - "Define Pydantic models for request/response schemas"
    - "Plan ranking algorithm and tie-breaking logic"
    - "Design performance optimization strategy for 500-stock universe"
  backend:
    - "Create models/schemas.py with Pydantic models"
    - "Define TopStocksRequest model with count, period, rf, universe"
    - "Define StockRanking model with ticker, name, sharpe, last_price, ret_1y"
    - "Create api/endpoints.py with /api/top-stocks route"
    - "Implement get_top_stocks() endpoint handler"
    - "Wire together SP500 loader, yfinance adapter, and Sharpe engine"
    - "Add ranking logic with proper tie-breaking (by ticker name)"
    - "Implement in-process caching for repeated requests"
    - "Add request validation and error handling"
    - "Add performance monitoring and logging"
  tester:
    - "Create integration test with full request/response cycle"
    - "Test happy path with default parameters"
    - "Test edge cases: count=1, count=50, invalid parameters"
    - "Test performance with cold cache vs warm cache"
    - "Mock yfinance for deterministic testing"
    - "Test error handling for network failures and invalid tickers"
  reviewer:
    - "Review API design and Pydantic model structure"
    - "Validate ranking logic and tie-breaking implementation"
    - "Check performance optimizations and caching strategy"
    - "Review error handling and input validation"
agent_sequence:
  - planner: {tooling: "Sequential MCP + api-architect"}
  - backend: {agent: "python-backend-expert", cmd: "implement endpoint wiring adapter+sharpe engine + in-process cache"}
  - tester: {agent: "test-engineer", cmd: "author integration tests for happy/edge cases"}
  - reviewer: {agent: "code-reviewer", mode: "rigorous security-aware review"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

---

## Task 3: /api/price-series/:ticker for Sparkline

```yaml
title: "/api/price-series/:ticker for sparkline"
repo: "github.com/laurentHQ/top5-sharpe"
branch: "feat/api-price-series"
description: |
  Create API endpoint for individual stock price time series data to power sparkline visualizations.
  Provides historical price data in compact format optimized for frontend charting.
acceptance_criteria:
  - "GET /api/price-series/:ticker?period=5y returns compact timeseries (date, adj_close)"
  - "Handles missing ticker with 404 + error message"
cos: Standard
definition_of_done:
  - "Endpoint documented; unit tests for serialization"
  - "Cache layer reused from adapter"
todo_list:
  planner:
    - "Design compact time series API response format"
    - "Plan error handling for invalid/missing tickers"
    - "Define cache reuse strategy from yfinance adapter"
  backend:
    - "Add /api/price-series/{ticker} route to endpoints.py"
    - "Create PriceSeriesResponse Pydantic model"
    - "Implement get_price_series() endpoint handler"
    - "Reuse yfinance adapter cache for price data"
    - "Return compact JSON: [{date: 'YYYY-MM-DD', price: float}]"
    - "Add 404 handling for invalid tickers with error message"
    - "Add input validation for ticker format"
  tester:
    - "Test valid ticker returns expected time series format"
    - "Test invalid ticker returns 404 with proper error message"
    - "Test cache reuse from previous API calls"
    - "Verify compact JSON format and data types"
  reviewer:
    - "Review API endpoint design and response format"
    - "Validate error handling and status codes"
    - "Check cache integration and performance"
agent_sequence:
  - planner: {tooling: "Sequential MCP + api-architect"}
  - backend: {agent: "python-backend-expert", cmd: "add endpoint using adapter cache; compact JSON"}
  - tester: {agent: "test-engineer", cmd: "tests for valid/invalid ticker"}
  - reviewer: {agent: "code-reviewer", mode: "rigorous security-aware review"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

---

## Task 4: Input Validation + Error Paths + Logging

```yaml
title: "Input validation + error paths + logging"
repo: "github.com/laurentHQ/top5-sharpe"
branch: "feat/api-validation-logging"
description: |
  Implement comprehensive input validation and structured error handling across all API endpoints.
  Adds observability through structured logging and request correlation.
acceptance_criteria:
  - "Validate count (1–50), period (3y/5y), rf (0–0.2); structured error responses"
  - "Request/response logging with correlation id; rate limit placeholder"
cos: Standard
definition_of_done:
  - "Negative tests added; pydantic validation errors mapped"
  - "Logging documented in README"
todo_list:
  planner:
    - "Design input validation rules and error response format"
    - "Plan structured logging strategy with correlation IDs"
    - "Design rate limiting approach and configuration"
    - "Plan error categorization and status code mapping"
  backend:
    - "Create validation/validators.py with input validators"
    - "Add CountValidator (1 <= count <= 50)"
    - "Add PeriodValidator (3y, 5y only)"
    - "Add RiskFreeRateValidator (0.0 <= rf <= 0.2)"
    - "Create middleware/logging.py for request logging"
    - "Add correlation ID generation and tracking"
    - "Create error handlers for validation failures"
    - "Add rate limiting middleware placeholder"
    - "Implement structured error response format"
  tester:
    - "Create negative test cases for all validation rules"
    - "Test error response format and status codes"
    - "Test logging output and correlation ID tracking"
    - "Verify rate limiting placeholder functionality"
  reviewer:
    - "Review validation logic and error handling completeness"
    - "Validate logging strategy and data sensitivity"
    - "Check rate limiting implementation readiness"
agent_sequence:
  - planner: {tooling: "Sequential MCP + api-architect"}
  - backend: {agent: "python-backend-expert", cmd: "add validators, error mappers, logging middleware"}
  - tester: {agent: "test-engineer", cmd: "negative test cases for invalid inputs"}
  - reviewer: {agent: "code-reviewer", mode: "rigorous security-aware review"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

---

## Task 5: Observability Hooks (Basic Logging Metrics)

```yaml
title: "Observability hooks (basic logging metrics)"
repo: "github.com/laurentHQ/top5-sharpe"
branch: "feat/observability-hooks"
description: |
  Add performance monitoring and observability features to track API usage and performance.
  Provides operational visibility into cache performance and request patterns.
acceptance_criteria:
  - "Log request latencies; cache hit/miss metrics; simple /metrics JSON"
  - "Sample dashboard JSON or documentation"
cos: Standard
definition_of_done:
  - "Metrics visible locally; docs updated"
  - "Perf budget tracked in README"
todo_list:
  planner:
    - "Design metrics collection strategy and storage"
    - "Plan /metrics endpoint format and content"
    - "Define performance budget tracking approach"
    - "Plan dashboard visualization requirements"
  backend:
    - "Create metrics/collector.py for metrics gathering"
    - "Add request latency timing middleware"
    - "Track cache hit/miss ratios from yfinance adapter"
    - "Implement /metrics endpoint with JSON response"
    - "Add memory usage and request count tracking"
    - "Create performance budget monitoring"
    - "Add metrics reset functionality"
  tester:
    - "Test metrics collection under various load patterns"
    - "Verify /metrics endpoint returns expected format"
    - "Test cache metrics accuracy with known scenarios"
    - "Benchmark metrics collection overhead"
  reviewer:
    - "Review metrics collection performance impact"
    - "Validate metrics accuracy and usefulness"
    - "Check metrics endpoint security considerations"
agent_sequence:
  - planner: {tooling: "Sequential MCP + backend-developer"}
  - backend: {agent: "python-backend-expert", cmd: "emit timing + cache metrics; add /metrics"}
  - tester: {agent: "performance-optimizer", cmd: "verify metrics fields present under load"}
  - reviewer: {agent: "code-reviewer", mode: "rigorous security-aware review"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

---

## Task Group Dependencies

**Requires Foundation:**
- S&P 500 data loader (01_foundation_data.md)
- yfinance adapter with caching
- Sharpe ratio calculation engine

**Provides API For:**
- Frontend UI data fetching
- External API consumers
- Performance monitoring and optimization

**Quality Gates:**
- All endpoints return proper HTTP status codes
- Response times meet SLA requirements (≤5s cold, ≤2s warm)
- Input validation prevents invalid requests
- Error responses follow consistent format
- Logging provides operational visibility

**Performance Targets:**
- `/health` endpoint: <50ms response time
- `/api/top-stocks` (warm cache): <2s response time
- `/api/price-series` (warm cache): <500ms response time
- Memory usage: <200MB under normal load
- Cache hit rate: >80% for repeated requests
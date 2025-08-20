# 04 Testing & Validation Tasks

Comprehensive testing strategy covering unit tests, integration tests, and end-to-end validation. These tasks ensure system reliability, correctness, and performance compliance.

## Task Group Priority
**Phase**: Quality Assurance
**Dependencies**: Backend API (02_backend_api.md), Frontend UI (03_frontend_ui.md)
**Blocks**: Production deployment, release management
**Estimated Duration**: 4-5 days

---

## Task 1: Unit Tests - Sharpe Math (Deterministic + Randomized)

```yaml
title: "Unit tests: Sharpe math (deterministic + randomized)"
repo: "github.com/laurentHQ/top5-sharpe"
branch: "test/sharpe-unit"
description: |
  Comprehensive testing of Sharpe ratio calculations with both deterministic and property-based tests.
  Ensures mathematical correctness and handles edge cases robustly.
acceptance_criteria:
  - "Deterministic tests (known arrays) match expected Sharpe values"
  - "Property tests (random walks) produce finite numbers; reject NaN"
cos: Standard
definition_of_done:
  - "Coverage for sharpe utils ≥95%"
  - "CI green"
todo_list:
  planner:
    - "Design comprehensive test strategy for Sharpe ratio calculations"
    - "Plan deterministic test cases with known input/output pairs"
    - "Design property-based test strategy for edge cases"
    - "Plan coverage measurement and reporting"
  tester:
    - "Create test_sharpe_utils.py with pytest framework"
    - "Write deterministic tests with synthetic perfect data"
    - "Test known Sharpe values: risk-free asset (0), market return scenarios"
    - "Test edge cases: zero volatility, all negative returns, single data point"
    - "Implement property-based tests with hypothesis library"
    - "Test random walk price series produce finite Sharpe ratios"
    - "Test NaN handling in price series and returns"
    - "Test risk-free rate override functionality"
    - "Test data sufficiency checks (3-year minimum)"
    - "Add parametrized tests for different risk-free rates"
    - "Set up coverage reporting with pytest-cov"
  reviewer:
    - "Review test coverage and edge case completeness"
    - "Validate mathematical accuracy of test cases"
    - "Check property-based test robustness"
    - "Verify CI integration and reporting"
agent_sequence:
  - planner: {tooling: "Sequential MCP + test-engineer"}
  - tester: {agent: "test-engineer", cmd: "author unit + property tests; run locally"}
  - reviewer: {agent: "code-reviewer", mode: "rigorous security-aware review"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

---

## Task 2: Integration Test - /api/top-stocks Happy + Edge

```yaml
title: "Integration test: /api/top-stocks happy + edge"
repo: "github.com/laurentHQ/top5-sharpe"
branch: "test/api-top-stocks-integ"
description: |
  Comprehensive integration testing of the primary API endpoint with real data flows.
  Validates end-to-end functionality from request parsing to response formatting.
acceptance_criteria:
  - "Happy path: returns 5 items within ≤5s cold; schema validated"
  - "Edges: invalid count, rf out of range, partial data flagged"
cos: Standard
definition_of_done:
  - "Test suite runnable via make test and CI"
  - "Flaky test tolerance measured; retries configured"
todo_list:
  planner:
    - "Design integration test strategy for API endpoints"
    - "Plan test data setup and teardown procedures"
    - "Define performance validation within tests"
    - "Plan flaky test detection and retry logic"
  tester:
    - "Create test_api_integration.py with FastAPI test client"
    - "Set up test fixtures with known S&P 500 subset"
    - "Mock yfinance for deterministic integration testing"
    - "Test happy path: /api/top-stocks with default parameters"
    - "Validate response schema matches Pydantic models"
    - "Test performance: response time under 5s cold start"
    - "Test edge cases: count=1, count=50, invalid parameters"
    - "Test risk-free rate boundary values (0.0, 0.2)"
    - "Test error handling: invalid tickers, network failures"
    - "Test partial data flagging with insufficient history"
    - "Add retry logic for potentially flaky network operations"
    - "Configure test timeouts and performance assertions"
  reviewer:
    - "Review integration test coverage and scenarios"
    - "Validate test reliability and flaky test handling"
    - "Check performance assertions and timeout handling"
    - "Verify test isolation and cleanup procedures"
agent_sequence:
  - planner: {tooling: "Sequential MCP + test-engineer"}
  - tester: {agent: "test-engineer", cmd: "write integration tests using test client + fixtures"}
  - reviewer: {agent: "code-reviewer", mode: "rigorous security-aware review"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

---

## Task 3: Frontend Smoke Test on Docker Preview

```yaml
title: "Frontend smoke on Docker preview"
repo: "github.com/laurentHQ/top5-sharpe"
branch: "test/frontend-smoke-docker"
description: |
  End-to-end smoke testing of the complete application stack using Docker Compose.
  Validates frontend-backend integration and user workflow functionality.
acceptance_criteria:
  - "Open UI via compose; table renders; sorting works; RF input triggers reload"
  - "No uncaught promise rejections"
cos: Standard
definition_of_done:
  - "Test notes and screenshots attached"
  - "Issues created for any defects"
todo_list:
  planner:
    - "Design end-to-end smoke test workflow"
    - "Plan Docker Compose test environment setup"
    - "Define user journey validation checkpoints"
    - "Plan evidence collection and defect reporting"
  tester:
    - "Create smoke test procedure documentation"
    - "Set up Docker Compose test environment"
    - "Test application startup: docker-compose up"
    - "Verify /health endpoint accessibility"
    - "Test frontend loads without console errors"
    - "Test table renders with default data"
    - "Test column sorting functionality (all columns)"
    - "Test risk-free rate input and table reload"
    - "Test sparklines appear and render correctly"
    - "Test error states with simulated API failures"
    - "Test responsive design on different viewport sizes"
    - "Capture screenshots of key UI states"
    - "Document any defects or inconsistencies found"
  reviewer:
    - "Review smoke test procedure completeness"
    - "Validate test environment setup reliability"
    - "Check defect reporting and evidence quality"
agent_sequence:
  - tester: {agent: "test-engineer", cmd: "run smoke steps; capture evidence"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

---

## Task 4: Performance Validation & Benchmarking

```yaml
title: "Backend performance tune (cache warm path)"
repo: "github.com/laurentHQ/top5-sharpe"
branch: "perf/cache-warm"
description: |
  Performance optimization and validation to ensure SLA compliance.
  Implements cache warming strategies for improved response times.
acceptance_criteria:
  - "Warm cache routine for top 200 tickers at startup behind flag"
  - "Warm hit reduces /api/top-stocks latency by ≥40% vs cold"
cos: Intangible
definition_of_done:
  - "Benchmark before/after committed"
  - "Flag documented; default off"
todo_list:
  planner:
    - "Design cache warming strategy and implementation"
    - "Plan performance benchmarking methodology"
    - "Define SLA validation test procedures"
    - "Plan feature flag configuration and documentation"
  backend:
    - "Create cache warming module with startup hooks"
    - "Implement warm_cache_startup() behind feature flag"
    - "Add cache pre-loading for top 200 S&P 500 tickers"
    - "Configure cache warming as optional startup task"
    - "Add performance monitoring for warm vs cold hits"
    - "Document cache warming configuration options"
  tester:
    - "Benchmark cold start performance baseline"
    - "Measure warm cache performance improvements"
    - "Validate ≥40% latency reduction requirement"
    - "Test cache warming startup behavior"
    - "Performance test under simulated load"
    - "Document performance characteristics"
  reviewer:
    - "Review cache warming implementation efficiency"
    - "Validate performance improvements are measurable"
    - "Check feature flag configuration and defaults"
agent_sequence:
  - backend: {agent: "performance-optimizer", cmd: "implement optional warm-cache routine"}
  - tester: {agent: "test-engineer", cmd: "benchmark latency cold vs warm"}
  - reviewer: {agent: "code-reviewer", mode: "rigorous security-aware review"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

---

## Task 5: Cross-Module Review - Data Correctness

```yaml
title: "Cross-module review: data correctness"
repo: "github.com/laurentHQ/top5-sharpe"
branch: "review/data-correctness"
description: |
  Systematic review of data flow integrity across the entire application stack.
  Validates mathematical accuracy and data consistency from source to display.
acceptance_criteria:
  - "Verify adjusted close usage end-to-end; confirm ≥3y requirement honored"
  - "Spot-check 5 random tickers for consistency"
cos: Standard
definition_of_done:
  - "Review notes committed; issues filed if discrepancies"
  - "Green light to proceed to Test"
todo_list:
  planner:
    - "Design systematic data correctness review methodology"
    - "Plan end-to-end data flow validation approach"
    - "Define spot-check sampling strategy and criteria"
    - "Plan discrepancy reporting and issue tracking"
  reviewer:
    - "Review S&P 500 data quality and completeness"
    - "Validate yfinance adapter uses adjusted close prices"
    - "Check Sharpe ratio calculations against known benchmarks"
    - "Verify 3-year minimum data requirement enforcement"
    - "Spot-check 5 random tickers end-to-end:"
    - "- Data fetching accuracy from yfinance"
    - "- Sharpe calculation mathematical correctness"
    - "- API response format and values"
    - "- Frontend display and formatting"
    - "Review data handling for missing/partial data"
    - "Validate risk-free rate application in calculations"
    - "Check caching doesn't corrupt data integrity"
    - "Document review findings and any discrepancies"
  tester:
    - "Create validation scripts for spot-check automation"
    - "Verify review findings with additional test cases"
    - "Test data consistency across cache warm/cold states"
agent_sequence:
  - reviewer: {agent: "code-reviewer", mode: "rigorous security-aware review"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

---

## Task Group Dependencies

**Requires Complete Implementation:**
- All foundation data modules (01_foundation_data.md)
- All backend API endpoints (02_backend_api.md)
- All frontend UI components (03_frontend_ui.md)

**Validates System-Wide:**
- Mathematical accuracy of Sharpe calculations
- API contract compliance and performance
- Frontend-backend integration
- User workflow functionality
- Performance SLA compliance

**Quality Gates:**
- Unit test coverage ≥95% for mathematical functions
- Integration tests validate API contracts
- Smoke tests confirm user workflows
- Performance benchmarks meet SLA requirements
- Data correctness review passes with no critical issues

**Performance Validation:**
- Sharpe calculation accuracy: verified against known benchmarks
- API response times: ≤5s cold, ≤2s warm
- Frontend rendering: ≤2s after API response
- Cache performance: ≥40% improvement when warm
- Memory usage: <200MB backend, <50MB frontend
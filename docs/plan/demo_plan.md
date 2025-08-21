WIP limits — Design/Decompose: 2, Build: Generate: 3, Review: 2, Test: 2

# Options (Upstream)

```yaml
title: "Expedite placeholder: production hotfix policy"
repo: "github.com/demo/top5-sharpe"
branch: "ops/expedite-policy"
acceptance_criteria:
  - "Card reserved for true blockers only; one Expedite in system at a time"
  - "Swarm rule: all available agents pause Standard work until resolved"
cos: Expedite
definition_of_done:
  - "This placeholder remains empty unless a real blocker occurs"
  - "If used, post-mortem ticket created in Ready within 24h"
agent_sequence:
  - planner: {tooling: "MCP:architect,task-split"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

```yaml
title: "Expedite placeholder: security incident response"
repo: "github.com/demo/top5-sharpe"
branch: "ops/expedite-security"
acceptance_criteria:
  - "Only used for critical security fixes affecting data or users"
  - "Runtime to resolution target < 4h; announce start/stop times on board"
cos: Expedite
definition_of_done:
  - "Incident fixed, tests added to prevent regression"
  - "Post-incident review ticket added to Ready"
agent_sequence:
  - planner: {tooling: "MCP:architect,task-split"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

```yaml
title: "Fixed Date placeholder: live demo day (release readiness)"
repo: "github.com/demo/top5-sharpe"
branch: "release/demo-day"
acceptance_criteria:
  - "Demo checklist reviewed 48h, 24h, and 2h before demo"
  - "Risk review performed; any open risks have mitigation owners"
cos: FixedDate
definition_of_done:
  - "Release tag created; demo environment smoke-tested; rollback plan documented"
  - "Stakeholder sign-off captured on board"
agent_sequence:
  - planner: {tooling: "MCP:architect,task-split"}
  - devops: {agent: "Claude Code", cmd: "prepare demo environment + rollback plan"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

# Ready/Committed

```yaml
title: "Define S&P 500 universe & snapshot CSV"
repo: "github.com/demo/top5-sharpe"
branch: "feat/sp500-universe"
acceptance_criteria:
  - "Add data/sp500.csv with ticker, name; 500±10 rows; deterministic snapshot"
  - "Loader reads CSV and exposes list via Python module"
cos: Standard
definition_of_done:
  - "CSV committed; loader unit test >=1"
  - "README notes snapshot source/date"
agent_sequence:
  - planner: {tooling: "MCP:architect,task-split"}
  - data: {agent: "Claude Code", cmd: "create CSV + loader module with schema validation"}
  - reviewer: {agent: "Claude Code", mode: "static review + self-critique"}
  - tester: {agent: "Claude Code", cmd: "write unit tests for loader"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

```yaml
title: "Implement yfinance adapter + retries + caching"
repo: "github.com/demo/top5-sharpe"
branch: "feat/yf-adapter-cache"
acceptance_criteria:
  - "Fetch 5y adjusted close for a list of tickers; backoff (exponential, max 5 retries)"
  - "On-disk cache (parquet or SQLite) with TTL configurable; cache hit rate logged"
cos: Standard
definition_of_done:
  - "Adapter module documented; integration smoke passes"
  - "Unit tests cover retry/backoff and cache TTL behavior"
agent_sequence:
  - planner: {tooling: "MCP:architect,task-split"}
  - data: {agent: "Claude Code", cmd: "build adapter with yfinance, cache, retry/backoff"}
  - backend: {agent: "Claude Code", cmd: "expose adapter via service layer"}
  - reviewer: {agent: "Claude Code", mode: "static review + self-critique"}
  - tester: {agent: "Claude Code", cmd: "unit tests for cache+retry; record timings"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

```yaml
title: "Sharpe engine utilities (calc, RF override, partial data)"
repo: "github.com/demo/top5-sharpe"
branch: "feat/sharpe-engine"
acceptance_criteria:
  - "Daily log returns; annualized Sharpe = mean/std*sqrt(252); RF default 0.015; override via arg"
  - "Handles NaNs; requires ≥3y else marks partial=true"
cos: Standard
definition_of_done:
  - "Pure functions with docstrings; 100% branch coverage for edge cases"
  - "Property-based tests for stability on random inputs"
agent_sequence:
  - planner: {tooling: "MCP:architect,task-split"}
  - backend: {agent: "Claude Code", cmd: "implement sharpe utils + RF override handling"}
  - tester: {agent: "Claude Code", cmd: "unit/property tests for sharpe utils"}
  - reviewer: {agent: "Claude Code", mode: "static review + self-critique"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

```yaml
title: "FastAPI scaffold + /health"
repo: "github.com/demo/top5-sharpe"
branch: "feat/fastapi-scaffold"
acceptance_criteria:
  - "FastAPI app with GET /health returns {status:'ok', version}"
  - "Uvicorn dev server via make dev"
cos: Standard
definition_of_done:
  - "Basic project layout; lint passes"
  - "Docker runs /health successfully"
agent_sequence:
  - planner: {tooling: "MCP:architect,task-split"}
  - backend: {agent: "Claude Code", cmd: "create FastAPI app skeleton + /health"}
  - devops: {agent: "Claude Code", cmd: "update Makefile to run server"}
  - tester: {agent: "Claude Code", cmd: "smoke test /health"}
  - reviewer: {agent: "Claude Code", mode: "static review + self-critique"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

```yaml
title: "/api/top-stocks endpoint + models + ranking"
repo: "github.com/demo/top5-sharpe"
branch: "feat/api-top-stocks"
acceptance_criteria:
  - "GET /api/top-stocks?count=5&period=5y&rf=0.015&universe=sp500 returns JSON list with ticker, name, sharpe, last_price, ret_1y"
  - "Response time ≤5s cold, ≤2s warm for S&P500 universe"
cos: Standard
definition_of_done:
  - "Pydantic models; error handling for invalid params/timeouts"
  - "Integration test green on CI"
agent_sequence:
  - planner: {tooling: "MCP:architect,task-split"}
  - backend: {agent: "Claude Code", cmd: "implement endpoint wiring adapter+sharpe engine + in-process cache"}
  - tester: {agent: "Claude Code", cmd: "author integration tests for happy/edge cases"}
  - reviewer: {agent: "Claude Code", mode: "static review + self-critique"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

```yaml
title: "/api/price-series/:ticker for sparkline"
repo: "github.com/demo/top5-sharpe"
branch: "feat/api-price-series"
acceptance_criteria:
  - "GET /api/price-series/:ticker?period=5y returns compact timeseries (date, adj_close)"
  - "Handles missing ticker with 404 + error message"
cos: Standard
definition_of_done:
  - "Endpoint documented; unit tests for serialization"
  - "Cache layer reused from adapter"
agent_sequence:
  - planner: {tooling: "MCP:architect,task-split"}
  - backend: {agent: "Claude Code", cmd: "add endpoint using adapter cache; compact JSON"}
  - tester: {agent: "Claude Code", cmd: "tests for valid/invalid ticker"}
  - reviewer: {agent: "Claude Code", mode: "static review + self-critique"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

```yaml
title: "Input validation + error paths + logging"
repo: "github.com/demo/top5-sharpe"
branch: "feat/api-validation-logging"
acceptance_criteria:
  - "Validate count (1–50), period (3y/5y), rf (0–0.2); structured error responses"
  - "Request/response logging with correlation id; rate limit placeholder"
cos: Standard
definition_of_done:
  - "Negative tests added; pydantic validation errors mapped"
  - "Logging documented in README"
agent_sequence:
  - planner: {tooling: "MCP:architect,task-split"}
  - backend: {agent: "Claude Code", cmd: "add validators, error mappers, logging middleware"}
  - tester: {agent: "Claude Code", cmd: "negative test cases for invalid inputs"}
  - reviewer: {agent: "Claude Code", mode: "static review + self-critique"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

```yaml
title: "UI scaffold (Node JS + Tailwind)"
repo: "github.com/demo/top5-sharpe"
branch: "feat/ui-scaffold"
acceptance_criteria:
  - "Static index.html with Tailwind; main.js mounted; responsive container"
  - "Build-free dev: open with simple http server"
cos: Standard
definition_of_done:
  - "Basic layout ready; no console errors"
  - "README has 'open UI locally' steps"
agent_sequence:
  - planner: {tooling: "MCP:architect,task-split"}
  - frontend: {agent: "Claude Code", cmd: "create HTML skeleton + Tailwind + main.js wiring"}
  - reviewer: {agent: "Claude Code", mode: "static review + self-critique"}
  - tester: {agent: "Claude Code", cmd: "lint and smoke-load UI"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

```yaml
title: "Fetch & render Top‑5 table + sorting"
repo: "github.com/demo/top5-sharpe"
branch: "feat/ui-top5-table"
acceptance_criteria:
  - "Table shows ticker, name, Sharpe, last price, 1y return; sortable by each column"
  - "Load time ≤2s after API response; loading/empty/error states visible"
cos: Standard
definition_of_done:
  - "No blocking layout shift on initial render"
  - "Manual test against live API passes"
agent_sequence:
  - planner: {tooling: "MCP:architect,task-split"}
  - frontend: {agent: "Claude Code", cmd: "implement fetch to /api/top-stocks + sortable table"}
  - tester: {agent: "Claude Code", cmd: "frontend smoke test plan + run"}
  - reviewer: {agent: "Claude Code", mode: "static review + self-critique"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

```yaml
title: "Sparkline component (SVG)"
repo: "github.com/demo/top5-sharpe"
branch: "feat/ui-sparkline"
acceptance_criteria:
  - "Per-row SVG sparkline from /api/price-series; downsample for performance"
  - "Accessible: aria-label with last price and 1y delta"
cos: Standard
definition_of_done:
  - "No more than 16ms per render frame on 10 rows"
  - "Works on modern Chrome/Edge"
agent_sequence:
  - planner: {tooling: "MCP:architect,task-split"}
  - frontend: {agent: "Claude Code", cmd: "SVG sparkline util + async data hook"}
  - tester: {agent: "Claude Code", cmd: "perf check on 10–20 rows; a11y audit"}
  - reviewer: {agent: "Claude Code", mode: "static review + self-critique"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

```yaml
title: "RF input + reload + empty/error states"
repo: "github.com/demo/top5-sharpe"
branch: "feat/ui-rf-input-states"
acceptance_criteria:
  - "RF input (0–0.2) bound to API query; debounce 300ms; reloads table"
  - "Explicit messages for empty results, errors; retry button"
cos: Standard
definition_of_done:
  - "Keyboard accessible controls; tab order OK"
  - "Manual error injection shows correct state transitions"
agent_sequence:
  - planner: {tooling: "MCP:architect,task-split"}
  - frontend: {agent: "Claude Code", cmd: "implement RF control + state management"}
  - tester: {agent: "Claude Code", cmd: "frontend smoke for error/empty/loading"}
  - reviewer: {agent: "Claude Code", mode: "static review + self-critique"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

```yaml
title: "Unit tests: Sharpe math (deterministic + randomized)"
repo: "github.com/demo/top5-sharpe"
branch: "test/sharpe-unit"
acceptance_criteria:
  - "Deterministic tests (known arrays) match expected Sharpe values"
  - "Property tests (random walks) produce finite numbers; reject NaN"
cos: Standard
definition_of_done:
  - "Coverage for sharpe utils ≥95%"
  - "CI green"
agent_sequence:
  - planner: {tooling: "MCP:architect,task-split"}
  - tester: {agent: "Claude Code", cmd: "author unit + property tests; run locally"}
  - reviewer: {agent: "Claude Code", mode: "static review + self-critique"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

```yaml
title: "Integration test: /api/top-stocks happy + edge"
repo: "github.com/demo/top5-sharpe"
branch: "test/api-top-stocks-integ"
acceptance_criteria:
  - "Happy path: returns 5 items within ≤5s cold; schema validated"
  - "Edges: invalid count, rf out of range, partial data flagged"
cos: Standard
definition_of_done:
  - "Test suite runnable via make test and CI"
  - "Flaky test tolerance measured; retries configured"
agent_sequence:
  - planner: {tooling: "MCP:architect,task-split"}
  - tester: {agent: "Claude Code", cmd: "write integration tests using test client + fixtures"}
  - reviewer: {agent: "Claude Code", mode: "static review + self-critique"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

```yaml
title: "Accessibility & performance pass (basic)"
repo: "github.com/demo/top5-sharpe"
branch: "chore/a11y-perf"
acceptance_criteria:
  - "Lighthouse: Performance ≥90, Accessibility ≥90 on table view"
  - "No console errors; images/SVGs have accessible names"
cos: Intangible
definition_of_done:
  - "Report attached to PR; items tracked if not fixed"
  - "Simple improvements merged"
agent_sequence:
  - planner: {tooling: "MCP:architect,task-split"}
  - frontend: {agent: "Claude Code", cmd: "apply quick a11y/perf fixes"}
  - tester: {agent: "Claude Code", cmd: "capture Lighthouse report"}
  - reviewer: {agent: "Claude Code", mode: "static review + self-critique"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

```yaml
title: "Dockerfile + docker‑compose + Makefile"
repo: "github.com/demo/top5-sharpe"
branch: "ops/docker-compose"
acceptance_criteria:
  - "Dockerfile builds backend; compose starts API + static UI + volume cache"
  - "make dev/test/run targets documented; .env.sample read by compose"
cos: Standard
definition_of_done:
  - "Cold start ≤60s; /health reachable; UI served"
  - "README includes commands; works on Linux/Mac"
agent_sequence:
  - planner: {tooling: "MCP:architect,task-split"}
  - devops: {agent: "Claude Code", cmd: "write Dockerfile/compose + Makefile targets"}
  - tester: {agent: "Claude Code", cmd: "smoke run compose; verify endpoints"}
  - reviewer: {agent: "Claude Code", mode: "static review + self-critique"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

```yaml
title: "CI stub (GitHub Actions) for lint/test"
repo: "github.com/demo/top5-sharpe"
branch: "ci/gha-lint-test"
acceptance_criteria:
  - "Workflow: on push/PR run lint, unit, integration tests"
  - "Artifacts: test results + coverage uploaded"
cos: Intangible
definition_of_done:
  - "Status badges in README"
  - "CI runs under 10 minutes"
agent_sequence:
  - planner: {tooling: "MCP:architect,task-split"}
  - devops: {agent: "Claude Code", cmd: "create GitHub Actions workflow for Python+frontend"}
  - tester: {agent: "Claude Code", cmd: "ensure tests deterministic on CI"}
  - reviewer: {agent: "Claude Code", mode: "static review + self-critique"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

```yaml
title: "README with setup, .env, curl examples, screenshots"
repo: "github.com/demo/top5-sharpe"
branch: "docs/readme"
acceptance_criteria:
  - "Local + Docker setup steps; env vars documented with .env.sample"
  - "Example curl for /api/top-stocks and /api/price-series; screenshots of UI"
cos: Intangible
definition_of_done:
  - "README passes link check; screenshots in /docs"
  - "Quickstart reproduces in <15 min"
agent_sequence:
  - planner: {tooling: "MCP:architect,task-split"}
  - reviewer: {agent: "Claude Code", mode: "static review + self-critique"}
  - devops: {agent: "Claude Code", cmd: "validate quickstart on clean environment"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

```yaml
title: "Licensing & repo hygiene (.gitignore, CODEOWNERS)"
repo: "github.com/demo/top5-sharpe"
branch: "chore/repo-hygiene"
acceptance_criteria:
  - "Add MIT license; .gitignore (Python, node, docker); CODEOWNERS assigns review"
  - "PR template with AC/DoD checklist"
cos: Intangible
definition_of_done:
  - "Files in place; CI respects CODEOWNERS"
  - "Template used by next PR"
agent_sequence:
  - planner: {tooling: "MCP:architect,task-split"}
  - devops: {agent: "Claude Code", cmd: "add hygiene files + PR template"}
  - reviewer: {agent: "Claude Code", mode: "static review + self-critique"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

```yaml
title: "Security review (secrets, rate limits)"
repo: "github.com/demo/top5-sharpe"
branch: "sec/review-basics"
acceptance_criteria:
  - "No secrets in repo; .env only; add simple rate limit middleware stub"
  - "Dependency scan output attached"
cos: Standard
definition_of_done:
  - "Security checklist completed"
  - "Issues raised as follow-up tickets if needed"
agent_sequence:
  - planner: {tooling: "MCP:architect,task-split"}
  - devops: {agent: "Claude Code", cmd: "enable basic rate limit; run dep scan"}
  - reviewer: {agent: "Claude Code", mode: "static review + self-critique"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

```yaml
title: "Observability hooks (basic logging metrics)"
repo: "github.com/demo/top5-sharpe"
branch: "feat/observability-hooks"
acceptance_criteria:
  - "Log request latencies; cache hit/miss metrics; simple /metrics JSON"
  - "Sample dashboard JSON or documentation"
cos: Standard
definition_of_done:
  - "Metrics visible locally; docs updated"
  - "Perf budget tracked in README"
agent_sequence:
  - planner: {tooling: "MCP:architect,task-split"}
  - backend: {agent: "Claude Code", cmd: "emit timing + cache metrics; add /metrics"}
  - tester: {agent: "Claude Code", cmd: "verify metrics fields present under load"}
  - reviewer: {agent: "Claude Code", mode: "static review + self-critique"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

# Design/Decompose — WIP 2

```yaml
title: "Service design: adapter ↔ sharpe ↔ API"
repo: "github.com/demo/top5-sharpe"
branch: "design/service-wiring"
acceptance_criteria:
  - "Sequence diagram and interfaces for adapter, sharpe utils, API services"
  - "Identify data contracts and caching boundaries"
cos: Standard
definition_of_done:
  - "Diagram committed under /docs; tasks updated if contracts change"
  - "Stakeholder review note attached"
agent_sequence:
  - planner: {tooling: "MCP:architect,task-split"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

```yaml
title: "Frontend interaction flow (states + API)"
repo: "github.com/demo/top5-sharpe"
branch: "design/frontend-flow"
acceptance_criteria:
  - "State diagram: loading/empty/error/success; RF input interactions defined"
  - "API contracts mapped to UI rendering"
cos: Standard
definition_of_done:
  - "Diagram and checklist in /docs"
  - "No open questions for UI build"
agent_sequence:
  - planner: {tooling: "MCP:architect,task-split"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

# Build: Generate — WIP 3

```yaml
title: "Backend performance tune (cache warm path)"
repo: "github.com/demo/top5-sharpe"
branch: "perf/cache-warm"
acceptance_criteria:
  - "Warm cache routine for top 200 tickers at startup behind flag"
  - "Warm hit reduces /api/top-stocks latency by ≥40% vs cold"
cos: Intangible
definition_of_done:
  - "Benchmark before/after committed"
  - "Flag documented; default off"
agent_sequence:
  - backend: {agent: "Claude Code", cmd: "implement optional warm-cache routine"}
  - tester: {agent: "Claude Code", cmd: "benchmark latency cold vs warm"}
  - reviewer: {agent: "Claude Code", mode: "static review + self-critique"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

# Review — WIP 2

```yaml
title: "Cross-module review: data correctness"
repo: "github.com/demo/top5-sharpe"
branch: "review/data-correctness"
acceptance_criteria:
  - "Verify adjusted close usage end-to-end; confirm ≥3y requirement honored"
  - "Spot-check 5 random tickers for consistency"
cos: Standard
definition_of_done:
  - "Review notes committed; issues filed if discrepancies"
  - "Green light to proceed to Test"
agent_sequence:
  - reviewer: {agent: "Claude Code", mode: "static review + self-critique"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

# Test — WIP 2

```yaml
title: "Frontend smoke on Docker preview"
repo: "github.com/demo/top5-sharpe"
branch: "test/frontend-smoke-docker"
acceptance_criteria:
  - "Open UI via compose; table renders; sorting works; RF input triggers reload"
  - "No uncaught promise rejections"
cos: Standard
definition_of_done:
  - "Test notes and screenshots attached"
  - "Issues created for any defects"
agent_sequence:
  - tester: {agent: "Claude Code", cmd: "run smoke steps; capture evidence"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

# Integrate/Release

```yaml
title: "Tag v0.1.0 and publish demo artifacts"
repo: "github.com/demo/top5-sharpe"
branch: "release/v0.1.0"
acceptance_criteria:
  - "Git tag v0.1.0; attach README quickstart, screenshots, sample responses"
  - "Compose up works from clean clone"
cos: Standard
definition_of_done:
  - "Release notes in /docs/releases"
  - "Stakeholder sign-off recorded"
agent_sequence:
  - devops: {agent: "Claude Code", cmd: "create tag + draft release notes + verify compose"}
  - reviewer: {agent: "Claude Code", mode: "static review + self-critique"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

# Done

```yaml
title: "Kanban policy posted (WIP, pull, classes of service)"
repo: "github.com/demo/top5-sharpe"
branch: "policy/board-rules"
acceptance_criteria:
  - "Board displays WIP limits and pull criteria in header"
  - "Classes of Service lanes documented"
cos: Intangible
definition_of_done:
  - "Policies committed to /docs/policies.md"
  - "Team acknowledges in standup"
agent_sequence:
  - planner: {tooling: "MCP:architect,task-split"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

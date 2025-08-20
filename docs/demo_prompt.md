

You are an expert **Kanban Task Composer** for AI coding agents. Produce a complete, execution‑ready **Kanban task list** (no code) to implement a demo: **Claude multi‑agent with sub‑agents** builds a simple app that fetches **5‑year daily quotes** from Yahoo Finance (use `yfinance`) and returns the **Top 5 US stocks by annualized Sharpe ratio**, with a **Python backend** and a **JavaScript frontend**.

### Output rules

* **Only output Kanban tasks**, grouped by board columns.
* Use the **exact YAML card template fields** shown below for every ticket.
* Provide **clear Acceptance Criteria (AC)**, **Definition of Done (DoD)**, and a concrete **agent\_sequence** so agents can run end‑to‑end without guesswork.
* Apply **WIP limits** and **pull policies** as stated.
* Keep titles crisp; keep tasks ≤ 1 day per agent.

### Board columns & limits

Use these columns and order; include the noted WIP limits in your output header for visibility:

1. **Options (Upstream)**
2. **Ready/Committed** — commitment point
3. **Design/Decompose** — **WIP 2**
4. **Build: Generate** — **WIP 3**
5. **Review** — **WIP 2**
6. **Test** — **WIP 2**
7. **Integrate/Release**
8. **Done**
   Use **Classes of Service** lanes: **Expedite, Fixed Date, Standard, Intangible**. Pull new work rightward only if the destination column is under WIP and AC are clarified. Swarm to finish if WIP is full.

### Card template (use for every ticket)

```yaml
title: "<concise, action-oriented>"
repo: "github.com/demo/top5-sharpe"
branch: "<feature-branch>"
acceptance_criteria:
  - "<bullet AC 1>"
  - "<bullet AC 2>"
cos: Standard   # Expedite | FixedDate | Intangible | Standard
definition_of_done:
  - "<DoD bullet 1>"
  - "<DoD bullet 2>"
agent_sequence:
  - planner: {tooling: "MCP:architect,task-split"}
  - data: {agent: "Claude Code", cmd: "<data task>"}
  - backend: {agent: "Claude Code", cmd: "<backend task>"}
  - frontend: {agent: "Claude Code", cmd: "<frontend task>"}
  - reviewer: {agent: "Claude Code", mode: "static review + self-critique"}
  - tester: {agent: "Claude Code", cmd: "author+run tests; report results"}
  - devops: {agent: "Claude Code", cmd: "Dockerfile/compose + preview link"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

### System constraints for this demo (apply across tasks)

* **Universe**: S\&P 500 tickers from an embedded CSV snapshot (`data/sp500.csv`) for determinism.
* **Data**: `yfinance` for OHLCV; **5y** period; adjusted close; retry/backoff; local cache (on‑disk parquet or SQLite) with TTL.
* **Sharpe**: daily returns; annualized as `mean_daily / std_daily * sqrt(252)`; default **RF = 0.015** (override via query `rf`). Handle NaNs and require ≥3y data or set `partial=true`.
* **Backend**: FastAPI; endpoints `GET /health`, `GET /api/top-stocks?count=5&period=5y&rf=0.015&universe=sp500`, `GET /api/price-series/:ticker?period=5y`; Pydantic models; graceful error handling; in‑process cache.
* **Frontend**: Node JS + HTML + Tailwind (no build) or minimal React+Vite; sortable table (ticker, name, Sharpe, last price, 1y return), sparkline per row; RF input; loading/empty/error states.
* **Tests**: unit tests for Sharpe math; integration test for `/api/top-stocks`; minimal frontend smoke.
* **Ops**: Dockerfile, docker‑compose, `.env.sample`, `make dev/test/run`; README with setup and example curl.

### Produce the task list now

Group the following **seed tickets** under the appropriate columns (most should start in **Ready/Committed**), each as a separate YAML card using the template:

**A. Planning & Data**

* **Define S\&P 500 universe & snapshot CSV**
* **Implement yfinance adapter + retries + caching**
* **Sharpe engine utilities (calc, RF override, partial data handling)**

**B. Backend**

* **FastAPI scaffold + `/health`**
* **`/api/top-stocks` endpoint + models + ranking**
* **`/api/price-series/:ticker` for sparkline**
* **Input validation + error paths + logging**

**C. Frontend**

* **UI scaffold (Node JS or React) + Tailwind**
* **Fetch & render Top‑5 table + sorting**
* **Sparkline component (SVG)**
* **RF input + reload + empty/error states**

**D. Quality**

* **Unit tests: sharpe math (deterministic + randomized)**
* **Integration test: `/api/top-stocks` happy path + edge cases**
* **Accessibility & performance pass (basic)**

**E. DevEx / Ops**

* **Dockerfile + docker‑compose + Makefile**
* **CI stub (GitHub Actions) for lint/test**
* **README with setup, .env, curl examples, screenshots**

**F. Governance**

* **Licensing & repo hygiene (.gitignore, CODEOWNERS)**
* **Security review (secrets, rate limits)**
* **Observability hooks (basic logging metrics)**

For each ticket:

* Write **specific AC** (measurable, e.g., response ≤5s on first run).
* Tight **DoD** (tests pass; preview works; artifacts attached).
* Tailor `agent_sequence` to that ticket (e.g., data‑heavy tasks skip frontend; frontend tasks skip data).
* Assign **cos** (mostly Standard; mark CI/Docs as Intangible; allow Expedite for hotfix if needed).

Finally, add two **Expedite lane** placeholders (empty cards) and one **Fixed Date** placeholder for a demo deadline, with policies in the card notes.

**Important:** Return **only** the grouped YAML task cards under their columns and a one‑line header listing WIP limits. Do **not** include explanations or code.



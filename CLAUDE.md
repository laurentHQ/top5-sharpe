# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Kanban-driven demonstration project** for building a **Top 5 US Stocks by Sharpe Ratio** application using Claude Code multi-agent orchestration. The system fetches 5-year daily quotes from Yahoo Finance and calculates annualized Sharpe ratios for S&P 500 stocks.

## Architecture & Design

### Multi-Agent Development Pattern
This project follows a **Kanban task composition** approach with defined agent sequences:
- **planner**: Uses `MCP:architect,task-split` for task decomposition
- **data**: Handles data fetching, processing, and storage
- **backend**: Implements API endpoints and business logic
- **frontend**: Builds user interface components
- **reviewer**: Performs static review and self-critique
- **tester**: Authors and runs tests, reports results
- **devops**: Handles containerization and deployment

### System Architecture
- **Backend**: FastAPI with Python
- **Frontend**: Node.js + HTML + Tailwind CSS (no build step) or minimal React+Vite
- **Data Source**: Yahoo Finance via `yfinance` library
- **Data Storage**: Local cache (on-disk Parquet or SQLite) with TTL
- **Universe**: S&P 500 tickers from embedded CSV snapshot (`data/sp500.csv`)

### Core Components
1. **Data Layer**: yfinance adapter with retry/backoff and caching
2. **Calculation Engine**: Sharpe ratio utilities with NaN handling
3. **API Layer**: FastAPI endpoints with Pydantic models
4. **UI Layer**: Responsive table with sorting and sparklines
5. **Caching**: In-process cache with configurable TTL

## Development Workflow

### Kanban Board Structure
The project uses strict WIP limits and pull policies:
- **Design/Decompose**: WIP 2
- **Build: Generate**: WIP 3  
- **Review**: WIP 2
- **Test**: WIP 2

### Classes of Service
- **Expedite**: Production hotfixes and security incidents (reserved placeholders)
- **FixedDate**: Live demo day releases
- **Standard**: Feature development
- **Intangible**: Documentation, CI/CD, governance

### Task Management
Each task includes:
- Clear **Acceptance Criteria** with measurable outcomes
- **Definition of Done** with validation requirements
- Specific **agent_sequence** for execution
- **Pull policy**: "Move right only if WIP < limit and AC clarified"

## API Specifications

### Endpoints
- `GET /health` - Health check returning `{status: 'ok', version}`
- `GET /api/top-stocks?count=5&period=5y&rf=0.015&universe=sp500` - Top stocks by Sharpe ratio
- `GET /api/price-series/:ticker?period=5y` - Price series for sparklines

### Performance Requirements
- `/api/top-stocks`: ≤5s cold start, ≤2s warm
- Frontend rendering: ≤2s after API response
- Sparkline rendering: ≤16ms per frame for 10 rows

### Data Requirements
- **Sharpe Calculation**: `mean_daily / std_daily * sqrt(252)`
- **Risk-Free Rate**: Default 0.015, overrideable via `rf` parameter
- **Data Requirements**: ≥3 years of data, else mark `partial=true`
- **Universe**: S&P 500 from deterministic CSV snapshot

## Key Development Commands

*Note: This is a planning/documentation repository. No build commands exist yet as implementation follows the Kanban task sequence.*

Expected commands after implementation:
```bash
# Development
make dev          # Start development server
make test         # Run test suite  
make run          # Run production build

# Docker
docker-compose up # Start full stack
```

## Quality Standards

### Testing Requirements
- **Unit Tests**: ≥95% coverage for Sharpe utilities, property-based tests for stability
- **Integration Tests**: Happy path and edge cases for `/api/top-stocks`
- **Frontend Tests**: Smoke tests for UI interactions

### Performance Budgets
- **Load Time**: <3s on 3G, <1s on WiFi
- **Bundle Size**: <500KB initial, <2MB total
- **API Response**: <5s cold, <2s warm
- **Cache Hit Rate**: Logged and monitored

### Accessibility & Performance
- **Lighthouse Scores**: Performance ≥90, Accessibility ≥90
- **WCAG Compliance**: Aria labels for sparklines, keyboard navigation
- **Error Handling**: Graceful degradation with retry mechanisms

## Documentation Requirements

### Required Artifacts
- **README**: Setup instructions, API examples, curl samples
- **Screenshots**: UI examples in `/docs`
- **Environment**: `.env.sample` with documented variables
- **Sequence Diagrams**: Service interactions under `/docs`

### Security & Compliance
- **No Secrets**: Environment variables only, never in code
- **Rate Limiting**: Basic middleware implementation
- **Dependency Scanning**: Security review process
- **License**: MIT with proper attribution

## File Organization

```
/docs/               # Documentation and planning
  demo_plan.md       # Complete Kanban task breakdown
  demo_prompt.md     # Original requirements specification
/data/               # (Planned) S&P 500 universe CSV
/backend/            # (Planned) FastAPI application
/frontend/           # (Planned) UI components
/tests/              # (Planned) Test suites
docker-compose.yml   # (Planned) Container orchestration
Makefile            # (Planned) Development commands
```

## Development Notes

This project serves as a demonstration of:
- **Multi-agent coordination** in software development
- **Kanban methodology** applied to AI-driven development
- **Test-driven development** with comprehensive coverage requirements
- **Performance-conscious design** with specific SLAs and budgets
- **Production-ready practices** including security, observability, and deployment automation

The implementation follows strict quality gates and validation cycles, with each task having clear acceptance criteria and definition of done requirements before progression through the Kanban board.
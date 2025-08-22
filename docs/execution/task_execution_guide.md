# Task Execution Guide - Multi-Agent Kanban Workflow

This guide provides step-by-step instructions for executing tasks imported from `/create-kanban-tasks` command with optimal parallel workflows and agent coordination.

## Quick Start Execution

### 1. Import Tasks in Correct Order
```bash
# Import all phases with reverse order for proper Kanban stacking
/create-kanban-tasks --all-phases --project-id YOUR_PROJECT_ID --reverse-order --add-phase-prefix --parallel-analysis

# Alternative: Import specific phase
/create-kanban-tasks --phase 01 --project-id YOUR_PROJECT_ID --reverse-order --add-phase-prefix
```

### 2. Verify Task Order in Kanban
After import, your Kanban board should show (top to bottom):
```
📋 TODO Column:
├── 00: Project Planning Tasks
├── 01: Foundation Data Tasks  
├── 02: Backend API Tasks
├── 03: Frontend UI Tasks
├── 04: Testing Validation Tasks
├── 05: Infrastructure Deploy Tasks
├── 06: Documentation Polish Tasks
└── 99: Release Management Tasks
```

## Execution Phases & Parallel Opportunities

### Phase 1: Foundation Setup (Days 1-3)
**Goal**: Establish data infrastructure and calculation engine

#### Parallel Track A (2 agents)
```yaml
agents: [python-backend-expert, data-scientist]
tasks:
  - "01: S&P 500 Universe & Snapshot CSV"
  - "01: Sharpe Engine Utilities" (can run parallel)
dependencies: None
estimated_time: 2-3 days
```

#### Parallel Track B (1 agent - after Track A Task 1)
```yaml
agents: [python-backend-expert]
tasks:
  - "01: yfinance Adapter + Retries + Caching"
dependencies: S&P 500 Universe complete
estimated_time: 2 days
```

#### Success Criteria
- [ ] S&P 500 CSV with 500±10 tickers
- [ ] Sharpe ratio calculations working with test data
- [ ] yfinance adapter with caching and retry logic
- [ ] All unit tests passing (≥95% coverage)

### Phase 2: API Development (Days 4-6)
**Goal**: Build FastAPI application with core endpoints

#### Parallel Track A (1 agent)
```yaml
agents: [python-backend-expert]
tasks:
  - "02: FastAPI Scaffold + Health Endpoint"
dependencies: None (can start in parallel with Foundation)
estimated_time: 1 day
```

#### Parallel Track B (2 agents - after Track A)
```yaml
agents: [python-backend-expert, api-architect]
tasks:
  - "02: /api/top-stocks Endpoint + Models + Ranking"
  - "02: /api/price-series/:ticker for Sparkline"
dependencies: FastAPI scaffold + Foundation data layer
estimated_time: 2-3 days
```

#### Parallel Track C (2 agents - after endpoints)
```yaml
agents: [python-backend-expert, backend-developer]
tasks:
  - "02: Input Validation + Error Paths + Logging"
  - "02: Observability Hooks (Basic Logging Metrics)"
dependencies: Core endpoints functional
estimated_time: 2 days
```

#### Success Criteria
- [ ] Health endpoint responding
- [ ] /api/top-stocks returning ranked data (≤5s cold, ≤2s warm)
- [ ] /api/price-series returning time series data
- [ ] Input validation preventing invalid requests
- [ ] Observability and logging functional

### Phase 3: Frontend + Backend Parallel (Days 5-8)
**Goal**: Build responsive UI while finalizing backend features

#### Parallel Track A (2 agents)
```yaml
agents: [tailwind-frontend-expert, frontend-developer]
tasks:
  - "03: UI Scaffold (Build-free Tailwind)"
  - "03: Fetch & Render Top-5 Table + Sorting"
  - "03: Sparkline Component (SVG)"
dependencies: API endpoints available for testing
estimated_time: 3-4 days
```

#### Parallel Track B (2 agents)
```yaml
agents: [python-backend-expert, backend-developer]
tasks:
  - Continue backend optimization and error handling
  - Performance tuning and caching improvements
dependencies: Core API functionality complete
estimated_time: 2-3 days
```

#### Parallel Track C (1 agent)
```yaml
agents: [test-engineer]
tasks:
  - Begin integration testing with available endpoints
  - Setup testing infrastructure
dependencies: Basic endpoints functional
estimated_time: 2-3 days
```

#### Success Criteria
- [ ] Responsive UI loading and displaying data
- [ ] Table sorting functional
- [ ] Sparklines rendering (≤16ms per frame)
- [ ] Risk-free rate input working with API
- [ ] Loading/error states implemented

### Phase 4: Integration + Polish (Days 7-10)
**Goal**: Complete testing, accessibility, and deployment readiness

#### Parallel Track A (2 agents)
```yaml
agents: [test-engineer, performance-optimizer]
tasks:
  - "04: E2E Test Suite + API Coverage"
  - "04: Performance Testing + Benchmarks"
  - "04: Error Scenarios + Recovery Testing"
dependencies: Complete frontend + backend integration
estimated_time: 3-4 days
```

#### Parallel Track B (2 agents)
```yaml
agents: [accessibility-specialist, frontend-developer]
tasks:
  - "03: Accessibility & Performance Pass"
  - "04: Cross-Browser Compatibility"
  - UI polish and optimization
dependencies: UI components complete
estimated_time: 2-3 days
```

#### Parallel Track C (1 agent)
```yaml
agents: [devops-specialist]
tasks:
  - "05: Docker Setup + Container Deploy"
  - "05: Production Config + Environment"
dependencies: Application functional
estimated_time: 2-3 days
```

#### Success Criteria
- [ ] Lighthouse scores: Performance ≥90, Accessibility ≥90
- [ ] All tests passing (unit, integration, E2E)
- [ ] Cross-browser compatibility verified
- [ ] Docker deployment working
- [ ] Production configuration ready

## Agent Coordination Strategies

### Recommended Agent Assignments

#### Foundation Phase
```yaml
optimal_team:
  - python-backend-expert: Lead on yfinance adapter and Sharpe utilities
  - data-scientist: S&P 500 universe and data validation
  - backend-developer: Service layer integration and testing support
```

#### API Development Phase  
```yaml
optimal_team:
  - python-backend-expert: FastAPI endpoints and Pydantic models
  - api-architect: Endpoint design and validation patterns
  - backend-developer: Middleware, error handling, observability
```

#### Frontend Development Phase
```yaml
optimal_team:
  - tailwind-frontend-expert: UI components and responsive design
  - frontend-developer: JavaScript integration and API calls
  - accessibility-specialist: WCAG compliance and user experience
```

#### Testing & Deployment Phase
```yaml
optimal_team:
  - test-engineer: Comprehensive testing strategy and execution
  - performance-optimizer: Performance testing and optimization
  - devops-specialist: Infrastructure and deployment automation
```

### Communication Protocols

#### Daily Standups
- **Dependencies Check**: Which tasks are blocking others?
- **Parallel Opportunities**: What can be worked on simultaneously?
- **Resource Sharing**: Are there test data or mock services to share?
- **Integration Points**: When will components be ready for integration?

#### Phase Handoffs
- **Completion Criteria**: All acceptance criteria met and verified
- **Documentation**: README and API docs updated
- **Test Coverage**: Minimum thresholds achieved
- **Dependencies**: All blocked tasks unblocked for next phase

## Parallel Execution Best Practices

### Within-Phase Parallelism
1. **Independent Tasks First**: Start tasks with no dependencies
2. **Shared Resources**: Coordinate access to test data and environments
3. **API Contracts**: Establish endpoint contracts early for frontend development
4. **Mock Services**: Use mocking to enable parallel development

### Cross-Phase Parallelism
1. **Early Scaffolding**: Frontend scaffold can start with backend scaffold
2. **Progressive Integration**: Integrate components as soon as basic functionality is available
3. **Continuous Testing**: Begin testing as soon as components are available
4. **Documentation**: Update docs continuously throughout development

### Resource Management
1. **Agent Specialization**: Assign agents to their optimal domains
2. **Load Balancing**: Distribute work evenly across available agents
3. **Conflict Resolution**: Have clear escalation paths for technical decisions
4. **Context Sharing**: Maintain shared understanding of project state

## Quality Gates & Checkpoints

### Phase Completion Criteria
Each phase must meet these criteria before moving to the next:

#### Foundation Complete
- [ ] All data loading components functional
- [ ] Unit tests ≥95% coverage
- [ ] Sharpe calculations verified with known test cases
- [ ] Cache performance benchmarks documented

#### Backend Complete  
- [ ] All API endpoints responding correctly
- [ ] Response time SLAs met (≤5s cold, ≤2s warm)
- [ ] Input validation preventing invalid requests
- [ ] Error handling and logging functional
- [ ] Integration tests passing

#### Frontend Complete
- [ ] UI components responsive across devices
- [ ] API integration functional
- [ ] Loading and error states implemented
- [ ] Basic accessibility requirements met
- [ ] Cross-browser compatibility verified

#### Testing Complete
- [ ] E2E test suite covering critical paths
- [ ] Performance benchmarks documented
- [ ] Security testing completed
- [ ] Accessibility audit passed (≥90 Lighthouse score)
- [ ] Production deployment verified

## Troubleshooting Common Issues

### Dependency Conflicts
**Problem**: Tasks blocked waiting for dependencies
**Solution**: 
- Review dependency graph and identify minimum viable deliverables
- Create mock services or data to unblock dependent tasks
- Parallel track development with integration testing

### Resource Contention
**Problem**: Multiple agents need same resources
**Solution**:
- Implement shared development environment protocols
- Use feature branches for parallel development
- Schedule resource-intensive tasks (like full API testing)

### Integration Issues
**Problem**: Components don't work together as expected
**Solution**:
- Establish clear API contracts early
- Implement contract testing between components
- Regular integration checkpoints during development

### Performance Bottlenecks
**Problem**: System doesn't meet performance requirements
**Solution**:
- Profile early and often during development
- Implement performance budgets and monitoring
- Parallel optimization tracks while continuing feature development

This execution guide ensures efficient parallel development while maintaining quality and coordination across the multi-agent team.
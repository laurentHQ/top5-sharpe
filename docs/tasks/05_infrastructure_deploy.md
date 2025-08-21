# 05 Infrastructure & Deployment Tasks

DevOps and deployment automation tasks that create production-ready infrastructure and CI/CD pipelines. These tasks establish reliable deployment and operational monitoring capabilities.

## Task Group Priority
**Phase**: Infrastructure & Operations
**Dependencies**: Testing validation (04_testing_validation.md)
**Blocks**: Production deployment, monitoring setup
**Estimated Duration**: 3-4 days

---

## Task 1: Docker Compose + Makefile

```yaml
title: "Dockerfile + docker‑compose + Makefile"
repo: "github.com/laurentHQ/top5-sharpe"
branch: "ops/docker-compose"
description: |
  Create containerized deployment setup with Docker Compose for full-stack local development.
  Enables consistent development environment and simplified deployment workflow.
acceptance_criteria:
  - "Dockerfile builds backend; compose starts API + static UI + volume cache"
  - "make dev/test/run targets documented; .env.sample read by compose"
cos: Standard
definition_of_done:
  - "Cold start ≤60s; /health reachable; UI served"
  - "README includes commands; works on Linux/Mac"
todo_list:
  planner:
    - "Design Docker Compose architecture for backend + frontend"
    - "Plan volume strategy for data caching and persistence"
    - "Define environment variable configuration strategy"
    - "Plan Makefile targets for development workflow"
  devops:
    - "Create Dockerfile for FastAPI backend with Python 3.11"
    - "Configure requirements.txt installation and caching"
    - "Create docker-compose.yml with backend and nginx services"
    - "Configure nginx to serve frontend static files"
    - "Set up named volumes for yfinance cache persistence"
    - "Create .env.sample with all configurable variables"
    - "Add health checks for backend service"
    - "Create Makefile with dev, test, run, and clean targets"
    - "Configure hot reload for development mode"
    - "Add network configuration for service communication"
  tester:
    - "Test cold start from clean state measures under 60 seconds"
    - "Verify /health endpoint returns 200 OK"
    - "Test frontend serves correctly at localhost"
    - "Verify environment variable loading from .env"
    - "Test volume persistence across container restarts"
    - "Test Makefile targets work on Linux and Mac"
  reviewer:
    - "Review Dockerfile security best practices"
    - "Validate Docker Compose service configuration"
    - "Check resource limits and health check configuration"
    - "Review Makefile consistency and documentation"
agent_sequence:
  - planner: {tooling: "Sequential MCP + devops-specialist"}
  - devops: {agent: "devops-specialist", cmd: "write Dockerfile/compose + Makefile targets"}
  - tester: {agent: "test-engineer", cmd: "smoke run compose; verify endpoints"}
  - reviewer: {agent: "code-reviewer", mode: "rigorous security-aware review"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

---

## Task 2: CI Pipeline (GitHub Actions)

```yaml
title: "CI stub (GitHub Actions) for lint/test"
repo: "github.com/laurentHQ/top5-sharpe"
branch: "ci/gha-lint-test"
description: |
  Automated CI/CD pipeline for continuous testing and quality assurance.
  Provides automated validation of all pull requests and main branch changes.
acceptance_criteria:
  - "Workflow: on push/PR run lint, unit, integration tests"
  - "Artifacts: test results + coverage uploaded"
cos: Intangible
definition_of_done:
  - "Status badges in README"
  - "CI runs under 10 minutes"
todo_list:
  planner:
    - "Design CI/CD pipeline workflow and stages"
    - "Plan test execution strategy and parallelization"
    - "Define artifact collection and reporting"
    - "Plan status badge integration and documentation"
  devops:
    - "Create .github/workflows/ci.yml workflow file"
    - "Configure Python test environment with matrix testing"
    - "Add linting stage: black, flake8, mypy"
    - "Add unit test stage with coverage reporting"
    - "Add integration test stage with test database"
    - "Configure test artifact collection and upload"
    - "Add frontend linting and basic validation"
    - "Set up caching for dependencies and Docker layers"
    - "Configure workflow triggers: push, PR"
    - "Add status checks and branch protection rules"
  tester:
    - "Verify CI workflow runs complete in under 10 minutes"
    - "Test CI runs successfully on clean repository"
    - "Validate all test stages execute correctly"
    - "Check artifact upload and coverage reporting"
    - "Test branch protection and status checks"
  reviewer:
    - "Review CI workflow security and permissions"
    - "Validate test coverage and quality gates"
    - "Check workflow efficiency and resource usage"
agent_sequence:
  - planner: {tooling: "Sequential MCP + devops-specialist"}
  - devops: {agent: "devops-specialist", cmd: "create GitHub Actions workflow for Python+frontend"}
  - tester: {agent: "test-engineer", cmd: "ensure tests deterministic on CI"}
  - reviewer: {agent: "code-reviewer", mode: "rigorous security-aware review"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

---

## Task 3: Repository Hygiene & Security

```yaml
title: "Licensing & repo hygiene (.gitignore, CODEOWNERS)"
repo: "github.com/laurentHQ/top5-sharpe"
branch: "chore/repo-hygiene"
description: |
  Establish repository governance, security, and maintainability standards.
  Provides proper licensing, code ownership, and security baseline.
acceptance_criteria:
  - "Add MIT license; .gitignore (Python, node, docker); CODEOWNERS assigns review"
  - "PR template with AC/DoD checklist"
cos: Intangible
definition_of_done:
  - "Files in place; CI respects CODEOWNERS"
  - "Template used by next PR"
todo_list:
  planner:
    - "Plan repository governance and file organization"
    - "Define code ownership and review requirements"
    - "Design PR template with quality checklists"
    - "Plan .gitignore strategy for all technologies used"
  devops:
    - "Add MIT LICENSE file with proper copyright"
    - "Create comprehensive .gitignore for Python, Node, Docker"
    - "Add .gitignore entries for IDE files, OS files, cache directories"
    - "Create CODEOWNERS file with review assignments"
    - "Create .github/pull_request_template.md"
    - "Add AC/DoD checklist to PR template"
    - "Create .github/ISSUE_TEMPLATE/ with bug/feature templates"
    - "Add CONTRIBUTING.md with development guidelines"
    - "Configure branch protection with CODEOWNERS enforcement"
  tester:
    - "Verify .gitignore prevents unwanted file commits"
    - "Test CODEOWNERS integration with PR reviews"
    - "Validate PR template appears on new pull requests"
    - "Test issue templates work correctly"
  reviewer:
    - "Review license compatibility and requirements"
    - "Validate .gitignore completeness for project stack"
    - "Check CODEOWNERS accuracy and coverage"
    - "Review PR template usefulness and completeness"
agent_sequence:
  - planner: {tooling: "Sequential MCP + devops-specialist"}
  - devops: {agent: "devops-specialist", cmd: "add hygiene files + PR template"}
  - reviewer: {agent: "code-reviewer", mode: "rigorous security-aware review"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

---

## Task 4: Security Review & Hardening

```yaml
title: "Security review (secrets, rate limits)"
repo: "github.com/laurentHQ/top5-sharpe"
branch: "sec/review-basics"
description: |
  Comprehensive security audit and hardening of the application stack.
  Implements security best practices and validates against common vulnerabilities.
acceptance_criteria:
  - "No secrets in repo; .env only; add simple rate limit middleware stub"
  - "Dependency scan output attached"
cos: Standard
definition_of_done:
  - "Security checklist completed"
  - "Issues raised as follow-up tickets if needed"
todo_list:
  planner:
    - "Design security audit methodology and checklist"
    - "Plan secret management and environment variable strategy"
    - "Define rate limiting approach and configuration"
    - "Plan dependency vulnerability scanning workflow"
  devops:
    - "Audit codebase for hardcoded secrets or sensitive data"
    - "Implement rate limiting middleware with configurable limits"
    - "Add security headers middleware (CORS, CSRF, etc.)"
    - "Run dependency vulnerability scan (safety, npm audit)"
    - "Configure environment variable validation"
    - "Add input sanitization and validation hardening"
    - "Implement request size limits and timeout protection"
    - "Document security configuration in .env.sample"
    - "Create security.md with security reporting guidelines"
  tester:
    - "Test rate limiting functionality under load"
    - "Verify no secrets leak in logs or error messages"
    - "Test security headers are properly set"
    - "Validate input sanitization prevents injection"
  reviewer:
    - "Review security implementation completeness"
    - "Validate rate limiting configuration and defaults"
    - "Check dependency scan results and remediation plan"
    - "Verify secret management practices"
agent_sequence:
  - planner: {tooling: "Sequential MCP + devops-specialist"}
  - devops: {agent: "devops-specialist", cmd: "enable basic rate limit; run dep scan"}
  - reviewer: {agent: "code-reviewer", mode: "rigorous security-aware review"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

---

## Task Group Dependencies

**Requires Stable Application:**
- All testing validation passed (04_testing_validation.md)
- Application functionality verified
- Performance benchmarks met

**Provides Infrastructure For:**
- Reliable development environment
- Automated testing and validation  
- Security baseline and monitoring
- Production deployment readiness

**Quality Gates:**
- Docker containers build and run successfully
- CI pipeline completes all tests in <10 minutes
- Security scan shows no critical vulnerabilities
- All repository files properly configured
- Development workflow documented and tested

**Operational Targets:**
- Container startup time: <60s cold start
- CI pipeline execution: <10 minutes total
- Security scan coverage: 100% of dependencies
- Development setup time: <15 minutes for new contributors
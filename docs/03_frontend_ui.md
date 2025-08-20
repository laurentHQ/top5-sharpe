# 03 Frontend UI Tasks

User interface and interaction tasks that create the visual layer for the Sharpe ratio application. These tasks build the responsive web interface that displays ranked stocks and interactive features.

## Task Group Priority
**Phase**: Frontend Development
**Dependencies**: Backend API tasks (02_backend_api.md)
**Blocks**: End-to-end testing, accessibility validation
**Estimated Duration**: 5-7 days

---

## Task 1: UI Scaffold (Build-free Tailwind)

```yaml
title: "UI scaffold (Node JS + Tailwind)"
repo: "github.com/laurentHQ/top5-sharpe"
branch: "feat/ui-scaffold"
description: |
  Create the foundational frontend structure using build-free Tailwind CSS and vanilla JavaScript.
  Establishes responsive layout and development workflow without complex build tools.
acceptance_criteria:
  - "Static index.html with Tailwind; main.js mounted; responsive container"
  - "Build-free dev: open with simple http server"
cos: Standard
definition_of_done:
  - "Basic layout ready; no console errors"
  - "README has 'open UI locally' steps"
todo_list:
  planner:
    - "Design build-free frontend architecture with CDN Tailwind"
    - "Plan responsive layout structure and component organization"
    - "Define development workflow without build step"
    - "Plan JavaScript module organization and loading"
  frontend:
    - "Create frontend/ directory structure"
    - "Create index.html with Tailwind CSS CDN link"
    - "Add responsive container with mobile-first design"
    - "Create main.js with basic app initialization"
    - "Add header section with title and description"
    - "Create placeholder sections for table and controls"
    - "Add meta tags for responsive viewport"
    - "Style with Tailwind utility classes for clean layout"
    - "Add basic error boundary and loading states"
  reviewer:
    - "Review HTML semantic structure and accessibility"
    - "Validate Tailwind CSS integration and responsive design"
    - "Check JavaScript module organization"
  tester:
    - "Test loading in multiple browsers (Chrome, Firefox, Safari)"
    - "Verify responsive design at mobile, tablet, desktop sizes"
    - "Check console for errors and warnings"
    - "Test with simple HTTP server (python -m http.server)"
agent_sequence:
  - planner: {tooling: "Sequential MCP + tech-lead-orchestrator"}
  - frontend: {agent: "tailwind-frontend-expert", cmd: "create HTML skeleton + Tailwind + main.js wiring"}
  - reviewer: {agent: "code-reviewer", mode: "rigorous security-aware review"}
  - tester: {agent: "test-engineer", cmd: "lint and smoke-load UI"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

---

## Task 2: Fetch & Render Top-5 Table + Sorting

```yaml
title: "Fetch & render Top‑5 table + sorting"
repo: "github.com/laurentHQ/top5-sharpe"
branch: "feat/ui-top5-table"
description: |
  Implement the core data table that fetches and displays ranked stocks with interactive sorting.
  This is the primary user interface that presents the Sharpe ratio analysis results.
acceptance_criteria:
  - "Table shows ticker, name, Sharpe, last price, 1y return; sortable by each column"
  - "Load time ≤2s after API response; loading/empty/error states visible"
cos: Standard
definition_of_done:
  - "No blocking layout shift on initial render"
  - "Manual test against live API passes"
todo_list:
  planner:
    - "Design table component with sortable columns"
    - "Plan loading states and error handling UX"
    - "Define data fetching strategy and caching"
    - "Plan responsive table design for mobile"
  frontend:
    - "Create table.js module for table component"
    - "Implement fetchTopStocks() API call function"
    - "Create renderTable() with sortable column headers"
    - "Add loading spinner during API calls"
    - "Implement column sorting by ticker, Sharpe, price, return"
    - "Format numbers: Sharpe (2 decimals), price ($), return (%)"
    - "Add empty state message when no data"
    - "Add error state with retry button"
    - "Style table with Tailwind for responsive design"
    - "Add click handlers for column sorting"
    - "Implement sort indicators (arrows) in headers"
  tester:
    - "Test table rendering with mock data"
    - "Test all column sorting functionality"
    - "Test loading states and error handling"
    - "Verify responsive design on different screen sizes"
    - "Test against live API with network throttling"
  reviewer:
    - "Review component architecture and separation of concerns"
    - "Validate accessibility and keyboard navigation"
    - "Check performance and rendering optimization"
agent_sequence:
  - planner: {tooling: "Sequential MCP + frontend-developer"}
  - frontend: {agent: "tailwind-frontend-expert", cmd: "implement fetch to /api/top-stocks + sortable table"}
  - tester: {agent: "test-engineer", cmd: "frontend smoke test plan + run"}
  - reviewer: {agent: "code-reviewer", mode: "rigorous security-aware review"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

---

## Task 3: Sparkline Component (SVG)

```yaml
title: "Sparkline component (SVG)"
repo: "github.com/laurentHQ/top5-sharpe"
branch: "feat/ui-sparkline"
description: |
  Create compact SVG sparklines that show price trends for each stock in the ranking table.
  Provides visual context for stock performance alongside numerical Sharpe ratios.
acceptance_criteria:
  - "Per-row SVG sparkline from /api/price-series; downsample for performance"
  - "Accessible: aria-label with last price and 1y delta"
cos: Standard
definition_of_done:
  - "No more than 16ms per render frame on 10 rows"
  - "Works on modern Chrome/Edge"
todo_list:
  planner:
    - "Design SVG sparkline component interface and sizing"
    - "Plan data downsampling strategy for performance"
    - "Define accessibility requirements and ARIA labels"
    - "Plan integration with table rows and async loading"
  frontend:
    - "Create sparkline.js module with SVG generation"
    - "Implement createSparkline(data, width, height) function"
    - "Add data downsampling to ~50 points for performance"
    - "Create SVG path generation from price data"
    - "Add accessibility with meaningful aria-label"
    - "Implement async loading from /api/price-series"
    - "Add loading placeholder and error states for sparklines"
    - "Style sparklines with consistent colors and sizing"
    - "Optimize rendering to stay under 16ms per frame"
  tester:
    - "Benchmark rendering performance with 10+ sparklines"
    - "Test accessibility with screen readers"
    - "Verify sparklines update correctly with new data"
    - "Test error handling for failed price-series calls"
    - "Validate sparkline accuracy against raw data"
  reviewer:
    - "Review SVG generation efficiency and accuracy"
    - "Validate accessibility implementation"
    - "Check performance optimization and frame timing"
agent_sequence:
  - planner: {tooling: "Sequential MCP + frontend-developer"}
  - frontend: {agent: "tailwind-frontend-expert", cmd: "SVG sparkline util + async data hook"}
  - tester: {agent: "accessibility-specialist", cmd: "perf check on 10–20 rows; a11y audit"}
  - reviewer: {agent: "code-reviewer", mode: "rigorous security-aware review"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

---

## Task 4: Risk-Free Rate Input + Reload + States

```yaml
title: "RF input + reload + empty/error states"
repo: "github.com/laurentHQ/top5-sharpe"
branch: "feat/ui-rf-input-states"
description: |
  Add interactive risk-free rate control that allows users to adjust calculations dynamically.
  Implements comprehensive state management for all UI interaction scenarios.
acceptance_criteria:
  - "RF input (0–0.2) bound to API query; debounce 300ms; reloads table"
  - "Explicit messages for empty results, errors; retry button"
cos: Standard
definition_of_done:
  - "Keyboard accessible controls; tab order OK"
  - "Manual error injection shows correct state transitions"
todo_list:
  planner:
    - "Design risk-free rate input control and validation"
    - "Plan state management for loading/error/empty scenarios"
    - "Define debouncing strategy for API calls"
    - "Plan keyboard accessibility and focus management"
  frontend:
    - "Create controls.js module for input management"
    - "Implement risk-free rate input with validation (0.0-0.2)"
    - "Add debouncing (300ms) to prevent excessive API calls"
    - "Wire RF input to trigger table reload with new parameter"
    - "Implement comprehensive state management:"
    - "- Loading state: show spinner, disable input"
    - "- Error state: show error message, retry button"
    - "- Empty state: show 'no results' message"
    - "- Success state: show data table normally"
    - "Add keyboard navigation and proper tab order"
    - "Style states with consistent Tailwind classes"
    - "Add input validation feedback (invalid range)"
  tester:
    - "Test RF input validation with edge cases (negative, >0.2)"
    - "Test debouncing prevents rapid API calls"
    - "Test all state transitions (loading → success/error)"
    - "Test keyboard navigation and accessibility"
    - "Test retry button functionality after errors"
    - "Simulate network errors and verify error states"
  reviewer:
    - "Review state management logic and transitions"
    - "Validate input validation and user feedback"
    - "Check accessibility and keyboard navigation"
agent_sequence:
  - planner: {tooling: "Sequential MCP + frontend-developer"}
  - frontend: {agent: "tailwind-frontend-expert", cmd: "implement RF control + state management"}
  - tester: {agent: "test-engineer", cmd: "frontend smoke for error/empty/loading"}
  - reviewer: {agent: "code-reviewer", mode: "rigorous security-aware review"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

---

## Task 5: Accessibility & Performance Pass

```yaml
title: "Accessibility & performance pass (basic)"
repo: "github.com/laurentHQ/top5-sharpe"
branch: "chore/a11y-perf"
description: |
  Comprehensive accessibility audit and performance optimization for the complete UI.
  Ensures WCAG compliance and meets performance budgets across all components.
acceptance_criteria:
  - "Lighthouse: Performance ≥90, Accessibility ≥90 on table view"
  - "No console errors; images/SVGs have accessible names"
cos: Intangible
definition_of_done:
  - "Report attached to PR; items tracked if not fixed"
  - "Simple improvements merged"
todo_list:
  planner:
    - "Plan comprehensive accessibility audit strategy"
    - "Define performance budget validation approach"
    - "Plan Lighthouse testing across different scenarios"
    - "Define accessibility compliance checklist"
  frontend:
    - "Run comprehensive Lighthouse audit on complete UI"
    - "Fix accessibility issues: missing ARIA labels, focus management"
    - "Add proper semantic HTML structure and landmarks"
    - "Optimize image loading and SVG accessibility"
    - "Implement keyboard navigation improvements"
    - "Add skip links for keyboard users"
    - "Ensure color contrast meets WCAG AA standards"
    - "Optimize JavaScript bundle size and loading"
    - "Add proper loading states and progress indicators"
  tester:
    - "Run automated accessibility testing (axe-core)"
    - "Test with screen readers (NVDA/JAWS)"
    - "Validate keyboard-only navigation through all features"
    - "Test performance across different network conditions"
    - "Capture Lighthouse scores for documentation"
  reviewer:
    - "Review accessibility improvements and compliance"
    - "Validate performance optimizations effectiveness"
    - "Check that fixes don't break existing functionality"
agent_sequence:
  - planner: {tooling: "Sequential MCP + accessibility-specialist"}
  - frontend: {agent: "accessibility-specialist", cmd: "apply quick a11y/perf fixes"}
  - tester: {agent: "performance-optimizer", cmd: "capture Lighthouse report"}
  - reviewer: {agent: "code-reviewer", mode: "rigorous security-aware review"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

---

## Task Group Dependencies

**Requires API Foundation:**
- All backend API endpoints functional (02_backend_api.md)
- Data models and validation working
- Performance targets met by backend

**Provides User Interface For:**
- Stock ranking visualization
- Interactive risk-free rate adjustment
- Historical price trend sparklines
- Responsive design across devices

**Quality Gates:**
- Lighthouse Performance ≥90, Accessibility ≥90
- No console errors or warnings
- Responsive design works on mobile/tablet/desktop
- Keyboard navigation fully functional
- Loading states provide clear user feedback
- Error handling with recovery options

**Performance Targets:**
- Initial page load: <3s on 3G
- Table render after API response: <2s
- Sparkline rendering: <16ms per frame
- RF input debounce: 300ms delay
- Memory usage: <50MB for UI components
- Bundle size: <500KB initial load
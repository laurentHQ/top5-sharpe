# /create-kanban-tasks - Import Task Templates to Vibe Kanban

Import structured task templates into Vibe Kanban boards for execution and progress tracking. This command analyzes task files, applies execution-order sorting, and creates numbered tasks with phase identification for streamlined development workflow.

## Command Usage

```
/create-kanban-tasks [template-file] [options]
```

## Arguments

| Argument | Description | Default | Examples |
|----------|-------------|---------|-----------|
| `template-file` | Path to task template file | `docs/tasks/*.md` | `docs/tasks/01_foundation_data.md` |

## Options

| Flag | Description | Default | Values |
|------|-------------|---------|---------|
| `--project-id` | Vibe Kanban project ID | Auto-detect or prompt | Project UUID from Kanban board |
| `--status` | Initial task status | `todo` | `todo`, `inprogress`, `inreview`, `done` |
| `--batch-size` | Tasks per batch import | `10` | Number of tasks to import at once |
| `--dry-run` | Preview without creating | `false` | `true`, `false` |
| `--all-phases` | Import all phase files | `false` | Import entire `docs/tasks/` directory |
| `--phase` | Specific phase to import | None | Phase number like `01`, `02`, etc. |
| `--reverse-order` | Import in reverse execution order | `true` | `true`, `false` - Last tasks first for proper Kanban stack |
| `--add-phase-prefix` | Add phase number to task titles | `true` | `true`, `false` - Enables "01: Task Name" format |
| `--parallel-analysis` | Analyze parallel execution opportunities | `true` | `true`, `false` - Generate parallel execution docs |
| `--skip-duplicates` | Skip tasks that already exist in Kanban | `true` | `true`, `false` - Prevents duplicate task creation |
| `--duplicate-check` | Method for detecting duplicate tasks | `title` | `title`, `title-exact`, `description`, `smart` |
| `--force-import` | Import even if duplicates detected | `false` | `true`, `false` - Override duplicate prevention |
| `--update-existing` | Update existing tasks instead of skipping | `false` | `true`, `false` - Merge template with existing tasks |

## Examples

### Import Single Phase
```
/create-kanban-tasks docs/tasks/01_foundation_data.md --project-id abc123
```
Creates all tasks from the foundation data phase in the specified Kanban project.

### Import All Phases
```
/create-kanban-tasks --all-phases --project-id abc123 --status todo
```
Imports all task phases from `docs/tasks/` directory into the Kanban board.

### Dry Run Preview
```
/create-kanban-tasks docs/tasks/02_backend_api.md --project-id abc123 --dry-run
```
Shows what tasks would be created without actually importing them.

### Import Specific Phase by Number
```
/create-kanban-tasks --phase 03 --project-id abc123
```
Imports tasks from `docs/tasks/03_frontend_ui.md`.

### Batch Import with Custom Status
```
/create-kanban-tasks --all-phases --project-id abc123 --status todo --batch-size 5
```
Imports all phases in batches of 5 tasks, setting initial status to `todo`.

### Skip Duplicate Tasks (Safe Import)
```
/create-kanban-tasks --all-phases --project-id abc123 --skip-duplicates --duplicate-check smart
```
Imports all phases while automatically skipping tasks that already exist in the Kanban board.

### Force Import with Duplicate Override
```
/create-kanban-tasks --phase 02 --project-id abc123 --force-import --duplicate-check title
```
Forces import of phase 02 tasks even if similar tasks already exist.

### Update Existing Tasks
```
/create-kanban-tasks --phase 01 --project-id abc123 --update-existing --duplicate-check title-exact
```
Updates existing tasks with new template content instead of creating duplicates.

## What This Command Does

### 1. Task Structure Analysis & Discovery
- **Scan all task files** in `docs/tasks/` directory to understand complete project structure
- **Parse YAML frontmatter** from task template files with comprehensive validation
- **Extract task definitions** with titles, descriptions, and acceptance criteria
- **Identify task relationships** and dependencies between phases
- **Map agent sequences** to task metadata for execution planning
- **Validate task structure** for Kanban compatibility and completeness
- **Analyze execution dependencies** to determine proper import order
- **Detect parallel execution opportunities** within and across phases

### 2. Project Validation & Duplicate Detection
- **List available projects** using `mcp__vibe_kanban__list_projects`
- **Validate project ID** exists and is accessible
- **Check project permissions** for task creation
- **Display project information** for confirmation
- **Scan existing tasks** using `mcp__vibe_kanban__list_tasks` to identify duplicates
- **Analyze task similarity** using configurable duplicate detection methods
- **Generate duplicate report** showing existing vs. template tasks
- **Provide import recommendations** based on duplicate analysis

### 3. Smart Task Creation Process with Duplicate Handling
- **Filter out duplicate tasks** based on selected duplicate detection method
- **Sort remaining tasks in reverse execution order** - last phases imported first for proper Kanban stacking
- **Add phase prefixes** to task titles (e.g., "01: S&P 500 Universe & Snapshot CSV")
- **Create new tasks only** using `mcp__vibe_kanban__create_task` in proper stacking order
- **Update existing tasks** if `--update-existing` is enabled with template content merge
- **Set task metadata** from template specifications with phase identification
- **Configure initial status** based on options with dependency awareness
- **Handle batch processing** to avoid overwhelming the API
- **Track creation/update progress** with status updates and duplicate notifications

### 4. Error Handling & Recovery
- **Validate input files** before processing
- **Handle API rate limits** with backoff strategy
- **Retry failed creations** with exponential backoff
- **Report creation status** for each task
- **Provide rollback guidance** if needed

### 5. Parallel Execution Analysis & Documentation
- **Analyze task dependencies** within each phase to identify parallel opportunities
- **Cross-phase dependency mapping** to determine which tasks can run simultaneously
- **Generate execution documentation** in `docs/execution/` with parallel workflow recommendations
- **Agent specialization analysis** to optimize parallel agent assignment
- **Performance optimization** through intelligent task batching and parallel execution

## Duplicate Detection & Prevention

### Duplicate Detection Methods

#### `title` - Fuzzy Title Matching (Default)
- **Logic**: Compares task titles using normalized string matching (case-insensitive, punctuation removed)
- **Match Criteria**: 85% similarity threshold using string distance algorithms
- **Example**: "01: S&P 500 Universe & Snapshot CSV" matches "S&P 500 Universe and Snapshot CSV"
- **Use Case**: General-purpose duplicate prevention with flexibility for minor title variations

#### `title-exact` - Exact Title Matching
- **Logic**: Requires exact title match after phase prefix normalization
- **Match Criteria**: Exact string equality (case-insensitive)
- **Example**: "01: FastAPI Scaffold + Health Endpoint" only matches "FastAPI Scaffold + Health Endpoint"
- **Use Case**: Strict duplicate prevention when title consistency is critical

#### `description` - Content-Based Matching
- **Logic**: Analyzes task descriptions and acceptance criteria for similarity
- **Match Criteria**: 70% content similarity using TF-IDF and cosine similarity
- **Example**: Tasks with similar acceptance criteria but different titles are detected as duplicates
- **Use Case**: Detecting functionally identical tasks with different naming

#### `smart` - Multi-Factor Intelligent Matching
- **Logic**: Combines title, description, and metadata analysis for comprehensive duplicate detection
- **Match Criteria**: Weighted scoring: title (40%), description (30%), agent_sequence (20%), cos (10%)
- **Example**: Detects tasks that are similar across multiple dimensions
- **Use Case**: Most comprehensive duplicate detection for complex projects

### Duplicate Handling Strategies

#### Skip Duplicates (Default Behavior)
```yaml
behavior: skip_duplicates
default: true
outcome:
  - "Existing tasks remain unchanged"
  - "Only new tasks are imported"
  - "Detailed skip report provided"
  - "No data loss or overwrites"
```

#### Force Import Override
```yaml
behavior: force_import
flag: --force-import
outcome:
  - "Creates duplicate tasks despite detection"
  - "Useful for testing or intentional duplicates"
  - "Warning displayed before proceeding"
  - "Original tasks remain unchanged"
```

#### Update Existing Tasks
```yaml
behavior: update_existing
flag: --update-existing
outcome:
  - "Merges template content with existing tasks"
  - "Updates descriptions, acceptance criteria, metadata"
  - "Preserves task status and creation dates"
  - "Creates backup of original task data"
```

### Duplicate Detection Workflow

#### Phase 1: Existing Task Analysis
1. **Fetch all existing tasks** from Kanban project using `mcp__vibe_kanban__list_tasks`
2. **Normalize task data** for comparison (remove phase prefixes, standardize formatting)
3. **Index tasks by detection method** (create searchable indexes for titles, descriptions, metadata)
4. **Prepare similarity matrices** for efficient matching

#### Phase 2: Template Task Comparison
1. **Parse template tasks** and normalize for comparison
2. **Apply selected detection method** to identify potential duplicates
3. **Calculate similarity scores** for each template vs. existing task pair
4. **Flag duplicates** based on threshold values

#### Phase 3: Decision Making
1. **Generate duplicate report** showing matches and similarity scores
2. **Apply handling strategy** (skip, force, update) based on flags
3. **Create action plan** with tasks to create, skip, or update
4. **Request user confirmation** for destructive operations

### Duplicate Detection Output

#### Duplicate Detection Report
```
╭─ Duplicate Detection Report ─────────────────────────────────╮
│ Project: Demo (bd722867-73b5-4f8d-b425-7551cb3d84c7)        │
│ Detection Method: smart                                       │
│ Templates Analyzed: 7 tasks                                  │
│ Existing Tasks: 10 tasks                                     │
├───────────────────────────────────────────────────────────────┤
│ DUPLICATES DETECTED:                                          │
│                                                               │
│ 🔄 Template: "01: FastAPI Scaffold + Health Endpoint"        │
│    Existing: "Task 1: FastAPI Scaffold + Health Endpoint"    │
│    Similarity: 95% (title: 100%, description: 90%)          │
│    Action: SKIP (use --force-import to override)             │
│                                                               │
│ 🔄 Template: "02: /api/top-stocks Endpoint + Models"         │
│    Existing: "Task 2: /api/top-stocks Endpoint + Models"     │
│    Similarity: 92% (title: 98%, description: 85%)           │
│    Action: SKIP (use --update-existing to merge)             │
│                                                               │
│ NEW TASKS TO CREATE:                                          │
│ ✅ "05: Observability Hooks (Basic Logging Metrics)"         │
│ ✅ "06: Frontend UI Components & Sparklines"                 │
│ ✅ "07: E2E Testing & Performance Validation"                │
├───────────────────────────────────────────────────────────────┤
│ Summary: 2 duplicates skipped, 3 new tasks to create         │
│ Continue with import? [Y/n]                                  │
╰───────────────────────────────────────────────────────────────╯
```

#### Update Existing Report
```
╭─ Task Update Report ─────────────────────────────────────────╮
│ Mode: Update Existing Tasks                                   │
│ Detection Method: title-exact                                 │
├───────────────────────────────────────────────────────────────┤
│ TASKS TO UPDATE:                                              │
│                                                               │
│ 📝 Task: "FastAPI Scaffold + Health Endpoint"                │
│    Changes:                                                   │
│    + Added: 3 new acceptance criteria from template          │
│    + Updated: Agent sequence with newer specifications       │
│    + Updated: Definition of done with Docker requirements    │
│    ~ Preserved: Current status (done), creation date         │
│                                                               │
│ 📝 Task: "/api/top-stocks Endpoint + Models"                 │
│    Changes:                                                   │
│    + Added: Performance requirements (≤5s cold, ≤2s warm)    │
│    + Updated: Error handling specifications                   │
│    ~ Preserved: Current status (todo), existing metadata     │
├───────────────────────────────────────────────────────────────┤
│ Summary: 2 tasks will be updated, no data loss               │
│ Backups will be created before updates                       │
│ Continue with updates? [Y/n]                                 │
╰───────────────────────────────────────────────────────────────╯
```

## Reverse Order Import Logic

### Why Reverse Order?
Kanban boards display tasks in creation order with newest tasks at the top. For proper execution flow, we need:
- **Foundation tasks** (01_foundation_data.md) to appear at the **top** of the board (executed first)
- **Final tasks** (06_documentation_polish.md) to appear at the **bottom** of the board (executed last)

### Import Sequence
```yaml
execution_order: [00, 01, 02, 03, 04, 05, 06, 99]  # Natural execution flow
import_order: [99, 06, 05, 04, 03, 02, 01, 00]     # Reverse for Kanban stacking
result_in_kanban: [00, 01, 02, 03, 04, 05, 06, 99] # Proper top-to-bottom flow
```

### Phase Identification System
- **Automatic Prefixing**: Tasks get phase numbers: "01: Foundation Task Name"
- **Dependency Tracking**: Phase-aware dependency validation
- **Agent Sequences**: Preserved with phase context for execution planning

## Task Template Format

### Expected YAML Structure
```yaml
# Task templates should follow this structure:
title: "Descriptive Task Title"
description: |
  Detailed description of what this task accomplishes
  and its business value
acceptance_criteria:
  - "Specific measurable outcome 1"
  - "Specific measurable outcome 2"
definition_of_done:
  - "Completion criteria 1"
  - "Completion criteria 2"
cos: Standard  # Standard|Expedite|FixedDate|Intangible
agent_sequence:
  - planner: {tooling: "Sequential MCP + tech-lead-orchestrator"}
  - backend: {agent: "python-backend-expert", cmd: "API implementation"}
  - reviewer: {agent: "code-reviewer", mode: "rigorous security-aware review"}
  - tester: {agent: "test-engineer", cmd: "integration tests"}
```

### Task Mapping to Kanban
| Template Field | Kanban Field | Processing |
|----------------|--------------|------------|
| `title` | Task title | Direct mapping |
| `description` | Task description | Combined with acceptance criteria |
| `acceptance_criteria` | Description appendix | Formatted as checklist |
| `definition_of_done` | Description appendix | Formatted as completion criteria |
| `cos` | Priority/Tags | Mapped to priority levels |
| `agent_sequence` | Task metadata | Stored as structured metadata |

## Command Workflow

### Phase 1: Preparation
1. **Validate input parameters** and required options
2. **Check template file existence** and readability
3. **Parse template structure** and validate format
4. **List available Kanban projects** for selection
5. **Confirm project ID** and permissions

### Phase 2: Template Processing
1. **Parse YAML frontmatter** from template files
2. **Extract individual task definitions** from markdown sections
3. **Process task descriptions** and acceptance criteria
4. **Map agent sequences** to task metadata
5. **Validate task completeness** and required fields

### Phase 3: Kanban Integration
1. **Create tasks in Kanban board** using MCP vibe-kanban
2. **Set initial task status** based on options
3. **Configure task metadata** from template
4. **Handle batch processing** with rate limiting
5. **Track creation progress** and report status

### Phase 4: Validation & Reporting
1. **Verify task creation** in Kanban board
2. **Report creation statistics** (success/failure counts)
3. **List created task IDs** for reference
4. **Provide next steps** for task execution
5. **Generate summary report** of import process

## MCP Integration Details

### Vibe Kanban MCP Tools Used
- **`list_projects`**: Get available projects for selection
- **`list_tasks`**: Fetch existing tasks for duplicate detection and analysis
- **`create_task`**: Create individual tasks in the board (new tasks only)
- **`update_task`**: Update existing tasks when --update-existing is enabled
- **`get_task`**: Verify task creation and fetch detailed task data for comparison
- **`delete_task`**: Remove duplicates if force-import creates unwanted duplicates

### Error Handling Patterns
```yaml
project_not_found:
  error: "Project ID not found"
  action: "List available projects and prompt for selection"
  
task_creation_failed:
  error: "Failed to create task"
  action: "Log error details and continue with next task"
  
rate_limit_exceeded:
  error: "API rate limit exceeded"
  action: "Implement exponential backoff and retry"
  
invalid_template:
  error: "Template format invalid"
  action: "Show validation errors and skip malformed tasks"

duplicate_detection_failed:
  error: "Unable to analyze existing tasks for duplicates"
  action: "Log warning and proceed with import (duplicates may be created)"
  
task_update_failed:
  error: "Failed to update existing task with template content"
  action: "Create new task instead and log update failure"
  
similarity_calculation_error:
  error: "Error calculating task similarity scores"
  action: "Fall back to simple title matching for duplicate detection"
```

## Output Format

### Dry Run Preview
```
╭─ Task Import Preview ─────────────────────────────────────╮
│ Project: My Project (abc123)                              │
│ Template: docs/tasks/01_foundation_data.md                │
│ Tasks to create: 7                                        │
├────────────────────────────────────────────────────────────┤
│ [1] Data Source Integration & API Adapters                │
│     Status: todo                                           │
│     Agent: python-backend-expert                          │
│                                                            │
│ [2] Core Business Logic Implementation                     │
│     Status: todo                                           │
│     Agent: python-backend-expert                          │
│                                                            │
│ ... (5 more tasks)                                        │
├────────────────────────────────────────────────────────────┤
│ Confirm import? [Y/n]                                     │
╰────────────────────────────────────────────────────────────╯
```

### Creation Progress
```
Creating tasks in project 'My Project'...

✅ Task 1/7: Data Source Integration & API Adapters (task_001)
✅ Task 2/7: Core Business Logic Implementation (task_002)
⚠️  Task 3/7: Data Validation - retrying...
✅ Task 3/7: Data Validation & Quality Assurance (task_003)
✅ Task 4/7: Caching Strategy & Implementation (task_004)
✅ Task 5/7: Data Models & Schema Creation (task_005)
✅ Task 6/7: Error Handling & Recovery (task_006)
✅ Task 7/7: Data Processing Pipeline Testing (task_007)

Summary: 7 tasks created successfully
Project URL: https://kanban.vibeboards.com/projects/abc123
```

### Error Report
```
Task Import Results:
✅ Successfully created: 6 tasks
❌ Failed to create: 1 task

Failed Tasks:
- "Performance Optimization Task" - Rate limit exceeded (will retry)

All tasks available at: https://kanban.vibeboards.com/projects/abc123
```

## Prerequisites

### Required Components
- **Vibe Kanban MCP server** configured and running
- **Valid project ID** in Vibe Kanban (get from web interface)
- **Task template files** in supported format
- **Network access** to Vibe Kanban API

### Project Setup
1. **Create Kanban project** at https://kanban.vibeboards.com
2. **Note the project ID** from the URL or settings
3. **Ensure MCP server** is configured in Claude Code
4. **Verify template files** follow the expected YAML structure

## Advanced Usage

### Custom Task Mapping
```
/create-kanban-tasks docs/tasks/custom_template.md --project-id abc123 --status inprogress
```
Creates tasks with custom initial status for immediate execution.

### Phase-by-Phase Import
```
# Import foundation phase
/create-kanban-tasks --phase 01 --project-id abc123

# Import backend phase (depends on foundation)
/create-kanban-tasks --phase 02 --project-id abc123

# Continue with remaining phases...
```

### Batch Processing for Large Projects
```
/create-kanban-tasks --all-phases --project-id abc123 --batch-size 3
```
Processes large task sets in smaller batches to avoid API limits.

## Integration with Other Commands

### Workflow Integration
```bash
# Generate task structure from PRD
/prd-to-tasks requirements.md --type web-app

# Import generated tasks to Kanban
/create-kanban-tasks --all-phases --project-id abc123

# Execute tasks using multi-agent orchestration
/task execute --project-id abc123 --agent-mode auto
```

### Task Execution Commands
After importing tasks to Kanban, use these patterns:
- `/task execute task_001` - Execute specific task
- `/task status --project-id abc123` - Check all task statuses  
- `/task update task_001 --status inprogress` - Update task status
- `/task complete task_001` - Mark task as completed

## Troubleshooting

### Common Issues

**Project ID Not Found**
```
Error: Project 'invalid-id' not found
Solution: Use /list-kanban-projects to see available projects
```

**Template File Not Found**
```
Error: Template file 'docs/tasks/missing.md' not found
Solution: Check file path or use --all-phases to import all available templates
```

**Task Creation Failed**
```
Error: Failed to create task 'Task Name'
Solution: Check task template format and required fields
```

**MCP Server Not Available**
```
Error: vibe-kanban MCP server not responding
Solution: Verify MCP server configuration and network connectivity
```

**Duplicate Detection Issues**
```
Error: Tasks not detected as duplicates when they should be
Solution: 
- Try different --duplicate-check methods (smart, description, title-exact)
- Use --dry-run to test detection before import
- Check for minor title/description differences that affect matching
```

**False Positive Duplicates**
```
Error: Tasks incorrectly flagged as duplicates
Solution:
- Use stricter detection method (title-exact instead of title)
- Use --force-import to override duplicate detection
- Review similarity thresholds and adjust detection method
```

**Update Existing Tasks Failed**
```
Error: Unable to update existing tasks with template content
Solution:
- Verify project permissions allow task modification
- Check existing task format compatibility
- Use --force-import to create new tasks instead
```

### Debug Mode
```
# Enable verbose logging for troubleshooting
/create-kanban-tasks docs/tasks/01_foundation_data.md --project-id abc123 --debug
```

## Best Practices

### Template Organization
- **Use consistent YAML structure** across all template files
- **Include clear acceptance criteria** for each task
- **Define complete agent sequences** for execution
- **Set appropriate classes of service** (Standard, Expedite, etc.)

### Import Strategy
- **Start with single phases** to validate format
- **Use dry-run** to preview before importing
- **Import dependencies first** (foundation before backend)
- **Monitor task creation** progress and handle errors

### Duplicate Prevention Strategy
- **Always use --skip-duplicates** for production imports to prevent accidental duplicates
- **Test detection methods** with --dry-run to find optimal duplicate matching
- **Use smart detection** for comprehensive duplicate prevention across projects
- **Create backups** before using --update-existing to modify existing tasks
- **Force import sparingly** and only when intentional duplicates are needed

### Kanban Board Management
- **Create dedicated projects** for different development efforts
- **Use consistent naming** for easy identification
- **Set appropriate WIP limits** based on team capacity
- **Configure board columns** to match development workflow

## Parallel Execution Analysis

### Automatic Parallel Detection
The command analyzes task structures to identify parallel execution opportunities:

#### Within-Phase Parallelism
```yaml
01_foundation_data.md:
  parallel_opportunities:
    - "Task 1: S&P 500 Universe" + "Task 3: Sharpe Engine" (no dependencies)
    - "Task 2: yfinance Adapter" (depends on Task 1, can run parallel with Task 3)
  
02_backend_api.md:
  parallel_opportunities:
    - "Task 2: /api/top-stocks" + "Task 3: /api/price-series" (independent endpoints)
    - "Task 4: Input Validation" + "Task 5: Observability" (can run parallel after endpoints)

03_frontend_ui.md:
  parallel_opportunities:
    - "Task 2: Top-5 Table" + "Task 3: Sparkline Component" (independent UI components)
    - "Task 4: RF Input" (depends on table, can run with sparklines)
```

#### Cross-Phase Parallelism
```yaml
overlapping_phases:
  backend_frontend_overlap:
    - "02: Task 1 FastAPI Scaffold" allows "03: Task 1 UI Scaffold" to start
    - Backend endpoint development can run parallel with UI component development
  
  testing_development_overlap:
    - "04: Testing tasks" can start once endpoints are available
    - Unit test development can run parallel with integration work

documentation_continuous:
  - Documentation tasks can run throughout development phases
  - README and API docs can be incrementally updated
```

### Generated Execution Documentation
When `--parallel-analysis` is enabled, creates `docs/execution/parallel_workflow.md` with:

#### Execution Phases
```markdown
# Parallel Execution Plan

## Phase 1: Foundation Setup (Days 1-3)
**Parallel Track A**: S&P 500 Universe + Sharpe Engine (2 agents)
**Parallel Track B**: yfinance Adapter (1 agent, after Track A Task 1)
**Dependencies**: None
**Agents**: 2-3 backend developers, 1 data specialist

## Phase 2: API Development (Days 4-6) 
**Parallel Track A**: FastAPI Scaffold + Health endpoint (1 agent)
**Parallel Track B**: Core endpoints development (2 agents after Track A)
**Parallel Track C**: UI Scaffold can start (1 frontend agent)
**Dependencies**: Foundation data layer complete
**Agents**: 2-3 backend developers, 1 frontend developer

## Phase 3: Frontend + Backend Parallel (Days 5-8)
**Parallel Track A**: Frontend table + sparklines (2 agents)
**Parallel Track B**: Backend validation + observability (2 agents) 
**Parallel Track C**: Testing can begin (1 QA agent)
**Dependencies**: API endpoints functional
**Agents**: 2 frontend developers, 2 backend developers, 1 QA engineer

## Phase 4: Integration + Polish (Days 7-10)
**Parallel Track A**: E2E testing + performance (2 agents)
**Parallel Track B**: Accessibility + documentation (2 agents)
**Parallel Track C**: Infrastructure + deployment (1 agent)
**Dependencies**: Core functionality complete
**Agents**: 2 QA engineers, 1 accessibility specialist, 1 DevOps engineer
```

#### Agent Specialization Recommendations
```yaml
optimal_agent_assignment:
  foundation_phase:
    - python-backend-expert: yfinance adapter, Sharpe utilities
    - data-scientist: S&P 500 universe, data validation
    - backend-developer: service layer integration
  
  api_phase:
    - python-backend-expert: FastAPI endpoints, Pydantic models
    - api-architect: endpoint design, validation patterns
    - backend-developer: middleware, error handling
  
  frontend_phase:
    - tailwind-frontend-expert: UI components, responsive design
    - frontend-developer: JavaScript modules, API integration
    - accessibility-specialist: WCAG compliance, screen reader testing
  
  testing_phase:
    - test-engineer: unit tests, integration tests
    - performance-optimizer: load testing, optimization
    - qa-specialist: manual testing, edge cases
```

This command provides a bridge between Claude Code's task generation capabilities and Vibe Kanban's project management features, enabling seamless transition from planning to execution with intelligent parallel workflow optimization.
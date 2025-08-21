# /create-kanban-tasks - Import Task Templates to Vibe Kanban

Import structured task templates into Vibe Kanban boards for execution and progress tracking.

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

## What This Command Does

### 1. Template File Analysis
- **Parse YAML frontmatter** from task template files
- **Extract task definitions** with titles, descriptions, and acceptance criteria
- **Identify task relationships** and dependencies
- **Map agent sequences** to task metadata
- **Validate task structure** for Kanban compatibility

### 2. Project Validation
- **List available projects** using `mcp__vibe_kanban__list_projects`
- **Validate project ID** exists and is accessible
- **Check project permissions** for task creation
- **Display project information** for confirmation

### 3. Task Creation Process
- **Create tasks** using `mcp__vibe_kanban__create_task`
- **Set task metadata** from template specifications
- **Configure initial status** based on options
- **Handle batch processing** to avoid overwhelming the API
- **Track creation progress** with status updates

### 4. Error Handling & Recovery
- **Validate input files** before processing
- **Handle API rate limits** with backoff strategy
- **Retry failed creations** with exponential backoff
- **Report creation status** for each task
- **Provide rollback guidance** if needed

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
- **`create_task`**: Create individual tasks in the board
- **`get_task`**: Verify task creation (validation)
- **`list_tasks`**: Check existing tasks (duplicate prevention)

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

### Kanban Board Management
- **Create dedicated projects** for different development efforts
- **Use consistent naming** for easy identification
- **Set appropriate WIP limits** based on team capacity
- **Configure board columns** to match development workflow

This command provides a bridge between Claude Code's task generation capabilities and Vibe Kanban's project management features, enabling seamless transition from planning to execution.
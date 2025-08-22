# /remove-kanban-task - Remove Tasks from Vibe Kanban

Remove specific tasks from Vibe Kanban boards with safety controls and bulk operations. Supports filtering by status, selective removal, and recovery options for safe task management.

## Command Usage

```
/remove-kanban-task [task-filter] [options]
```

## Arguments

| Argument | Description | Default | Examples |
|----------|-------------|---------|-----------|
| `task-filter` | Task selection criteria | Required | `--task-id abc123`, `--status todo`, `--phase 01` |

## Options

| Flag | Description | Default | Values |
|------|-------------|---------|---------|
| `--project-id` | Vibe Kanban project ID | Auto-detect or prompt | Project UUID from Kanban board |
| `--task-id` | Specific task ID to remove | None | Single task ID or comma-separated list |
| `--status` | Remove tasks by status | None | `todo`, `inprogress`, `inreview`, `done`, `cancelled` |
| `--phase` | Remove tasks by phase prefix | None | `01`, `02`, `03`, etc. |
| `--title-contains` | Remove tasks with title containing text | None | Keywords or phrases to match |
| `--dry-run` | Preview without removing | `true` | `true`, `false` - Shows what would be removed |
| `--confirm` | Skip confirmation prompts | `false` | `true`, `false` - Use with caution |
| `--backup-first` | Create backup before removal | `true` | `true`, `false` - Export tasks before deletion |
| `--filter-mode` | How to combine multiple filters | `and` | `and`, `or` - Logical combination of filters |

## Examples

### Remove Specific Task
```
/remove-kanban-task --task-id abc123 --project-id proj456
```
Remove a single task by its ID with confirmation prompt.

### Remove Tasks by Status (Safe Default)
```
/remove-kanban-task --status todo --project-id proj456 --dry-run
```
Preview removal of all tasks in 'todo' status without actually deleting them.

### Remove Completed Tasks
```
/remove-kanban-task --status done --project-id proj456 --backup-first
```
Remove all completed tasks after creating a backup export.

### Remove Tasks by Phase
```
/remove-kanban-task --phase 01 --project-id proj456
```
Remove all tasks with "01:" prefix (foundation phase tasks).

### Bulk Remove with Confirmation
```
/remove-kanban-task --status cancelled --status done --filter-mode or --project-id proj456 --confirm
```
Remove all tasks that are either cancelled or done without individual confirmations.

### Remove by Title Content
```
/remove-kanban-task --title-contains "test" --project-id proj456 --dry-run
```
Preview removal of all tasks with "test" in their title.

### Complex Filter Combination
```
/remove-kanban-task --phase 03 --status todo --title-contains "UI" --filter-mode and --project-id proj456
```
Remove tasks that are in phase 03, have todo status, AND contain "UI" in title.

## What This Command Does

### 1. Task Discovery & Filtering
- **List all tasks** in the specified project using `mcp__vibe_kanban__list_tasks`
- **Apply filters** based on provided criteria (status, phase, title, ID)
- **Validate task existence** and accessibility before attempting removal
- **Display filtered results** with task details for user review
- **Handle filter combinations** using AND/OR logic as specified

### 2. Safety & Validation Checks
- **Dry-run by default** to prevent accidental deletions
- **Backup creation** before bulk removals (optional but recommended)
- **Confirmation prompts** for each removal unless explicitly skipped
- **Dependency checking** to identify tasks that depend on removal candidates
- **Status validation** to prevent removal of critical in-progress work

### 3. Task Removal Process
- **Individual removal** using `mcp__vibe_kanban__delete_task` for each matched task
- **Batch processing** with progress tracking for bulk operations
- **Error handling** with continue-on-error for partial failures
- **Removal verification** to confirm successful deletion
- **Result summary** with success/failure counts and details

### 4. Recovery & Rollback Options
- **Pre-removal backup** export to JSON format for recovery
- **Removal history** logging for audit trails
- **Recovery instructions** provided after removal completion
- **Failed removal tracking** for retry operations
- **Undo guidance** using backup files and manual recreation

## Task Selection & Filtering

### Filter Types

#### By Task ID
```yaml
single_task:
  command: "--task-id abc123"
  matches: "Exactly one task with specified ID"
  safety: "High - explicit selection"

multiple_tasks:
  command: "--task-id abc123,def456,ghi789"
  matches: "Multiple specific tasks by ID list"
  safety: "High - explicit selection"
```

#### By Status
```yaml
status_filters:
  todo: "Tasks ready for work (safest to remove)"
  inprogress: "Tasks currently being worked on (requires confirmation)"
  inreview: "Tasks under review (moderate safety)"
  done: "Completed tasks (safe to remove)"
  cancelled: "Cancelled tasks (safe to remove)"
```

#### By Phase Prefix
```yaml
phase_filters:
  foundation: "--phase 01  # Remove all foundation tasks"
  backend: "--phase 02     # Remove all backend API tasks"
  frontend: "--phase 03    # Remove all frontend UI tasks"
  testing: "--phase 04     # Remove all testing tasks"
  deploy: "--phase 05      # Remove all deployment tasks"
  docs: "--phase 06        # Remove all documentation tasks"
```

#### By Title Content
```yaml
title_filters:
  keywords: "--title-contains 'API'     # Tasks with API in title"
  test_tasks: "--title-contains 'test'  # All testing-related tasks"
  deprecated: "--title-contains 'old'   # Legacy or outdated tasks"
```

### Filter Combination Logic

#### AND Logic (Default)
```yaml
and_example:
  command: "--phase 01 --status todo --filter-mode and"
  matches: "Tasks that are phase 01 AND status todo"
  use_case: "Precise targeting of specific task subset"
```

#### OR Logic
```yaml
or_example:
  command: "--status done --status cancelled --filter-mode or"
  matches: "Tasks that are done OR cancelled"
  use_case: "Cleanup of completed/abandoned work"
```

## Safety Features & Workflows

### Default Safety Measures
```yaml
safety_defaults:
  dry_run: true          # Always preview first
  confirmation: true     # Prompt before each removal
  backup: true          # Create export before bulk operations
  dependency_check: true # Warn about dependent tasks
```

### Confirmation Workflows

#### Single Task Removal
```
┌─ Task Removal Confirmation ─────────────────────────────┐
│ Task: "01: S&P 500 Universe & Snapshot CSV"             │
│ ID: abc123                                               │
│ Status: todo                                             │
│ Phase: 01 (Foundation Data)                             │
│                                                          │
│ ⚠️  This action cannot be undone!                       │
│                                                          │
│ Remove this task? [y/N]                                 │
└──────────────────────────────────────────────────────────┘
```

#### Bulk Removal Confirmation
```
┌─ Bulk Removal Confirmation ──────────────────────────────┐
│ Filter: --status todo --phase 01                         │
│ Matched Tasks: 3                                         │
│                                                           │
│ Tasks to be removed:                                      │
│ • [abc123] 01: S&P 500 Universe & Snapshot CSV          │
│ • [def456] 01: yfinance Adapter + Retries + Caching     │
│ • [ghi789] 01: Sharpe Engine Utilities                  │
│                                                           │
│ ⚠️  Backup will be created before removal                │
│                                                           │
│ Continue with bulk removal? [y/N]                        │
└───────────────────────────────────────────────────────────┘
```

### Dependency Impact Analysis
```yaml
dependency_check:
  before_removal:
    - "Scan all remaining tasks for dependencies on removal candidates"
    - "Identify tasks that may be blocked by removal"
    - "Display warning with affected task list"
    - "Require explicit confirmation for removal with dependencies"
  
  impact_display:
    warning: "⚠️ 2 tasks depend on this task and may be blocked"
    affected_tasks:
      - "[xyz123] 02: FastAPI Scaffold + Health Endpoint"
      - "[uvw456] 02: /api/top-stocks Endpoint + Models"
    recommendation: "Consider updating dependent tasks before removal"
```

## Backup & Recovery

### Automatic Backup Creation
```yaml
backup_process:
  trigger: "Bulk operations (>1 task) or --backup-first flag"
  format: "JSON export with full task metadata"
  location: "docs/backups/kanban_backup_TIMESTAMP.json"
  content:
    - "Complete task data with all fields"
    - "Project metadata and configuration"
    - "Removal operation details and timestamp"
    - "Recovery instructions and task recreation commands"
```

### Backup File Format
```json
{
  "backup_metadata": {
    "created_at": "2024-01-15T10:30:00Z",
    "project_id": "proj456",
    "operation": "bulk_remove",
    "filter_criteria": {
      "status": "todo",
      "phase": "01"
    },
    "total_tasks": 3
  },
  "tasks": [
    {
      "task_id": "abc123",
      "title": "01: S&P 500 Universe & Snapshot CSV",
      "description": "Create a deterministic S&P 500 stock universe...",
      "status": "todo",
      "created_at": "2024-01-10T08:00:00Z",
      "metadata": {
        "phase": "01",
        "agent_sequence": ["planner", "data", "reviewer", "tester"]
      }
    }
  ],
  "recovery_instructions": {
    "manual_recreation": "Use /create-kanban-tasks to recreate from templates",
    "api_commands": [
      "mcp__vibe_kanban__create_task with original data"
    ]
  }
}
```

### Recovery Procedures
```yaml
recovery_options:
  from_backup:
    command: "/restore-kanban-tasks --backup-file docs/backups/kanban_backup_*.json"
    description: "Recreate tasks from backup file"
    limitations: "Task IDs will be different, dependencies may need updating"
  
  from_templates:
    command: "/create-kanban-tasks --phase 01 --project-id proj456"
    description: "Recreate from original task templates"
    benefits: "Ensures latest task definitions, maintains consistency"
  
  manual_recreation:
    process: "Use backup file data to manually recreate tasks via UI"
    use_case: "When automated recovery fails or partial restoration needed"
```

## Command Workflow

### Phase 1: Discovery & Validation
1. **Connect to project** using provided project ID
2. **List all tasks** in the project for filtering
3. **Apply filter criteria** to identify removal candidates
4. **Validate task access** and removal permissions
5. **Check dependencies** for impact analysis

### Phase 2: Safety & Confirmation
1. **Display matched tasks** with full details for review
2. **Show dependency warnings** if applicable
3. **Create backup** for bulk operations (if enabled)
4. **Request confirmation** for removal operation
5. **Final safety check** before proceeding

### Phase 3: Removal Execution
1. **Remove tasks individually** using vibe-kanban MCP
2. **Track progress** for bulk operations with status updates
3. **Handle errors** gracefully with continue-on-error behavior
4. **Verify removal** by checking task no longer exists
5. **Log operation** for audit trail and recovery reference

### Phase 4: Completion & Recovery Info
1. **Generate removal summary** with success/failure counts
2. **Provide backup location** and recovery instructions
3. **Display any warnings** or post-removal recommendations
4. **Update documentation** if tasks were template-based
5. **Clean up temporary files** and close connections

## Error Handling & Recovery

### Common Error Scenarios

#### Task Not Found
```yaml
error: "Task ID 'abc123' not found in project"
action: "Skip task and continue with remaining removals"
logging: "Record missing task ID for investigation"
user_feedback: "Display warning with suggestion to refresh task list"
```

#### Permission Denied
```yaml
error: "Insufficient permissions to delete task 'abc123'"
action: "Skip task and continue with remaining removals"
logging: "Record permission failure for admin review"
user_feedback: "Suggest checking project access permissions"
```

#### Network/API Failures
```yaml
error: "Failed to connect to Vibe Kanban API"
action: "Retry with exponential backoff (3 attempts)"
logging: "Record connectivity issues and retry attempts"
user_feedback: "Suggest checking network connection and API status"
```

#### Dependency Conflicts
```yaml
error: "Task has dependent tasks that would be orphaned"
action: "Require explicit confirmation or abort removal"
logging: "Record dependency conflict details"
user_feedback: "Display affected tasks and provide resolution options"
```

### Recovery Strategies
```yaml
partial_failure_recovery:
  scenario: "Some tasks removed successfully, others failed"
  action: "Provide detailed report with successful/failed task lists"
  recommendation: "Retry failed removals individually or use backup for restoration"

complete_failure_recovery:
  scenario: "All removal operations failed"
  action: "Preserve original state, no changes made"
  recommendation: "Check permissions, connectivity, and task existence"

accidental_removal_recovery:
  scenario: "Tasks removed by mistake"
  action: "Use backup file for task recreation"
  recommendation: "Restore from backup or recreate from templates immediately"
```

## Integration with Other Commands

### Workflow Integration
```bash
# Clean up completed work before new phase
/remove-kanban-task --status done --project-id proj456 --backup-first

# Remove cancelled/obsolete tasks  
/remove-kanban-task --status cancelled --project-id proj456

# Clear specific phase for reimport
/remove-kanban-task --phase 01 --project-id proj456
/create-kanban-tasks --phase 01 --project-id proj456

# Cleanup test tasks
/remove-kanban-task --title-contains "test" --dry-run --project-id proj456
```

### Best Practices

#### Before Major Operations
1. **Always dry-run first** to preview removal scope
2. **Create backups** before bulk operations
3. **Check dependencies** that might be affected
4. **Coordinate with team** for shared project changes

#### Safe Removal Patterns
```yaml
safest_removals:
  - "Tasks with status 'done' or 'cancelled'"
  - "Test tasks that are no longer needed"
  - "Duplicate tasks created by error"
  - "Tasks explicitly marked for removal"

risky_removals:
  - "Tasks with status 'inprogress'"
  - "Tasks with many dependencies"
  - "Foundation tasks that other phases depend on"
  - "Tasks without proper backup"
```

#### Recovery Preparedness
1. **Maintain template sources** for easy recreation
2. **Document removal rationale** for future reference
3. **Keep backup files** until project completion
4. **Test recovery procedures** before major cleanups

## Troubleshooting

### Common Issues

#### "No tasks match filter criteria"
```
Error: No tasks found matching the specified filters
Solution: 
- Use --dry-run to test filters before removal
- Check task list with /list-kanban-tasks
- Verify project ID and filter syntax
```

#### "Cannot remove in-progress tasks"
```
Error: Safety check prevents removal of active tasks
Solution:
- Update task status to 'cancelled' or 'done' first
- Use --confirm flag to override safety check
- Review why in-progress tasks need removal
```

#### "Backup creation failed"
```
Error: Unable to create backup file
Solution:
- Check write permissions for docs/backups/ directory
- Ensure sufficient disk space
- Manually export tasks via UI before removal
```

#### "Some tasks could not be removed"
```
Error: Partial failure in bulk removal operation
Solution:
- Review error details for each failed task
- Retry failed removals individually
- Check for dependency conflicts or permission issues
```

This command provides safe, controlled task removal from Vibe Kanban boards with comprehensive backup and recovery options, ensuring team productivity and data safety.
# /prd-to-tasks - Generate Task Structure from PRD

Generate Kanban task structure documents from Product Requirements Documents using strategic project templates.

## Command Usage

```
/prd-to-tasks [prd-file] [options]
```

## Arguments

| Argument | Description | Default | Examples |
|----------|-------------|---------|-----------|
| `prd-file` | Path to PRD file | `prd.md`, `prd.txt`, `docs/prd.md` | `requirements.md`, `specs/prd.txt` |

## Options

| Flag | Description | Default | Values |
|------|-------------|---------|---------|
| `--type` | Project domain type | `web-app` | `web-app`, `mobile-app`, `api-service`, `data-platform`, `ml-system` |
| `--timeline` | Development approach | `standard` | `fast-mvp`, `standard`, `comprehensive` |
| `--output` | Output directory | `docs/tasks` | Any valid directory path |
| `--github-owner` | GitHub owner | Auto-detect from git | GitHub username or org |
| `--project-name` | Project name | Current directory name | Custom project name |

## Examples

### Basic Usage
```
/prd-to-tasks prd.md
```
Generates standard web-app task structure from `prd.md` in `docs/tasks/`

### Web Application with Custom Settings
```
/prd-to-tasks requirements.md --type web-app --timeline standard --github-owner mycompany
```

### Fast MVP for API Service
```
/prd-to-tasks api-spec.txt --type api-service --timeline fast-mvp
```

### Comprehensive Data Platform
```
/prd-to-tasks data-requirements.md --type data-platform --timeline comprehensive --output planning/
```

## What This Command Does

### 1. PRD Analysis
- **Read and parse** the specified PRD file
- **Extract key requirements** and features
- **Detect technology stack** from mentions
- **Assess complexity** based on feature count
- **Classify domain** based on feature types

### 2. Template Processing
- **Load strategic project template** from `docs/plan/strategic_project_template.md`
- **Apply domain-specific adaptations** based on project type
- **Customize phases and agents** for the technology stack
- **Scale task complexity** based on timeline selection

### 3. Task Generation
Creates structured task files using `docs/plan/task_template.md`:

```
docs/tasks/
├── init_project_setup.md          # Phase -1: Bootstrap
├── 000_project_ideation.md         # Phase 0: Requirements
├── 00_project_planning.md          # Phase 1: Planning
├── 01_foundation_data.md           # Phase 2: Data Layer
├── 02_backend_api.md               # Phase 3: Backend API
├── 03_frontend_ui.md               # Phase 4: Frontend UI
├── 04_testing_validation.md        # Phase 5: Testing
├── 05_infrastructure_deploy.md     # Phase 6: Infrastructure
├── 06_documentation_polish.md      # Phase 7: Documentation
└── 99_release_management.md        # Phase 8: Release
```

### 4. Content Customization
Each generated file includes:
- **Project-specific metadata** (name, GitHub owner, tech stack)
- **Kanban-compatible task structure** with YAML frontmatter
- **Agent sequences** optimized for the detected technology stack
- **Performance targets** appropriate for the domain type
- **Quality gates** aligned with project complexity
- **Dependencies** mapped between phases

## Project Type Adaptations

### Web Application (`--type web-app`)
- **Additional Phases**: SEO optimization, analytics, content management
- **Specialized Agents**: `frontend-developer`, `accessibility-specialist`, `performance-optimizer`
- **Performance Targets**: <3s load time, WCAG AA compliance, Core Web Vitals
- **Quality Gates**: Lighthouse scores ≥90, accessibility testing, performance budgets

### Mobile Application (`--type mobile-app`)
- **Additional Phases**: Mobile UI/UX, device integration, app store optimization
- **Specialized Agents**: `mobile-developer`, `ux-designer`
- **Performance Targets**: <2s app launch, 60fps animations, battery efficiency
- **Quality Gates**: Platform-specific testing, performance profiling

### API Service (`--type api-service`)
- **Additional Phases**: API versioning, rate limiting, service mesh integration
- **Specialized Agents**: `api-architect`, `backend-developer`, `security-specialist`
- **Performance Targets**: <200ms response time, 99.9% uptime, auto-scaling
- **Quality Gates**: API contract testing, security scanning, load testing

### Data Platform (`--type data-platform`)
- **Additional Phases**: ETL pipelines, data warehouse design, stream processing
- **Specialized Agents**: `data-scientist`, `database-architect`, `mlops-engineer`
- **Performance Targets**: <5min batch processing, real-time streaming, data accuracy
- **Quality Gates**: Data quality validation, pipeline monitoring, compliance checks

### ML System (`--type ml-system`)
- **Additional Phases**: Model training, evaluation, deployment, monitoring
- **Specialized Agents**: `python-ml-specialist`, `mlops-engineer`, `data-scientist`
- **Performance Targets**: Model accuracy metrics, inference latency, training time
- **Quality Gates**: Model validation, A/B testing, performance monitoring

## Timeline Options

### Fast MVP (`--timeline fast-mvp`)
- **Duration**: 2-4 hours implementation
- **Task Count**: 8-12 essential tasks
- **Focus**: Core features only, minimal viable product
- **Agent Sequences**: Simplified, single specialist per task
- **Quality Gates**: Essential validation only
- **Use Case**: Rapid prototyping, proof of concept, learning experiments

### Standard (`--timeline standard`)
- **Duration**: 1-2 weeks implementation
- **Task Count**: 15-25 comprehensive tasks
- **Focus**: Production-ready features with full quality
- **Agent Sequences**: Complete multi-agent coordination
- **Quality Gates**: Full 8-step validation cycle
- **Use Case**: Standard product development, business applications

### Comprehensive (`--timeline comprehensive`)
- **Duration**: 2-4 weeks implementation
- **Task Count**: 25-40 tasks with specialized phases
- **Focus**: Enterprise-grade with full compliance
- **Agent Sequences**: Extended with security and performance specialists
- **Quality Gates**: Enhanced validation with compliance requirements
- **Use Case**: Enterprise products, regulated industries, critical systems

## Generated Task Structure

### YAML Frontmatter Format
```yaml
title: "Descriptive Task Title"
repo: "github.com/{GITHUB_OWNER}/{PROJECT_NAME}"
branch: "feat/task-branch-name"
description: |
  Detailed description of what this task accomplishes
  and its business value
acceptance_criteria:
  - "Specific measurable outcome 1"
  - "Specific measurable outcome 2"
cos: Standard  # Standard|Expedite|FixedDate|Intangible
definition_of_done:
  - "Completion criteria 1"
  - "Completion criteria 2"
agent_sequence:
  - planner: {tooling: "Sequential MCP + tech-lead-orchestrator"}
  - {domain_agent}: {agent: "specialist-agent", cmd: "specific command"}
  - reviewer: {agent: "code-reviewer", mode: "rigorous security-aware review"}
  - tester: {agent: "test-engineer", cmd: "test type and scope"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

### Task Content Sections
- **Task Group Priority**: Phase classification and dependencies
- **Individual Tasks**: Numbered tasks with full specifications
- **Quality Gates**: Validation requirements and success criteria
- **Performance Targets**: Domain-specific performance requirements

## Integration Features

### Task-Master-AI Compatibility
The generated task structure is fully compatible with Task-Master-AI:
```bash
# After generating tasks, initialize Task-Master-AI
taskmaster initialize-project --project-root .
taskmaster parse-prd --input docs/prd.txt --output docs/tasks/tasks.json
```

### Vibe Kanban Integration
Tasks can be imported directly to Kanban boards:
```bash
# Import generated tasks to Kanban board
vibe-kanban import-tasks --project-id <project-id> --source docs/tasks/
```

### Multi-Agent Orchestration
Each task includes optimized agent sequences:
- **Planner**: Sequential MCP + tech-lead-orchestrator
- **Domain Specialist**: Based on task type (frontend, backend, data, etc.)
- **Reviewer**: Code-reviewer with security focus
- **Tester**: Test-engineer with appropriate test strategy

## Prerequisites

This command requires the following files in your repository:

### Required Template Files
- `docs/plan/strategic_project_template.md` - Master project template
- `docs/plan/task_template.md` - Individual task template

### Optional Integration Files
- `prd.md` or `prd.txt` - Product Requirements Document
- `.git/config` - For GitHub owner detection
- `package.json` or similar - For technology stack detection

## Error Handling

### Common Error Cases
- **PRD file not found**: Command will prompt for correct file path
- **Template files missing**: Command will suggest copying from demo repository
- **Invalid project type**: Command will list valid options
- **Output directory permission**: Command will suggest alternative paths
- **Git repository not found**: GitHub owner will default to placeholder

### Validation Checks
- **Template placeholder replacement**: Ensures all `{PLACEHOLDER}` values are replaced
- **Task numbering consistency**: Validates sequential task numbering
- **Dependency validation**: Checks logical dependency relationships
- **Agent compatibility**: Verifies agent and tool combinations are valid
- **Performance target realism**: Ensures targets are achievable for domain

## Implementation Notes

This command is designed to work in any repository by:
1. **Reading template files** from the current or specified template directory
2. **Auto-detecting project context** from git configuration and file structure
3. **Generating portable task files** that work with various project management tools
4. **Following Kanban principles** with proper WIP limits and pull policies
5. **Supporting multi-agent orchestration** patterns for AI-driven development

The generated task structure provides a complete foundation for systematic project development using Claude Code's multi-agent capabilities.
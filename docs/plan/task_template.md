# Kanban Task Template

This template provides a standardized structure for creating Kanban-compatible tasks based on the project's multi-agent development patterns.

## Task Group Template

```yaml
# {NUMBER} {GROUP_NAME} Tasks

{DESCRIPTION_OF_TASK_GROUP}

## Task Group Priority
**Phase**: {Foundation|Development|Testing|Deployment|Polish}
**Dependencies**: {LIST_OF_DEPENDENCIES}
**Blocks**: {WHAT_THIS_BLOCKS}
**Estimated Duration**: {TIME_ESTIMATE}

---

## Task {N}: {TASK_TITLE}

```yaml
title: "{DESCRIPTIVE_TASK_TITLE}"
repo: "github.com/{OWNER}/{PROJECT_NAME}"
branch: "{BRANCH_NAME}"
description: |
  {DETAILED_DESCRIPTION_OF_WHAT_THIS_TASK_ACCOMPLISHES}
  {WHY_THIS_TASK_IS_IMPORTANT_AND_ITS_BUSINESS_VALUE}
acceptance_criteria:
  - "{SPECIFIC_MEASURABLE_OUTCOME_1}"
  - "{SPECIFIC_MEASURABLE_OUTCOME_2}"
cos: {Standard|Expedite|FixedDate|Intangible}
definition_of_done:
  - "{COMPLETION_CRITERIA_1}"
  - "{COMPLETION_CRITERIA_2}"
todo_list:
  planner:
    - "{PLANNING_TASK_1}"
    - "{PLANNING_TASK_2}"
  {AGENT_ROLE}:
    - "{IMPLEMENTATION_TASK_1}"
    - "{IMPLEMENTATION_TASK_2}"
  reviewer:
    - "{REVIEW_TASK_1}"
    - "{REVIEW_TASK_2}"
  tester:
    - "{TESTING_TASK_1}"
    - "{TESTING_TASK_2}"
agent_sequence:
  - planner: {tooling: "Sequential MCP + tech-lead-orchestrator"}
  - {AGENT_ROLE}: {agent: "{SPECIFIC_AGENT}", cmd: "{AGENT_COMMAND}"}
  - reviewer: {agent: "code-reviewer", mode: "rigorous security-aware review"}
  - tester: {agent: "test-engineer", cmd: "{TEST_COMMAND}"}
pull_policy: "Move right only if WIP < limit and AC clarified"
blockers: []
```

---

## Task Group Dependencies

**Provides Foundation For:**
- {WHAT_THIS_ENABLES}

**Quality Gates:**
- {QUALITY_REQUIREMENT_1}
- {QUALITY_REQUIREMENT_2}

**Performance Targets:**
- {PERFORMANCE_METRIC_1}
- {PERFORMANCE_METRIC_2}
```

## Field Guide

### Title & Identification
- **title**: Short, action-oriented description (e.g., "Implement FastAPI scaffold + /health")
- **repo**: Use format "github.com/{OWNER}/{PROJECT_NAME}" for your project
- **branch**: Use pattern `feat/`, `fix/`, `design/`, `ops/` prefix

### Description & Requirements
- **description**: 2-3 sentences explaining what and why
- **acceptance_criteria**: Specific, measurable outcomes with technical details
- **definition_of_done**: Completion criteria including tests, documentation, deployment

### Classes of Service (cos)
- **Standard**: Normal feature development (most tasks)
- **Expedite**: Production hotfixes (emergency only)
- **FixedDate**: Demo day releases with deadlines
- **Intangible**: Documentation, policies, governance

### Todo List Structure
- **planner**: Analysis, design, planning tasks using Sequential MCP
- **{role}**: Implementation tasks for specific domain (data, backend, frontend, devops)
- **reviewer**: Code review and security analysis
- **tester**: Test creation and validation

### Agent Sequence Patterns
Common agent configurations:
- **planner**: `{tooling: "Sequential MCP + tech-lead-orchestrator"}`
- **data**: `{agent: "python-backend-expert", cmd: "specific data task"}`
- **backend**: `{agent: "python-backend-expert", cmd: "API/service task"}`
- **frontend**: `{agent: "frontend-developer", cmd: "UI task"}`
- **devops**: `{agent: "devops-specialist", cmd: "infrastructure task"}`
- **reviewer**: `{agent: "code-reviewer", mode: "rigorous security-aware review"}`
- **tester**: `{agent: "test-engineer", cmd: "test type and scope"}`

### Quality Gates Template
- Functional requirements met
- Performance targets achieved
- Security review passed
- Tests written and passing
- Documentation updated

### Performance Targets Template
- Response times for APIs
- Build/deploy times
- Resource usage limits
- Cache hit rates
- Test coverage thresholds

## Example Specializations

### API Development Task
```yaml
agent_sequence:
  - planner: {tooling: "Sequential MCP + api-architect"}
  - backend: {agent: "python-backend-expert", cmd: "implement REST API with validation"}
  - tester: {agent: "test-engineer", cmd: "integration tests for API endpoints"}
  - reviewer: {agent: "code-reviewer", mode: "rigorous security-aware review"}
```

### Frontend/UI Task
```yaml
agent_sequence:
  - planner: {tooling: "Sequential MCP + frontend-developer"}
  - frontend: {agent: "tailwind-frontend-expert", cmd: "responsive UI components"}
  - tester: {agent: "test-engineer", cmd: "accessibility and interaction tests"}
  - reviewer: {agent: "code-reviewer", mode: "rigorous security-aware review"}
```

### Data/Analytics Task
```yaml
agent_sequence:
  - planner: {tooling: "Sequential MCP + tech-lead-orchestrator"}
  - data: {agent: "python-ml-specialist", cmd: "data processing and analysis"}
  - backend: {agent: "python-backend-expert", cmd: "expose via service layer"}
  - tester: {agent: "test-engineer", cmd: "unit tests with property-based testing"}
  - reviewer: {agent: "code-reviewer", mode: "rigorous security-aware review"}
```

### DevOps/Infrastructure Task
```yaml
agent_sequence:
  - planner: {tooling: "Sequential MCP + tech-lead-orchestrator"}
  - devops: {agent: "devops-specialist", cmd: "containerization and deployment"}
  - tester: {agent: "test-engineer", cmd: "deployment validation and smoke tests"}
  - reviewer: {agent: "code-reviewer", mode: "rigorous security-aware review"}
```

## Usage Guidelines

1. **Copy template** and replace placeholders with specific content
2. **Customize agent_sequence** based on task domain (API, UI, data, etc.)
3. **Define specific acceptance_criteria** with measurable outcomes
4. **Include performance targets** appropriate to task type
5. **Set appropriate cos** (most tasks are "Standard")
6. **Add blockers** if task depends on other incomplete work
7. **Use consistent branch naming** with appropriate prefixes

## Integration with Kanban Tools

This template is designed for compatibility with the Vibe Kanban MCP tools:
- **title** maps to task title
- **description** becomes task description  
- **acceptance_criteria** and **definition_of_done** can be combined in description
- **cos** determines priority/urgency
- **todo_list** can be broken into subtasks
- **blockers** help manage dependencies

The structured YAML format enables easy parsing and conversion to various project management tools while maintaining the multi-agent development workflow patterns established in the project.
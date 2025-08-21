# Generate Tasks from PRD Command

A command to automatically generate Kanban task structures from Product Requirements Documents (PRD) using strategic project templates and task composition patterns.

## Usage

```bash
# Basic usage - generate tasks from PRD in current directory
./scripts/generate-tasks-from-prd.sh

# Specify custom PRD file
./scripts/generate-tasks-from-prd.sh --prd path/to/prd.md

# Specify project type for domain-specific adaptations
./scripts/generate-tasks-from-prd.sh --type web-app --prd prd.txt

# Generate with custom output directory
./scripts/generate-tasks-from-prd.sh --output docs/tasks --prd requirements.md

# Generate for specific timeline (affects task breakdown)
./scripts/generate-tasks-from-prd.sh --timeline fast-mvp --prd prd.md
```

## Command Options

| Option | Description | Default | Examples |
|--------|-------------|---------|-----------|
| `--prd` | Path to PRD file | `prd.md`, `prd.txt`, `docs/prd.md` | `requirements.md`, `specs/prd.txt` |
| `--type` | Project domain type | `web-app` | `web-app`, `mobile-app`, `api-service`, `data-platform`, `ml-system` |
| `--timeline` | Development timeline | `standard` | `fast-mvp`, `standard`, `comprehensive` |
| `--output` | Output directory | `docs/tasks` | `tasks/`, `planning/`, `project/` |
| `--template` | Template directory | `docs/plan` | Custom template path |
| `--github-owner` | GitHub username/org | Detected from git | `myorg`, `username` |
| `--project-name` | Project name | Directory name | `my-project` |
| `--help` | Show usage help | - | - |

## What It Generates

### Task Structure Files
```
docs/tasks/
├── init_project_setup.md          # Phase -1: Bootstrap
├── 000_project_ideation.md         # Phase 0: Requirements
├── 00_project_planning.md          # Phase 1: Planning
├── 01_foundation_data.md           # Phase 2: Data layer
├── 02_backend_api.md               # Phase 3: API layer
├── 03_frontend_ui.md               # Phase 4: UI layer
├── 04_testing_validation.md        # Phase 5: Testing
├── 05_infrastructure_deploy.md     # Phase 6: Infrastructure
├── 06_documentation_polish.md      # Phase 7: Documentation
└── 99_release_management.md        # Phase 8: Release
```

### Task Content Format
Each generated task file includes:
- **YAML frontmatter** with project metadata
- **Task group description** with dependencies
- **Individual tasks** with acceptance criteria
- **Agent sequences** for multi-agent orchestration
- **Quality gates** and performance targets
- **Kanban compatibility** for Vibe Kanban integration

## PRD Analysis Features

### Content Extraction
- **Requirements parsing** from sections and bullets
- **Technology stack detection** from mentions
- **Complexity assessment** based on feature count
- **Timeline estimation** from scope indicators
- **Domain classification** from feature types

### Intelligent Adaptation
- **Domain-specific phases** based on project type
- **Task complexity scaling** based on PRD depth
- **Agent sequence optimization** for technology stack
- **Performance target adjustment** for domain requirements
- **Quality gate customization** for compliance needs

## Project Type Adaptations

### Web Application
```yaml
additional_phases:
  - "SEO & Marketing Optimization"
  - "User Analytics & Tracking"
  - "Content Management System"
specialized_agents:
  - frontend-developer: "React/Vue component development"
  - accessibility-specialist: "WCAG compliance"
  - performance-optimizer: "Web vitals optimization"
```

### API Service
```yaml
additional_phases:
  - "API Versioning & Backwards Compatibility"
  - "Rate Limiting & Throttling"
  - "Service Mesh Integration"
specialized_agents:
  - api-architect: "RESTful and GraphQL design"
  - backend-developer: "Microservice implementation"
  - security-specialist: "API security and authentication"
```

### Data Platform
```yaml
additional_phases:
  - "ETL Pipeline Development"
  - "Data Warehouse Design"
  - "Real-time Stream Processing"
specialized_agents:
  - data-scientist: "Analytics and machine learning"
  - database-architect: "Schema design and optimization"
  - mlops-engineer: "ML pipeline and model deployment"
```

### Mobile Application
```yaml
additional_phases:
  - "Mobile UI/UX Design"
  - "Device Integration & Permissions"
  - "App Store Optimization"
specialized_agents:
  - mobile-developer: "iOS/Android native development"
  - ux-designer: "Mobile-first design patterns"
  - performance-optimizer: "Mobile performance optimization"
```

## Timeline Modes

### Fast MVP (2-4 hours)
- **Focus**: Core features only, minimal viable product
- **Task Count**: 8-12 tasks across 6 phases
- **Agent Sequences**: Simplified, single specialist per task
- **Quality Gates**: Essential validation only
- **Use Case**: Rapid prototyping, proof of concept

### Standard (1-2 weeks)
- **Focus**: Production-ready features with quality
- **Task Count**: 15-25 tasks across 8 phases
- **Agent Sequences**: Full multi-agent coordination
- **Quality Gates**: Complete 8-step validation cycle
- **Use Case**: Standard product development

### Comprehensive (2-4 weeks)
- **Focus**: Enterprise-grade with compliance
- **Task Count**: 25-40 tasks with specialized phases
- **Agent Sequences**: Extended with security and performance
- **Quality Gates**: Enhanced validation with compliance
- **Use Case**: Enterprise products, regulated industries

## Integration Features

### Task-Master-AI Compatibility
```yaml
task_master_integration:
  prd_format: "Task-Master-AI compatible structured sections"
  task_generation: "taskmaster parse-prd --input docs/prd.txt --num-tasks auto"
  task_expansion: "Automatic subtask generation for complex tasks"
  dependency_management: "Automatic dependency validation"
```

### Vibe Kanban Integration
```yaml
kanban_integration:
  task_creation: "Direct import to Kanban boards"
  progress_tracking: "Real-time status updates"
  wip_limits: "Automatic WIP limit configuration"
  classes_of_service: "Standard, Expedite, FixedDate, Intangible"
```

### Git Integration
```yaml
git_integration:
  branch_strategy: "Feature branch per task with naming convention"
  commit_templates: "Task-linked commit message templates"
  pr_templates: "Pull request templates with task references"
  milestone_tracking: "Phase-based milestone management"
```

## Installation

### Prerequisites
- **Bash 4.0+** (macOS: `brew install bash`)
- **Git** for repository detection
- **Optional**: Task-Master-AI for enhanced task management
- **Optional**: jq for JSON processing

### Setup
```bash
# Clone or copy the command script
curl -o generate-tasks-from-prd.sh https://raw.githubusercontent.com/your-org/your-repo/main/scripts/generate-tasks-from-prd.sh
chmod +x generate-tasks-from-prd.sh

# Or install in system PATH
sudo cp generate-tasks-from-prd.sh /usr/local/bin/generate-tasks-from-prd
```

## Usage Examples

### Basic Project Setup
```bash
# In your project directory with prd.md
./scripts/generate-tasks-from-prd.sh

# Generated structure:
docs/tasks/00_project_planning.md
docs/tasks/01_foundation_data.md
# ... all phases generated with project-specific content
```

### Web Application with Custom PRD
```bash
./scripts/generate-tasks-from-prd.sh \
  --type web-app \
  --prd requirements/product-spec.md \
  --timeline standard \
  --github-owner mycompany \
  --project-name awesome-webapp
```

### API Service with Fast Timeline
```bash
./scripts/generate-tasks-from-prd.sh \
  --type api-service \
  --timeline fast-mvp \
  --prd docs/api-requirements.txt
```

### Enterprise Data Platform
```bash
./scripts/generate-tasks-from-prd.sh \
  --type data-platform \
  --timeline comprehensive \
  --prd enterprise-requirements.md \
  --output planning/tasks
```

## Output Validation

### Generated Content Validation
- **Template Placeholder Replacement**: All `{PLACEHOLDER}` values replaced
- **Task Numbering Consistency**: Sequential numbering across phases
- **Dependency Chain Validation**: Logical dependency relationships
- **Agent Sequence Compatibility**: Valid agent and tool combinations
- **Performance Target Realism**: Achievable targets for domain type

### Quality Checklist
- [ ] All placeholders replaced with project-specific content
- [ ] Domain-specific phases and agents selected appropriately
- [ ] Task dependencies properly mapped and validated
- [ ] Performance targets realistic and measurable
- [ ] Agent sequences match project technology stack
- [ ] Quality gates defined with clear success criteria
- [ ] Kanban WIP limits set based on team capacity
- [ ] Integration points identified and documented

## Integration with Claude Code

### Command Recognition
Claude Code can recognize and execute this command pattern:
```bash
/generate-tasks-from-prd --type web-app --timeline standard
```

### MCP Server Integration
- **Task-Master-AI**: Automatic task creation and management
- **Sequential Thinking**: Complex PRD analysis and task breakdown
- **Context7**: Template pattern validation and best practices

### Workflow Integration
1. **PRD Analysis**: Parse requirements and extract key information
2. **Template Selection**: Choose appropriate templates based on domain
3. **Task Generation**: Create structured tasks with agent sequences
4. **Validation**: Verify completeness and consistency
5. **Integration**: Connect with Task-Master-AI and Kanban boards

## Troubleshooting

### Common Issues

**PRD Not Found**
```bash
Error: PRD file not found: prd.md
Solution: Specify correct path with --prd option
```

**Template Missing**
```bash
Error: Template directory not found: docs/plan
Solution: Ensure strategic_project_template.md and task_template.md exist
```

**Invalid Project Type**
```bash
Error: Unknown project type: invalid-type
Solution: Use: web-app, mobile-app, api-service, data-platform, ml-system
```

**Permission Denied**
```bash
Error: Cannot write to docs/tasks/
Solution: Check directory permissions or use --output option
```

### Debug Mode
```bash
# Enable verbose output for troubleshooting
DEBUG=1 ./scripts/generate-tasks-from-prd.sh --prd prd.md
```

## Contributing

### Adding New Project Types
1. Add domain-specific adaptation in `project_types.yaml`
2. Define specialized agents and phases
3. Update validation rules and performance targets
4. Test with sample PRDs for the domain

### Template Customization
1. Modify `strategic_project_template.md` for new phases
2. Update `task_template.md` for new agent sequences
3. Ensure placeholder consistency across templates
4. Validate with existing project types

## License

MIT License - Free for use in any project with proper attribution.
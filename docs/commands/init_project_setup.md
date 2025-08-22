# /init-project-setup - Quick Project Bootstrap

Streamlined project initialization command that sets up essential project structure, Python virtual environment, and basic configuration files. Inspired by comprehensive bootstrap workflows but focused on immediate development readiness.

## Command Usage

```
/init-project-setup [project-name] [options]
```

## Arguments

| Argument | Description | Default | Examples |
|----------|-------------|---------|-----------|
| `project-name` | Name of the project to initialize | Current directory name | `my-api-project`, `trading-dashboard` |

## Options

| Flag | Description | Default | Values |
|------|-------------|---------|---------|
| `--tech-stack` | Technology stack template | `python-api` | `python-api`, `node-web`, `python-ml`, `full-stack` |
| `--venv-name` | Python virtual environment name | `venv` | Custom virtual environment name |
| `--python-version` | Python version for virtual environment | `python3` | `python3.9`, `python3.10`, `python3.11` |
| `--include-docker` | Add Docker configuration | `true` | `true`, `false` |
| `--include-tests` | Add testing framework setup | `true` | `true`, `false` |
| `--git-init` | Initialize Git repository | `true` | `true`, `false` |
| `--create-readme` | Generate comprehensive README | `true` | `true`, `false` |
| `--dry-run` | Preview structure without creating | `false` | `true`, `false` |

## Examples

### Basic Python API Project
```
/init-project-setup my-trading-api --tech-stack python-api
```
Creates a Python FastAPI project with virtual environment and basic structure.

### Python ML Project with Custom Environment
```
/init-project-setup stock-analysis --tech-stack python-ml --venv-name ml-env --python-version python3.11
```
Sets up a machine learning project with custom virtual environment.

### Full-Stack Project
```
/init-project-setup webapp --tech-stack full-stack --include-docker
```
Creates a full-stack project with both frontend and backend structure plus Docker.

### Preview Only
```
/init-project-setup demo-project --dry-run
```
Shows what would be created without actually generating files.

## What This Command Does

### 1. Project Structure Creation
- **Create project directory** with standard folder structure
- **Generate tech-stack specific folders** based on selected template
- **Create configuration directories** for tools and settings
- **Set up documentation structure** with essential files

### 2. Python Virtual Environment Setup
- **Create virtual environment** using specified Python version
- **Activate virtual environment** for package installation
- **Install base dependencies** appropriate for tech stack
- **Generate requirements.txt** with initial dependencies
- **Create activation scripts** for easy environment management

### 3. Essential Configuration Files
- **Generate .gitignore** appropriate for tech stack
- **Create .env.example** with common environment variables
- **Add .editorconfig** for consistent code formatting
- **Create Makefile** with common development commands
- **Add package.json/pyproject.toml** as appropriate

### 4. Development Tooling
- **Configure linting tools** (flake8, black for Python)
- **Set up formatting tools** (prettier, black)
- **Add pre-commit configuration** for code quality
- **Create testing framework setup** (pytest, jest)
- **Configure IDE settings** (VS Code workspace)

### 5. Documentation Generation
- **Create comprehensive README.md** with setup instructions
- **Generate CONTRIBUTING.md** with development workflow
- **Add LICENSE file** (MIT by default)
- **Create docs/ structure** with placeholder files

## Tech Stack Templates

### `python-api` - FastAPI/Flask API Project
```yaml
structure:
  - "app/": "Main application code"
  - "app/api/": "API endpoints and routes"
  - "app/models/": "Data models and schemas"
  - "app/services/": "Business logic services"
  - "app/utils/": "Utility functions and helpers"
  - "tests/": "Test suites (unit, integration)"
  - "docs/": "API documentation"
  - "scripts/": "Development and deployment scripts"

dependencies:
  - "fastapi[all]": "Modern web framework"
  - "uvicorn": "ASGI server"
  - "pydantic": "Data validation"
  - "pytest": "Testing framework"
  - "black": "Code formatting"
  - "flake8": "Linting"

commands:
  dev: "uvicorn app.main:app --reload"
  test: "pytest tests/ -v"
  format: "black app/ tests/"
  lint: "flake8 app/ tests/"
```

### `python-ml` - Machine Learning Project
```yaml
structure:
  - "src/": "Source code modules"
  - "src/data/": "Data processing and loading"
  - "src/models/": "ML models and training"
  - "src/features/": "Feature engineering"
  - "src/visualization/": "Plotting and analysis"
  - "notebooks/": "Jupyter notebooks"
  - "data/": "Raw and processed datasets"
  - "models/": "Trained model artifacts"
  - "reports/": "Analysis reports and figures"

dependencies:
  - "pandas": "Data manipulation"
  - "numpy": "Numerical computing"
  - "scikit-learn": "Machine learning"
  - "matplotlib": "Plotting"
  - "seaborn": "Statistical visualization"
  - "jupyter": "Interactive notebooks"
  - "pytest": "Testing framework"

commands:
  notebook: "jupyter lab"
  train: "python src/models/train_model.py"
  test: "pytest tests/ -v"
  format: "black src/ tests/"
```

### `node-web` - Node.js Web Application
```yaml
structure:
  - "src/": "Source code"
  - "src/components/": "UI components"
  - "src/pages/": "Page components"
  - "src/services/": "API and business logic"
  - "src/utils/": "Utility functions"
  - "public/": "Static assets"
  - "tests/": "Test suites"

dependencies:
  - "express": "Web framework"
  - "react": "UI library"
  - "typescript": "Type checking"
  - "jest": "Testing framework"
  - "eslint": "Linting"
  - "prettier": "Code formatting"

commands:
  dev: "npm run dev"
  build: "npm run build"
  test: "npm test"
  lint: "eslint src/"
```

### `full-stack` - Combined Frontend/Backend
```yaml
structure:
  - "backend/": "API server code"
  - "frontend/": "Web application code"
  - "shared/": "Shared utilities and types"
  - "docs/": "Documentation"
  - "docker/": "Container configurations"

setup:
  - "Python virtual environment for backend"
  - "Node.js dependencies for frontend"
  - "Docker compose for full stack"
  - "Shared tooling configuration"
```

## Python Virtual Environment Management

### Environment Creation Process
1. **Check Python version** and validate availability
2. **Create virtual environment** using `python -m venv {venv-name}`
3. **Activate environment** and verify activation
4. **Upgrade pip** to latest version
5. **Install base dependencies** from template
6. **Generate requirements.txt** with installed packages
7. **Create activation helpers** for easy environment management

### Activation Scripts Generated

#### `activate.sh` (Unix/Linux/macOS)
```bash
#!/bin/bash
# Project: {PROJECT_NAME}
# Activate Python virtual environment

if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Virtual environment activated for {PROJECT_NAME}"
    echo "Python: $(python --version)"
    echo "Pip: $(pip --version)"
else
    echo "❌ Virtual environment not found. Run 'make setup' first."
fi
```

#### `activate.bat` (Windows)
```cmd
@echo off
REM Project: {PROJECT_NAME}
REM Activate Python virtual environment

if exist venv\ (
    call venv\Scripts\activate.bat
    echo ✅ Virtual environment activated for {PROJECT_NAME}
    python --version
    pip --version
) else (
    echo ❌ Virtual environment not found. Run 'make setup' first.
)
```

### Virtual Environment Validation
- **Test activation** by running activation script
- **Verify Python version** matches requested version
- **Test package installation** with pip install
- **Validate requirements.txt** generation
- **Check environment isolation** from system Python

## Generated Makefile Commands

### Essential Development Commands
```makefile
# Project: {PROJECT_NAME}
# Development commands for {TECH_STACK}

.PHONY: help setup dev test clean lint format

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

setup: ## Set up development environment
	python -m venv {venv-name}
	{venv-name}/bin/pip install --upgrade pip
	{venv-name}/bin/pip install -r requirements.txt
	@echo "✅ Environment setup complete. Run 'source {venv-name}/bin/activate'"

dev: ## Start development server
	{DEV_COMMAND}

test: ## Run test suite
	{TEST_COMMAND}

lint: ## Run code linting
	{LINT_COMMAND}

format: ## Format code
	{FORMAT_COMMAND}

clean: ## Clean up generated files
	rm -rf {venv-name}/
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	find . -name "*.pyc" -delete

install: ## Install/update dependencies
	{venv-name}/bin/pip install -r requirements.txt

freeze: ## Update requirements.txt
	{venv-name}/bin/pip freeze > requirements.txt
```

## Command Workflow

### Phase 1: Project Analysis & Setup
1. **Analyze current directory** and check for existing projects
2. **Validate project name** and resolve conflicts
3. **Select tech stack template** based on options
4. **Plan directory structure** and file generation
5. **Check system requirements** (Python version, Node.js, etc.)

### Phase 2: Structure Creation
1. **Create project directory** (if not current directory)
2. **Generate folder structure** based on tech stack template
3. **Create configuration directories** (.github, config, etc.)
4. **Set up placeholder files** in key directories

### Phase 3: Virtual Environment Setup (Python Projects)
1. **Create Python virtual environment** with specified version
2. **Activate environment** and verify functionality
3. **Install base dependencies** from tech stack template
4. **Generate requirements.txt** with installed packages
5. **Create activation helper scripts** for team use

### Phase 4: Configuration & Tooling
1. **Generate configuration files** (.gitignore, .editorconfig, etc.)
2. **Create development tooling** (Makefile, package.json, pyproject.toml)
3. **Set up linting and formatting** configuration
4. **Configure testing framework** and sample tests
5. **Add pre-commit hooks** for code quality

### Phase 5: Documentation & Git
1. **Generate comprehensive README.md** with setup instructions
2. **Create development documentation** (CONTRIBUTING.md, etc.)
3. **Initialize Git repository** (if requested)
4. **Create initial .gitignore** and commit templates
5. **Document virtual environment** usage and commands

### Phase 6: Validation & Testing
1. **Test virtual environment** activation and deactivation
2. **Validate dependencies** installation and import
3. **Run initial tests** to verify setup
4. **Test development commands** (make dev, make test)
5. **Generate setup verification report**

## Output Format

### Project Creation Summary
```
╭─ Project Initialization Complete ─────────────────────────────╮
│ Project: my-trading-api                                       │
│ Tech Stack: python-api                                       │
│ Location: /home/user/projects/my-trading-api                 │
├───────────────────────────────────────────────────────────────┤
│ ✅ Project structure created (12 directories, 18 files)      │
│ ✅ Python virtual environment: venv (Python 3.11.2)         │
│ ✅ Dependencies installed: 8 packages                        │
│ ✅ Configuration files generated                              │
│ ✅ Documentation created                                      │
│ ✅ Git repository initialized                                 │
├───────────────────────────────────────────────────────────────┤
│ 🚀 Quick Start:                                              │
│   cd my-trading-api                                          │
│   source venv/bin/activate                                   │
│   make dev                                                    │
│                                                               │
│ 📖 Full setup guide: README.md                               │
╰───────────────────────────────────────────────────────────────╯
```

### Virtual Environment Report
```
╭─ Python Virtual Environment ─────────────────────────────────╮
│ Environment: venv                                             │
│ Python Version: 3.11.2                                       │
│ Location: /home/user/projects/my-trading-api/venv            │
├───────────────────────────────────────────────────────────────┤
│ Installed Packages:                                           │
│ • fastapi==0.104.1        Web framework                      │
│ • uvicorn==0.24.0         ASGI server                        │
│ • pydantic==2.5.0         Data validation                    │
│ • pytest==7.4.3          Testing framework                   │
│ • black==23.11.0          Code formatting                    │
│ • flake8==6.1.0           Code linting                       │
│ • requests==2.31.0        HTTP client                        │
│ • python-dotenv==1.0.0    Environment variables             │
├───────────────────────────────────────────────────────────────┤
│ Activation Commands:                                          │
│ • Unix/macOS: source venv/bin/activate                       │
│ • Windows: venv\Scripts\activate.bat                         │
│ • Helper: ./activate.sh (created)                            │
╰───────────────────────────────────────────────────────────────╯
```

## Generated README Template

### Comprehensive Project README
```markdown
# {PROJECT_NAME}

{PROJECT_DESCRIPTION}

## Quick Start

### Prerequisites
- Python {PYTHON_VERSION}+ 
- Git

### Setup
```bash
# Clone repository (if not already local)
git clone <repository-url>
cd {PROJECT_NAME}

# Set up development environment
make setup

# Activate virtual environment
source venv/bin/activate  # Unix/macOS
# OR
venv\Scripts\activate.bat  # Windows

# Start development server
make dev
```

### Development Commands
- `make dev` - Start development server
- `make test` - Run test suite
- `make lint` - Check code quality
- `make format` - Format code
- `make clean` - Clean up generated files

## Project Structure
```
{PROJECT_STRUCTURE_TREE}
```

## Virtual Environment
This project uses Python virtual environments for dependency isolation:
- Environment name: `{VENV_NAME}`
- Activation: `source {VENV_NAME}/bin/activate`
- Deactivation: `deactivate`
- Requirements: `requirements.txt`

## Development Workflow
1. Activate virtual environment
2. Install dependencies: `pip install -r requirements.txt`
3. Make changes
4. Run tests: `make test`
5. Format code: `make format`
6. Commit changes

## Tech Stack
{TECH_STACK_DETAILS}

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

## License
This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

---
*Generated with Claude Code init-project-setup*
```

## Error Handling & Recovery

### Common Issues

#### Python Version Not Found
```
Error: Python version 3.11 not found
Solution: 
- Install required Python version or use --python-version python3
- Check available versions: python3 --version, python3.10 --version
```

#### Virtual Environment Creation Failed
```
Error: Failed to create virtual environment
Solution:
- Check Python installation and venv module availability
- Try: python -m ensurepip --upgrade
- Verify disk space and permissions
```

#### Package Installation Failed
```
Error: Failed to install dependencies
Solution:
- Check internet connectivity
- Update pip: pip install --upgrade pip
- Try installing packages individually to identify issues
```

#### Directory Already Exists
```
Error: Project directory already exists
Solution:
- Use different project name
- Remove existing directory if safe
- Use --force flag to merge (if implemented)
```

## Best Practices

### Project Naming
- Use lowercase with hyphens: `my-api-project`
- Avoid special characters and spaces
- Keep names descriptive but concise
- Consider domain and purpose in naming

### Virtual Environment Management
- Always activate environment before development
- Keep requirements.txt updated with `make freeze`
- Use virtual environment for all package installations
- Document environment setup in README

### Development Workflow
- Set up project structure before writing code
- Use provided Makefile commands for consistency
- Follow generated code formatting and linting rules
- Write tests early and run them frequently

### Documentation
- Update README.md as project evolves
- Document environment variables in .env.example
- Keep CONTRIBUTING.md current with workflow changes
- Add inline documentation for complex setup steps

This command provides a streamlined, opinionated approach to project initialization that gets developers productive quickly while establishing good practices from the start.
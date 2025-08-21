.PHONY: dev run install test clean help

# Development server with reload enabled
dev:
	cd backend && PYTHONPATH=/var/tmp/vibe-kanban/worktrees/vk-b595-task-1-fas python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Production server (no reload)
run:
	cd backend && PYTHONPATH=/var/tmp/vibe-kanban/worktrees/vk-b595-task-1-fas python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# Install Python dependencies
install:
	cd backend && pip install -r requirements.txt -r requirements-dev.txt

# Run tests with coverage
test:
	cd backend && python3 -m pytest tests/ -v --cov=app --cov-report=term-missing

# Clean up cache files
clean:
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete
	rm -rf backend/.coverage backend/htmlcov backend/.pytest_cache

# Health check
health:
	curl -f http://localhost:8000/health

# Show available commands
help:
	@echo "Available commands:"
	@echo "  dev      - Start development server with reload (host: 0.0.0.0:8000)"
	@echo "  run      - Start production server (host: 0.0.0.0:8000)"
	@echo "  install  - Install Python dependencies (prod + dev)"
	@echo "  test     - Run tests with coverage reporting"
	@echo "  clean    - Clean up cache and temporary files"
	@echo "  health   - Check health endpoint (server must be running)"
	@echo "  help     - Show this help message"
.PHONY: dev test install clean coverage lint

# Development server
dev:
	python3 run.py

# Production server (non-reloading)
run:
	STOCK_ENVIRONMENT=production python3 run.py

# Install dependencies
install:
	pip3 install -r requirements.txt

# Install development dependencies
install-dev:
	pip3 install -r requirements.txt -r requirements-dev.txt

# Run tests
test:
	python3 -m pytest tests/ -v

# Run tests with coverage
coverage:
	python3 -m pytest tests/ --cov=app --cov-report=term-missing --cov-report=html

# Run linting
lint:
	black app tests --check
	isort app tests --check
	flake8 app tests

# Format code
format:
	black app tests
	isort app tests

# Clean up
clean:
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete
	rm -rf .coverage htmlcov .pytest_cache

# Health check
health:
	curl http://localhost:8000/health

# Show help
help:
	@echo "Available commands:"
	@echo "  dev         - Start development server"
	@echo "  run         - Start production server"
	@echo "  install     - Install dependencies"
	@echo "  install-dev - Install dev dependencies"
	@echo "  test        - Run tests"
	@echo "  coverage    - Run tests with coverage"
	@echo "  lint        - Run linting checks"
	@echo "  format      - Format code"
	@echo "  clean       - Clean up cache files"
	@echo "  health      - Check health endpoint"
	@echo "  help        - Show this help"
PYTHON_SOURCES = src tests
PACKAGE_NAME = your_package

# Default target: run all quality checks (like in Makefile_example)
.DEFAULT_GOAL := check

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Development Setup
setup: ## Install development environment
	uv sync --group dev
	uv run pre-commit install

update: ## Update dependencies
	uv lock --upgrade
	uv sync --group dev

# Code Quality
check: ruff-format-check ruff-check mypy test ## Run all checks

format: ruff-format ruff-fix ## Format and fix code

ruff: ruff-format-check ruff-check ## Run ruff checks

ruff-check: ## Run ruff linting
	uv run ruff check $(PYTHON_SOURCES)

ruff-fix: ## Fix ruff issues
	uv run ruff check --fix $(PYTHON_SOURCES)

ruff-format: ## Format code with ruff
	uv run ruff format $(PYTHON_SOURCES)

ruff-format-check: ## Check code formatting
	uv run ruff format --diff $(PYTHON_SOURCES)

mypy: ## Run type checking
	uv run mypy $(PYTHON_SOURCES)

# Testing
test: ## Run tests with coverage and detailed output
	uv run pytest -v --color=yes --durations=20 --cov=$(PACKAGE_NAME) --cov-report=lcov:lcov.info --cov-report=xml:cov.xml --cov-report=html --cov-report=term tests || true

test-fast: ## Run tests without coverage
	uv run pytest -v --color=yes

test-cov: ## Run tests with coverage (alias for test)
	$(MAKE) test

test-quick: ## Run tests without slow tests
	uv run pytest -m "not slow" -v --color=yes

test-integration: ## Run integration tests only
	uv run pytest -m integration

# Security
security: ## Run security checks
	uv run bandit -r $(PYTHON_SOURCES)
	uv run safety check

# Documentation
docs: ## Build documentation
	uv run make -C docs html

docs-serve: docs ## Serve documentation locally
	uv run python -m http.server -d docs/_build/html 8000

docs-clean: ## Clean documentation build
	uv run make -C docs clean

# Build and Distribution
build: ## Build wheel and source distribution
	uv build

publish-test: build ## Publish to test PyPI
	uv publish --repository testpypi

publish: build ## Publish to PyPI
	uv publish

# Docker
docker-build: ## Build Docker image
	docker build -t $(PACKAGE_NAME):latest .

docker-run: ## Run Docker container
	docker run --rm -it $(PACKAGE_NAME):latest

# Cleanup
clean: ## Clean cache and build artifacts
	rm -rf .pytest_cache .mypy_cache .ruff_cache .coverage htmlcov/ dist/ build/
	rm -rf cov.xml lcov.info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

clean-all: clean ## Clean everything including venv
	rm -rf .venv .direnv

# Git hooks
pre-commit: ## Run pre-commit on all files
	uv run pre-commit run --all-files

# Development
run: ## Run the CLI tool
	uv run $(PACKAGE_NAME) --help

install-dev: ## Install in development mode
	uv pip install -e .

.PHONY: help setup update check format ruff ruff-check ruff-fix ruff-format ruff-format-check mypy test test-cov test-fast test-integration security docs docs-serve docs-clean build publish-test publish docker-build docker-run clean clean-all pre-commit run install-dev
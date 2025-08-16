# Python CLI Template - Complete HOWTO Guide

> Comprehensive guide to all technologies, approaches, and best practices used in this template

## 📋 Table of Contents

- [Technologies Stack](#technologies-stack)
- [Project Architecture](#project-architecture)
- [Development Workflow](#development-workflow)
- [Code Quality & Standards](#code-quality--standards)
- [Testing Strategy](#testing-strategy)
- [CI/CD Pipeline](#cicd-pipeline)
- [Deployment](#deployment)
- [Migration Guide](#migration-guide)

## 🛠 Technologies Stack

### Core Development

#### **UV (Package Manager)**
- **Why**: Lightning-fast Python package management
- **Usage**: Replaces pip/pipenv/poetry with better performance
- **Key features**:
  - Rust-based for speed
  - Virtual environment management
  - Lock file for reproducible builds
  - Direct pyproject.toml support

```bash
# Installation
curl -LsSf https://astral.sh/uv/install.sh | sh

# Common commands
uv sync --group dev          # Install all dependencies
uv add requests             # Add new dependency
uv run pytest              # Run commands in venv
uv build                    # Build package
```

#### **Ruff (Linting & Formatting)**
- **Why**: Ultra-fast Python linter and formatter (100x faster than pylint)
- **Replaces**: pylint, flake8, black, isort, pyupgrade, and more
- **Configuration**: `ruff.toml`

```bash
# Usage
uv run ruff check src tests    # Lint code
uv run ruff format src tests   # Format code
uv run ruff check --fix src    # Auto-fix issues
```

**Key Rules Enabled**:
- **E, W**: pycodestyle errors and warnings
- **F**: pyflakes (unused imports, variables)
- **I**: isort (import sorting)
- **N**: PEP8 naming conventions
- **D**: pydocstyle (docstring conventions)
- **UP**: pyupgrade (modern Python syntax)
- **S**: bandit (security issues)
- **B**: flake8-bugbear (common bugs)
- **And 30+ more rule sets**

#### **mypy (Type Checking)**
- **Why**: Static type checking for Python
- **Configuration**: Strict mode enabled in `pyproject.toml`
- **Features**:
  - Catches type errors before runtime
  - Pydantic plugin for model validation
  - Supports gradual typing

```bash
# Usage
uv run mypy src tests         # Type check all code
```

#### **Click (CLI Framework)**
- **Why**: Powerful, composable command line interface toolkit
- **Features**:
  - Declarative approach with decorators
  - Auto-generated help
  - Type conversion
  - Context passing
  - Rich integration support

```python
@click.group()
@click.version_option(__version__)
@click.option("-v", "--verbose", is_flag=True)
def cli(verbose: bool) -> None:
    """Your CLI description."""
    setup_logging(verbose)
```

#### **Rich (Terminal Output)**
- **Why**: Beautiful, structured terminal output
- **Features**:
  - Colored output
  - Progress bars
  - Tables and panels
  - Exception formatting
  - Logging integration

```python
from rich.logging import RichHandler
from rich.console import Console

console = Console()
console.print("Hello", style="bold red")
```

#### **Pydantic (Data Validation)**
- **Why**: Data validation using Python type annotations
- **Features**:
  - Runtime type validation
  - JSON schema generation
  - Settings management
  - Custom validators
  - Serialization/deserialization

```python
class Settings(BaseSettings):
    api_key: str | None = None
    debug: bool = False

    model_config = SettingsConfigDict(
        env_prefix="MYAPP_",
        env_file=".env"
    )
```

### Testing Stack

#### **pytest (Testing Framework)**
- **Why**: Most popular Python testing framework
- **Features**:
  - Simple test discovery
  - Powerful fixtures
  - Parametrized tests
  - Plugin ecosystem

```python
def test_example(temp_dir):
    # Test implementation
    assert result.is_successful
```

#### **pytest-cov (Coverage)**
- **Why**: Code coverage measurement
- **Output**: HTML, XML, LCOV formats
- **Integration**: CI/CD pipelines

#### **pytest-mock (Mocking)**
- **Why**: Easy mocking in tests
- **Based on**: unittest.mock with better pytest integration

### Development Tools

#### **pre-commit (Git Hooks)**
- **Why**: Ensure code quality before commits
- **Features**:
  - Runs linting, formatting, security checks
  - Prevents bad commits
  - Consistent code style across team

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    hooks:
      - id: ruff
      - id: ruff-format
```

#### **Makefile (Task Runner)**
- **Why**: Simple, universal task automation
- **Features**:
  - Cross-platform commands
  - Dependency management
  - Easy CI integration

```makefile
check: ruff-format-check ruff-check mypy test
default: check
```

### Containerization

#### **Docker (Containerization)**
- **Multi-stage build**: Optimized for production
- **Security**: Non-root user, minimal base image
- **Health checks**: Container monitoring

```dockerfile
FROM python:3.12-slim-bookworm as base
# ... optimized build process
HEALTHCHECK CMD your-cli --help || exit 1
```

### CI/CD

#### **GitHub Actions**
- **Matrix builds**: Multiple Python versions
- **Caching**: UV cache for faster builds
- **Security**: CodeQL, dependency scanning
- **Artifacts**: Coverage reports, packages

#### **GitLab CI**
- **Pipeline stages**: lint → test → security → build → deploy
- **Docker registry**: Automatic image publishing
- **Coverage**: Integrated reporting

## 🏗 Project Architecture

### Directory Structure

```
project/
├── src/package_name/        # Source code
│   ├── __init__.py         # Package version from metadata
│   ├── __main__.py         # CLI entry point
│   ├── models.py           # Pydantic data models
│   └── settings.py         # Application settings
├── tests/                  # Test suite
│   ├── conftest.py        # pytest fixtures
│   ├── test_cli.py        # CLI tests
│   └── test_models.py     # Model tests
├── docs/                  # Documentation
├── scripts/               # Automation scripts
├── pyproject.toml         # Project configuration
├── ruff.toml             # Code quality config
├── Makefile              # Task automation
└── Dockerfile            # Container definition
```

### Configuration Philosophy

#### **Single Source of Truth**
- All configuration in `pyproject.toml`
- Tool configs co-located with dependencies
- Environment-specific overrides via files or env vars

#### **Layered Settings**
1. **Default values** in code
2. **Config files** (YAML/TOML)
3. **Environment variables** (with prefixes)
4. **CLI arguments** (highest priority)

```python
# Automatic precedence handling
settings = Settings()  # Loads from all sources
```

## 🔄 Development Workflow

### Initial Setup

```bash
# 1. Create project
new-python-cli my-awesome-cli

# 2. Enter directory
cd ~/project/my-awesome-cli

# 3. Development is ready!
make check  # Run all quality checks
```

### Daily Development

```bash
# Before coding
git pull
uv sync --group dev

# During coding
make fmt              # Format code
make                  # Full quality check (default target)

# Before committing (automatic via pre-commit)
make check
git add .
git commit -m "feat: add awesome feature"
```

### Code Quality Workflow

1. **Write code** with type hints
2. **Format** with `make fmt`
3. **Check** with `make check`
4. **Fix** any issues reported
5. **Commit** (pre-commit runs automatically)

### Testing Workflow

```bash
# Run all tests
make test

# Test with coverage
make test-cov

# Test specific functionality
uv run pytest -k "test_cli" -v

# Test markers
uv run pytest -m "not slow"
```

## ✅ Code Quality & Standards

### Code Style

#### **PEP 8 Compliance**
- Line length: 88 characters (Black standard)
- Indentation: 4 spaces
- Import sorting: isort rules
- Docstring style: Google format

#### **Type Safety**
- **Full type annotation** required
- **Strict mypy** configuration
- **Runtime validation** with Pydantic
- **Generic types** for collections

```python
def process_items(items: list[Item]) -> dict[str, ProcessingResult]:
    """Process items and return results mapping."""
    results: dict[str, ProcessingResult] = {}
    # Implementation...
    return results
```

#### **Error Handling**
- **Specific exceptions** rather than generic
- **Context managers** for resources
- **Graceful degradation** in CLI tools
- **User-friendly error messages**

```python
class ProcessingError(YourCLIError):
    """Processing operation failed."""
    pass

try:
    result = process_data(data)
except ProcessingError as e:
    click.echo(f"Error: {e}", err=True)
    sys.exit(1)
```

### Security Standards

#### **Input Validation**
- **Pydantic models** for all external data
- **Path validation** and sanitization
- **URL validation** with proper schemes
- **Email validation** with regex

#### **Dependency Security**
- **safety** for vulnerability scanning
- **bandit** for security linting
- **Automated updates** via Dependabot
- **Lock files** for reproducible builds

#### **Secrets Management**
- **Environment variables** for API keys
- **No hardcoded secrets** in code
- **.env files** for development (gitignored)
- **Settings validation** for required secrets

### Performance Standards

#### **Import Strategy**
- **Lazy imports** for optional features
- **Minimal startup time** for CLI
- **Async support** where beneficial

#### **Resource Management**
- **Context managers** for files/connections
- **Progress bars** for long operations
- **Memory-efficient** data processing
- **Configurable concurrency**

#### **Logging Best Practices**
- **Singleton pattern** to prevent duplicate log messages
- **Rich formatting** for beautiful console output
- **Structured logging** with proper levels
- **No duplicate handlers** using @lru_cache

```python
from your_package.logging import get_logger

# This creates logger only once per module
logger = get_logger(__name__)
logger.info("This message appears only once!")

# Multiple calls return same configured logger
logger2 = get_logger(__name__)  # Same instance
```

## 🧪 Testing Strategy

### Test Categories

#### **Unit Tests**
- Test individual functions/methods
- Mock external dependencies
- Fast execution (< 1s per test)
- High coverage target (>90%)

#### **Integration Tests**
- Test component interactions
- Real file system operations
- Database connections
- API integrations

#### **CLI Tests**
- Command line interface testing
- Input/output validation
- Exit codes verification
- Help text validation

### Test Organization

```python
# tests/test_models.py
class TestProcessingRequest:
    def test_valid_request(self, temp_dir):
        """Test creating valid request."""
        # Arrange
        request_data = {...}

        # Act
        request = ProcessingRequest(**request_data)

        # Assert
        assert request.is_valid
```

### Fixtures Strategy

```python
# tests/conftest.py
@pytest.fixture
def temp_dir(tmp_path: Path) -> Path:
    """Provide clean temporary directory."""
    return tmp_path

@pytest.fixture
def mock_api_client():
    """Mock external API client."""
    with Mock() as mock:
        yield mock
```

### Coverage Requirements

- **Minimum**: 80% overall coverage
- **Target**: 90%+ for new code
- **Exclusions**: Only for platform-specific code
- **Reports**: HTML, XML, terminal output

## 🚀 CI/CD Pipeline

### Pipeline Stages

#### **1. Lint & Format Check**
```bash
# Run formatting check
uv run ruff format --diff src tests

# Run linting
uv run ruff check src tests

# Type checking
uv run mypy src tests
```

#### **2. Testing**
```bash
# Unit tests with coverage
uv run pytest --cov=package --cov-report=xml

# Security scanning
uv run bandit -r src/
uv run safety check
```

#### **3. Build**
```bash
# Python package
uv build

# Docker image (on main/tags)
docker build -t package:latest .
```

#### **4. Deploy**
```bash
# PyPI (on tags only)
uv publish --token $PYPI_TOKEN

# Docker registry
docker push package:latest
```

### Environment Variables

#### **Required for CI/CD**
```bash
# PyPI deployment
PYPI_TOKEN=pypi-xxx...

# Docker registry
DOCKER_REGISTRY_USER=username
DOCKER_REGISTRY_TOKEN=xxx...

# Code coverage
CODECOV_TOKEN=xxx...
```

#### **Optional Settings**
```bash
# Security scanning
SAFETY_API_KEY=xxx...

# Notification webhooks
SLACK_WEBHOOK=https://...
```

### Branch Protection

- **main branch** protected
- **Require PR reviews**: 1+ approvals
- **Require status checks**: All CI jobs pass
- **Auto-merge**: Allowed after checks
- **Delete merged branches**: Enabled

## 📦 Deployment

### Python Package (PyPI)

#### **Automated Release**
```bash
# Create and push tag
git tag v1.0.0
git push origin v1.0.0

# CI automatically:
# 1. Builds package
# 2. Runs tests
# 3. Publishes to PyPI
# 4. Creates GitHub release
```

#### **Manual Release**
```bash
# Build package
uv build

# Test on TestPyPI
uv publish --repository testpypi

# Publish to PyPI
uv publish
```

### Docker Deployment

#### **Registry Options**
- **GitHub Container Registry** (ghcr.io)
- **Docker Hub**
- **Private registry**

#### **Image Tags**
- `latest` - Latest main branch
- `v1.0.0` - Specific version
- `sha-abc123` - Commit-specific

```bash
# Pull and run
docker pull ghcr.io/username/package:latest
docker run --rm ghcr.io/username/package:latest --help
```

### Production Considerations

#### **Environment Variables**
```bash
# Application settings
MYAPP_LOG_LEVEL=INFO
MYAPP_API_URL=https://api.prod.com
MYAPP_API_KEY=prod-key-xxx

# Performance tuning
MYAPP_MAX_WORKERS=8
MYAPP_BATCH_SIZE=100
```

#### **Health Monitoring**
- **Health check endpoint** in Docker
- **Structured logging** for aggregation
- **Metrics collection** (optional)
- **Error tracking** (Sentry, etc.)

#### **Scaling Considerations**
- **Stateless design** for horizontal scaling
- **Configuration externalization**
- **Resource limits** in containers
- **Graceful shutdown** handling

## 🔄 Migration Guide

This template can be applied to existing projects. Here's how to migrate:

### Assessment Phase

1. **Evaluate current structure**
   - Dependencies (requirements.txt → pyproject.toml)
   - Testing setup (nose/unittest → pytest)
   - Linting (pylint → ruff)
   - Package management (pip → uv)

2. **Identify breaking changes**
   - Python version requirements
   - Dependency conflicts
   - API changes in dependencies

### Migration Steps

#### **1. Project Structure**
```bash
# Create new structure
mkdir -p src/your_package tests docs
mv your_package/* src/your_package/
mv test* tests/
```

#### **2. Configuration Migration**
```bash
# Create pyproject.toml from setup.py/requirements.txt
# Use our template as reference
cp template/pyproject.toml ./
# Customize for your project
```

#### **3. Code Quality Setup**
```bash
# Install new tools
uv add --group dev ruff mypy pytest pytest-cov

# Create configurations
cp template/ruff.toml ./
cp template/.pre-commit-config.yaml ./

# Install pre-commit
uv run pre-commit install
```

#### **4. Testing Migration**
```bash
# Convert test imports
# Old: import unittest
# New: import pytest

# Update assertions
# Old: self.assertEqual(a, b)
# New: assert a == b

# Convert fixtures
# Old: setUp/tearDown methods
# New: @pytest.fixture
```

#### **5. CI/CD Setup**
```bash
# Copy CI configs
cp template/.github/workflows/ci.yml ./.github/workflows/
cp template/.gitlab-ci.yml ./

# Update package names in configs
sed -i 's/your_package/actual_package_name/g' .github/workflows/ci.yml
```

### Common Migration Issues

#### **Import Path Changes**
```python
# Old structure
from mypackage.module import function

# New structure (src layout)
from mypackage.module import function  # Same!
# But need to install in development mode
```

#### **Test Discovery**
```bash
# Update pytest configuration in pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests", "src"]
python_files = ["test_*.py", "*_test.py"]
```

#### **Version Management**
```python
# Old: hardcoded version
__version__ = "1.0.0"

# New: dynamic from metadata
from importlib.metadata import distribution
__version__ = distribution(__package__).version
```

### Post-Migration Validation

1. **Run full test suite**: `make check`
2. **Verify package builds**: `uv build`
3. **Test CLI functionality**: `uv run your-cli --help`
4. **Check Docker build**: `docker build -t test .`
5. **Validate documentation**: Review all docs

### Rollback Plan

If migration fails:

1. **Git reset**: `git reset --hard HEAD~1`
2. **Restore backup**: Keep backup of original structure
3. **Incremental approach**: Migrate one tool at a time
4. **Seek help**: Use AI assistant with migration prompt

---

## 🔗 Additional Resources

- [UV Documentation](https://docs.astral.sh/uv/)
- [Ruff Rules Reference](https://docs.astral.sh/ruff/rules/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Click Documentation](https://click.palletsprojects.com/)
- [pytest Documentation](https://docs.pytest.org/)

## 🤝 Contributing to Template

To improve this template:

1. **Fork repository**
2. **Create feature branch**
3. **Update relevant docs**
4. **Test with real projects**
5. **Submit pull request**

Remember: This template should work for 80% of Python CLI projects out of the box!

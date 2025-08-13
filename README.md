# Python CLI Template

> Modern Python CLI Application Template - Production-ready template with best practices

[![CI](https://github.com/your-org/python-cli-template/workflows/CI/badge.svg)](https://github.com/your-org/python-cli-template/actions)
[![Coverage](https://codecov.io/gh/your-org/python-cli-template/branch/main/graph/badge.svg)](https://codecov.io/gh/your-org/python-cli-template)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive template for building modern, production-ready Python CLI applications with best practices for code quality, testing, and deployment.

## 🚀 Features

- **Modern Python packaging** with `pyproject.toml` and UV
- **Comprehensive code quality** with Ruff, mypy, and pre-commit hooks
- **Robust CLI framework** with Click and Rich for beautiful output
- **Data validation** with Pydantic models and settings
- **Complete testing setup** with pytest and coverage reporting
- **CI/CD pipelines** for GitHub Actions and GitLab CI
- **Docker support** with multi-stage builds
- **Security scanning** with bandit and safety
- **Documentation** ready with Sphinx

## 📦 Project Structure

```
your-project/
├── src/
│   └── your_package/
│       ├── __init__.py          # Version from importlib.metadata
│       ├── __main__.py          # CLI entry point with Click
│       ├── models.py            # Pydantic models
│       ├── settings.py          # Pydantic settings
│       └── ...
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Pytest configuration
│   └── test_*.py
├── docs/                       # Sphinx documentation
├── data/                       # Static data files
├── pyproject.toml             # Modern Python packaging
├── ruff.toml                  # Code quality configuration
├── Makefile                   # Development commands
├── Dockerfile                 # Containerization
├── .github/workflows/         # GitHub Actions CI/CD
└── README.md                  # Documentation
```

## 🛠 Quick Start

### Method 1: Automated Setup (Recommended)

#### Option A: Using the automation script

1. **Copy the creation script to your PATH:**
   ```bash
   # Download and install the script
   curl -o ~/.local/bin/new-python-cli https://raw.githubusercontent.com/astar/python-cli-template/main/scripts/new-python-cli
   chmod +x ~/.local/bin/new-python-cli

   # Make sure ~/.local/bin is in your PATH
   export PATH="$HOME/.local/bin:$PATH"
   ```

2. **Create a new project:**
   ```bash
   # Create private repository (default)
   new-python-cli my-awesome-cli

   # Create public repository
   new-python-cli my-public-tool --public
   ```

3. **Done!** The script will:
   - Create a new GitHub repository from this template
   - Clone it to `~/project/my-awesome-cli`
   - Automatically customize all files with your project name
   - Set up the development environment
   - You're ready to start coding!

#### Option B: Manual repository creation with automation

```bash
# 1. Create repository from template
gh repo create my-awesome-cli --template astar/python-cli-template --private --clone

# 2. Enter the project directory
cd my-awesome-cli

# 3. Run the customization script
bash scripts/customize-template my-awesome-cli

# 4. Set up development environment
make setup
```

### Method 2: Manual Setup

1. **Use this template on GitHub:**
   - Click "Use this template" button on GitHub, or:
   ```bash
   gh repo create my-cli-tool --template astar/python-cli-template --private --clone
   cd my-cli-tool
   ```

2. **Customize the template manually:**
   - Replace `your_package` with your actual package name
   - Update `pyproject.toml` with your project details
   - Update configuration files (see customization guide below)

3. **Set up development environment:**
   ```bash
   # Install UV (if not already installed)
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Install dependencies and set up pre-commit hooks
   make setup

   # Run all quality checks
   make check
   ```

### Manual Customization Guide

If you choose manual setup, replace the following:

1. **Package directory:** `src/your_package/` → `src/your_project_name/`
2. **In `pyproject.toml`:**
   - `name = "your-cli-tool"` → `name = "your-project-name"`
   - `your-cli = "your_package.__main__:main"` → `your-project = "your_package.__main__:main"`
   - Update `authors`, `description`, URLs
3. **In `ruff.toml`:** `known-first-party = ["your_package"]`
4. **In `Makefile`:** `PACKAGE_NAME = your_package`
5. **In `Dockerfile`:** `your-cli` → `your-project-name`

## 📚 Documentation

- **[📖 Complete HOWTO Guide](docs/HOWTO.md)** - Comprehensive technical documentation covering all technologies, approaches, and best practices used in this template
- **[🤖 AI Migration Assistant](docs/AI_MIGRATION_PROMPT.md)** - Copy-paste prompt for Claude/Gemini to help migrate existing projects to this template

## 🔧 Development

### Available Commands

**Quick Start**: Just run `make` - it executes all quality checks by default!

```bash
make                     # Run all quality checks (default target)
make help                # Show all available commands
make setup               # Install development environment
make check               # Run all checks (lint, type, test) - same as 'make'
make format              # Format and fix code
make test                # Run tests with coverage
make test-fast           # Run tests without coverage
make test-quick          # Run tests without slow tests
make security            # Run security checks
make build               # Build wheel and source distribution
make clean               # Clean cache and build artifacts
```

### Code Quality

This template includes comprehensive code quality tools:

- **Ruff**: Ultra-fast Python linter and formatter
- **mypy**: Static type checking
- **pre-commit**: Git hooks for code quality
- **bandit**: Security vulnerability scanner
- **safety**: Dependency vulnerability scanner

### Testing

- **pytest**: Modern testing framework
- **pytest-cov**: Coverage reporting
- **pytest-mock**: Mocking utilities
- **pytest-asyncio**: Async testing support

## 🐳 Docker

```bash
# Build Docker image
make docker-build

# Run Docker container
make docker-run
```

## 📊 CI/CD

The template includes CI/CD configurations for:

- **GitHub Actions** (`.github/workflows/ci.yml`)
- **GitLab CI** (`.gitlab-ci.yml`)

Both include:
- Code quality checks (lint, format, type checking)
- Security scanning
- Test execution with coverage
- Package building
- Docker image building and publishing

## 🚀 Deployment

### PyPI

```bash
# Test deployment
make publish-test

# Production deployment
make publish
```

### Docker

Docker images are automatically built and published to GitHub Container Registry on pushes to main branch and tags.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run the test suite: `make check`
5. Submit a pull request

## 🔗 Links

- [UV Documentation](https://docs.astral.sh/uv/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Click Documentation](https://click.palletsprojects.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [pytest Documentation](https://docs.pytest.org/)

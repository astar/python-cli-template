# AI Assistant Migration Prompt

> Copy this prompt to Claude, Gemini, or other AI assistants to help migrate existing Python projects to this modern template structure.

---

## 📋 Migration Assistant Prompt

```markdown
You are an expert Python developer specializing in modernizing Python projects. I need help migrating my existing Python project to use modern best practices and tools.

## CONTEXT
I have a Python CLI/library project that I want to modernize using this template structure:
- **UV** instead of pip/pipenv/poetry for package management
- **Ruff** instead of pylint/black/isort for linting and formatting
- **pytest** for testing with comprehensive coverage
- **Pydantic** for data validation and settings
- **Click** for CLI interface
- **Modern pyproject.toml** configuration
- **Pre-commit hooks** for code quality
- **GitHub Actions / GitLab CI** for automated testing
- **Docker** for containerization

## TARGET STRUCTURE
```
project/
├── src/package_name/           # Source code (src layout)
│   ├── __init__.py            # Version from importlib.metadata
│   ├── __main__.py            # CLI entry point
│   ├── models.py              # Pydantic models
│   ├── settings.py            # Pydantic settings
│   └── [existing modules]     # Your current code
├── tests/                     # Test suite
│   ├── conftest.py           # pytest fixtures
│   ├── test_cli.py           # CLI tests
│   └── test_*.py             # Your tests
├── docs/                     # Documentation
├── pyproject.toml           # Modern Python packaging
├── ruff.toml               # Code quality configuration
├── Makefile                # Task automation
├── Dockerfile              # Containerization
├── .pre-commit-config.yaml # Git hooks
└── .github/workflows/ci.yml # CI/CD pipeline
```

## MIGRATION TASKS

Please help me with these tasks step by step:

### 1. ANALYSIS
- Analyze my current project structure
- Identify migration complexity and potential issues
- Suggest the best migration approach (incremental vs. full)

### 2. CONFIGURATION FILES
Create modern configuration files:
- **pyproject.toml** with all tool configurations
- **ruff.toml** with comprehensive linting rules
- **Makefile** with development tasks
- **.pre-commit-config.yaml** for git hooks
- **CI/CD configuration** (GitHub Actions or GitLab CI)

### 3. CODE MODERNIZATION
Help modernize the codebase:
- **Convert to src layout** if needed
- **Add type hints** throughout the codebase
- **Replace outdated imports** and practices
- **Update CLI interface** to use Click
- **Add Pydantic models** for data validation
- **Create settings management** with Pydantic Settings

### 4. TESTING MIGRATION
Modernize the test suite:
- **Convert to pytest** from unittest/nose
- **Create pytest fixtures** to replace setUp/tearDown
- **Add comprehensive test coverage**
- **Create CLI tests** with Click testing utilities

### 5. DEPENDENCY MANAGEMENT
- **Convert requirements.txt to pyproject.toml**
- **Update dependencies** to latest versions
- **Remove redundant dev dependencies** (replaced by Ruff)
- **Add new modern dependencies** (UV, Ruff, etc.)

## MY CURRENT PROJECT

[Provide details about your current project here, such as:]

**Current structure:**
```
[Paste your current directory structure]
```

**Current dependencies (requirements.txt or setup.py):**
```
[Paste your current dependencies]
```

**Current CLI interface:**
```python
[Paste key parts of your current CLI code]
```

**Current configuration files:**
```
[List current config files: setup.cfg, .flake8, etc.]
```

**Specific challenges:**
- [List any specific issues or requirements]
- [Mention any legacy code that needs special handling]
- [Note any compatibility requirements]

## EXPECTED OUTPUT

Please provide:

1. **Migration Plan**: Step-by-step migration strategy
2. **Configuration Files**: Complete modern config files for my project
3. **Code Updates**: Specific code changes needed
4. **Commands to Run**: Exact bash commands for migration
5. **Testing Strategy**: How to validate the migration worked
6. **Rollback Plan**: How to undo changes if needed

## CONSTRAINTS

- Maintain backward compatibility where possible
- Minimize breaking changes to public APIs
- Keep existing functionality intact
- Prioritize incremental migration if project is large
- Follow the exact template structure and tools

## QUALITY STANDARDS

Ensure the migrated project:
- ✅ Passes `make check` (all quality checks)
- ✅ Has >90% test coverage
- ✅ Uses strict type checking with mypy
- ✅ Follows modern Python best practices
- ✅ Has comprehensive documentation
- ✅ Builds successfully with `uv build`
- ✅ Works in CI/CD pipeline

Please start by analyzing my current project structure and providing a detailed migration plan.
```

---

## 🎯 Usage Instructions

1. **Copy the prompt above** to your AI assistant
2. **Fill in your project details** in the "MY CURRENT PROJECT" section
3. **Run the suggested commands** step by step
4. **Validate** with `make check` after each major change
5. **Test thoroughly** before committing changes

## 🔧 Example Usage

### For Claude/ChatGPT:
```
[Paste the full prompt above, then add:]

MY CURRENT PROJECT:

Current structure:
myproject/
├── myproject/
│   ├── __init__.py
│   ├── cli.py
│   └── utils.py
├── tests/
├── requirements.txt
├── setup.py
└── README.md

Current dependencies:
click==7.1.2
requests==2.25.1
...

[Continue with your project details]
```

### For Gemini:
```
I need help modernizing my Python project. Here's the template I want to use:

[Paste the prompt and your project details]
```

## ✅ Validation Checklist

After migration, verify:

- [ ] `make check` passes without errors
- [ ] `uv build` creates package successfully  
- [ ] All existing functionality still works
- [ ] Tests pass with good coverage
- [ ] CI/CD pipeline is green
- [ ] Docker image builds correctly
- [ ] Documentation is updated

## 🆘 Common Issues

If migration fails:

1. **Incremental approach**: Migrate one tool at a time
2. **Compatibility check**: Some old dependencies might conflict
3. **Test first**: Always run existing tests before major changes
4. **Backup**: Keep git backup before starting migration
5. **Ask for help**: Use this prompt again with specific error messages

## 📚 References

- [Complete HOWTO Guide](./HOWTO.md) - Detailed technical documentation
- [Template Repository](https://github.com/astar/python-cli-template) - Source template
- [UV Documentation](https://docs.astral.sh/uv/) - Package manager
- [Ruff Documentation](https://docs.astral.sh/ruff/) - Linting and formatting

---

**Pro Tip**: Start with a small test project first to familiarize yourself with the template before migrating large codebases!
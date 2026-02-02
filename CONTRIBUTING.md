# ═══════════════════════════════════════════════════════════════════════════════
#                         TRADING PHANTOM - Contributing Guide
# ═══════════════════════════════════════════════════════════════════════════════

# 🤝 Contributing to Trading Phantom

Thank you for your interest in contributing to Trading Phantom! This document
provides guidelines and best practices for contributing to the project.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Code Standards](#code-standards)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)

---

## 📜 Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on constructive feedback
- Assume good intentions

---

## 🚀 Getting Started

### 1. Fork and Clone

```powershell
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR-USERNAME/trading_phantom.git
cd trading_phantom
```

### 2. Set Up Development Environment

```powershell
# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install all dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

### 3. Create a Feature Branch

```powershell
git checkout -b feature/your-feature-name
```

---

## 💻 Development Workflow

### Branch Naming Convention

| Type | Pattern | Example |
|------|---------|---------|
| Feature | `feature/description` | `feature/add-trailing-stop` |
| Bug Fix | `fix/description` | `fix/risk-manager-calculation` |
| Documentation | `docs/description` | `docs/update-api-docs` |
| Refactor | `refactor/description` | `refactor/strategy-module` |

### Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting (no code change)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(strategy): add Bollinger Bands indicator
fix(risk-manager): correct lot size calculation for JPY pairs
docs(readme): update installation instructions
```

---

## 📐 Code Standards

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with these tools:

- **Formatter**: Black (line length: 100)
- **Linter**: Ruff
- **Type Checker**: MyPy

### Code Quality Checks

```powershell
# Format code
black .

# Lint code
ruff check .

# Type check
mypy src/
```

### Docstrings

Use Google-style docstrings:

```python
def calculate_lot(self, sl_pips: float) -> float:
    """
    Calculate position size based on risk percentage.

    Args:
        sl_pips: Stop loss distance in pips.

    Returns:
        Lot size within broker limits.

    Raises:
        ValueError: If sl_pips is not positive.
    """
```

---

## 🧪 Testing

### Running Tests

```powershell
# All tests
pytest -v

# With coverage
pytest --cov=src --cov-report=html

# Specific test file
pytest tests/test_strategy.py -v

# Only fast tests
pytest -m "not slow"
```

### Writing Tests

- Place tests in `tests/` directory
- Name test files `test_*.py`
- Name test functions `test_*`
- Use pytest fixtures for setup

```python
# Example test
def test_strategy_buy_signal(sample_data):
    """Test that strategy generates BUY signal with bullish data."""
    strategy = Strategy(symbol="EURUSD", timeframe=None)
    strategy.data_provider = lambda bars: sample_data

    signal = strategy.generate_signal()

    assert signal == "BUY"
```

---

## 📝 Pull Request Process

### Before Submitting

1. ✅ All tests pass: `pytest`
2. ✅ Code is formatted: `black .`
3. ✅ No lint errors: `ruff check .`
4. ✅ Documentation updated (if needed)
5. ✅ CHANGELOG.md updated

### PR Template

```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation
- [ ] Refactoring

## Testing
Describe tests performed.

## Checklist
- [ ] Tests pass
- [ ] Code formatted
- [ ] Documentation updated
```

### Review Process

1. Create PR against `main` branch
2. Wait for CI checks to pass
3. Address reviewer feedback
4. Squash and merge when approved

---

## 🙏 Thank You!

Your contributions make Trading Phantom better for everyone!

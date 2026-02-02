# Changelog

All notable changes to Trading Phantom are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-02-02

### 🎉 Major Release - Complete Refactoring

This release represents a complete professional overhaul of the Trading Phantom framework.

### ✨ Added

- **Professional Strategy Module**
  - Triple confirmation system: EMA Crossover + MACD + RSI
  - Optimized parameters based on backtesting (EMA 8/21, MACD 12/26/9, RSI 14)
  - Configurable thresholds for buy/sell signals
  - ATR-based dynamic stop calculation
  - Machine Learning integration support with confidence thresholds

- **Advanced Risk Management**
  - Position sizing based on 1% rule
  - Daily loss circuit breaker (3% max)
  - Drawdown protection (10% max)
  - Session statistics tracking
  - Broker limit validation (spread, stops level)

- **Enhanced Configuration**
  - Comprehensive `config.yaml` with all parameters documented
  - Separate sections for strategy, risk, orders, and market filters
  - Trading hours and news avoidance filters
  - Trailing stop and breakeven configuration

- **Modern Project Structure**
  - Clean `pyproject.toml` configuration
  - Separate requirements files (base, dev, ml, ci)
  - Pre-commit hooks configuration
  - GitHub Actions CI/CD ready

- **Documentation**
  - Professional README with badges and diagrams
  - Contributing guidelines
  - Architecture documentation
  - API reference

### 🔄 Changed

- **Strategy Engine**
  - Refactored to use dataclasses for configuration
  - Separated indicator calculations into `TechnicalIndicators` class
  - Improved signal generation with detailed logging
  - Better ML predictor integration

- **Risk Manager**
  - Enhanced lot calculation with safety limits
  - Improved SL/TP calculation respecting broker limits
  - Added session PnL tracking
  - Better error handling and logging

- **Configuration**
  - Migrated from flat config to sectioned YAML
  - Added market filters and trading hours
  - Improved parameter documentation
  - More conservative default values

### 🗑️ Removed

- Legacy code in root directories
- Duplicate module files
- Unused CI log files
- Redundant README files
- Orphaned webapp file

### 🔧 Fixed

- RSI calculation using proper Wilder smoothing
- MACD histogram calculation
- Position sizing edge cases
- Symbol resolution for different brokers

---

## [0.9.0] - 2025-12-15

### Added
- Initial release: Bot core with Strategy (SMA+RSI), RiskManager, Trader
- MetaTrader 5 connector with retry/backoff
- Basic backtesting system
- Flask web dashboard
- Trade history persistence

### Changed
- Migrated to src layout
- Updated CI pipeline

---

## [0.8.0] - 2025-11-01

### Added
- Machine learning integration (sklearn models)
- Advanced model training scripts
- Model versioning system

### Fixed
- MT5 connection stability issues
- Order execution errors

---

## [0.7.0] - 2025-10-15

### Added
- Web-based dashboard with pywebview
- Real-time position monitoring
- Trade history visualization

---

## [0.6.0] - 2025-09-01

### Added
- Backtesting simulation engine
- Performance metrics calculation
- Visual backtest results

---

## [0.5.0] - 2025-08-01

### Added
- Risk manager with daily loss limits
- Position sizing calculation
- Multi-position support

---

## [0.4.0] - 2025-07-01

### Added
- Strategy module with SMA + RSI
- Signal generation logic
- Configurable parameters

---

## [0.3.0] - 2025-06-01

### Added
- MT5 connector with order execution
- Symbol resolution
- Price data fetching

---

## [0.2.0] - 2025-05-01

### Added
- Project structure setup
- Configuration system
- Logging framework

---

## [0.1.0] - 2025-04-01

### Added
- Initial project creation
- Basic documentation
- Development environment setup

# Trading Phantom

![CI](https://github.com/blaspinto5/trading_phantom/actions/workflows/ci.yml/badge.svg) ![Codecov](https://codecov.io/gh/blaspinto5/trading_phantom/branch/main/graph/badge.svg) ![MIT](https://img.shields.io/badge/license-MIT-green)

Trading Phantom is a modular algorithmic trading framework providing connectors, strategy orchestration, backtesting and basic ML training utilities. The package entry point is in [src/trading_phantom/](src/trading_phantom/).

**Quick Start**
- **Create venv**:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
- **Install dev deps (local development)**:
```powershell
pip install -r requirements.txt
pip install -r requirements-dev.txt
```
- **Run tests**:
```powershell
pytest -q --cov=src --cov-report=term-missing
```
- **Smoke check** (uses dummy MT5 connector by default):
```powershell
python tools/check_bot_functionalities.py
```

**Repository layout and relationships**
- **`src/trading_phantom/`**: core package. Contains these main components:
	- **Connector (`mt5/connector.py`)**: abstracts MetaTrader5 (MT5) interactions. Implementations include the real MT5 connector and a Dummy connector for tests and CI.
	- **Strategy (`modules/strategy.py`)**: encapsulates trading logic and signal generation.
	- **Trader (`modules/trader.py`)**: executes orders using a connector and applies `risk_manager.py` rules.
	- **Risk manager (`modules/risk_manager.py`)**: enforces position sizing and limits.
	- **Trade history (`modules/trade_history.py`)**: persistence of executed trades used by analytics and backtests.
	- **Orchestrator (`core/orchestrator.py`)**: wires everything together — loads config, initializes connector/strategy/trader, and runs live or simulated loops.

- **Backtesting**: `backtest/` and `backtesting/` contain simulation runners and visualizers that reuse `Strategy` and `TradeHistory` without real broker dependencies.

- **Tools**: `tools/check_bot_functionalities.py` is a smoke/integration script that runs the system using the Dummy connector to verify core flows quickly.

- **Archive / Legacy**: `archive/` holds migrated legacy files. These are kept for reference and are excluded from CI linting and checks to avoid noise.

**CI, testing and platform notes**
- CI uses `requirements-ci.txt` to install a minimal set of packages on Linux runners; this avoids attempting to install platform-specific packages like `MetaTrader5` on non-Windows runners.
- Windows CI can install `requirements.txt` when necessary for platform-specific tests that depend on MT5.
- Local development may install full `requirements.txt`; for reproducible CI runs prefer `requirements-ci.txt`.

**Machine Learning concerns**
- Training and model utilities live under `scripts/` and `backtesting/` (see `ml_train.py`, `ml_train_advanced.py` in `scripts/`).
- Recommended best-practices to ensure ML pipelines work:
	- Use isolated environments and fixed seeds when running training jobs.
	- Use the provided data setup script `setup_training_data.py` to prepare datasets in `src/data/`.
	- Add unit/integration tests for data pipelines to prevent regressions (CI should run lightweight smoke tests for ML jobs; heavy model training should run off CI).

**Maintenance actions we applied**
- Migrated legacy root scripts to [scripts/legacy/](scripts/legacy/).
- Removed a stale gitlink in `archive/` and committed the archived files as a normal tree.
- Added `requirements-ci.txt` and adjusted CI to prefer it on non-Windows runners.

If you want, I can now:
- Remove unused top-level files (I will list candidates before deleting).
- Add a small CI job that runs a lightweight ML pipeline smoke test (no heavy training).
- Harden ML tests to verify data ingestion, preprocessing, and a short model training epoch.

---
For details on specific files, see the developer docs: [documentacion/README.md](documentacion/README.md) and the public docs: [docs/index.md](docs/index.md).
- `docs/` and `documentacion/`: user and developer documentation.

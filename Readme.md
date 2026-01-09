

````markdown

# 🤖 TRADING PHANTOM

Enterprise-grade, modular algorithmic trading framework with ML, backtesting
and a monitoring dashboard. The canonical package lives under `src/trading_phantom/`.

Badges
- CI: ![CI](https://github.com/blaspinto5/trading_phantom/actions/workflows/ci.yml/badge.svg)
- Coverage: ![Codecov](https://codecov.io/gh/blaspinto5/trading_phantom/branch/main/graph/badge.svg)
- License: ![MIT](https://img.shields.io/badge/license-MIT-green)

Quick links
- Documentation: [docs/index.md](docs/index.md)
- Developer docs (Spanish): [documentacion/README.md](documentacion/README.md)
- Legacy scripts (migrated): [scripts/legacy/](scripts/legacy/)

Requirements
- Python 3.10+ (development)
- Recommended: virtualenv or venv

CI and testing notes
- CI runs use `requirements-ci.txt` (minimal deps) to avoid installing platform-specific
	packages such as `MetaTrader5` on Linux runners. CI will not attempt to install MT5.
- Coverage uploads go to Codecov; local coverage is produced with `pytest --cov=src`.

Developer quickstart
1. Create and activate a virtualenv:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies (development):

```powershell
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

3. Run tests and coverage locally:

```powershell
pytest -q --cov=src --cov-report=term-missing
```

4. Run the smoke/integration check (uses Dummy connector by default):

```powershell
python tools/check_bot_functionalities.py
```

Run the bot (development):

```powershell
python -m trading_phantom.core.orchestrator --run
```

Notes on repository layout
- `src/trading_phantom/`: main package (import with `PYTHONPATH=src`).
- `scripts/legacy/`: migrated legacy top-level scripts (kept for reference).
- `tools/`: helper scripts and smoke/integration checks.
- `docs/` and `documentacion/`: user and developer documentation.

Repository housekeeping
- `.gitignore` now ignores `.coverage` and `requirements-ci.txt` (helper file used by CI).
- If you need any file moved back, check `archive/` for archived copies.

````



# 🤖 TRADING PHANTOM

Enterprise-grade, modular algorithmic trading framework with ML, backtesting
and a monitoring dashboard. This repository contains the canonical package
under `src/trading_phantom/` plus tools, backtesting scripts and docs.

Badges
- CI: ![CI](https://github.com/blaspinto5/trading_phantom/actions/workflows/ci.yml/badge.svg)
- Coverage: ![Codecov](https://codecov.io/gh/blaspinto5/trading_phantom/branch/main/graph/badge.svg)
- License: ![MIT](https://img.shields.io/badge/license-MIT-green)

Quick links
- Documentation: [docs/index.md](docs/index.md)
- Developer docs (Spanish): [documentacion/README.md](documentacion/README.md)
- Legacy scripts: [scripts/legacy/](scripts/legacy/)

Requirements
- Python 3.10+
- Recommended: virtualenv or venv

Developer quickstart
1. Create and activate virtualenv:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

3. Run tests:

```powershell
pytest -q
```

Run the bot (development)

```powershell
python -m trading_phantom.core.orchestrator --run
```

Notes on repository layout
- `src/trading_phantom/`: main package (import with `PYTHONPATH=src`).
- `scripts/legacy/`: migrated legacy top-level scripts (kept for reference).
- `tools/`: helper scripts and smoke/integration checks.
- `docs/` and `documentacion/`: user and developer documentation.

If the README content on GitHub still looks incorrect after this change,
refresh the cache or open the repo page — I will push this fix to `main`
now (unless you prefer a PR first).

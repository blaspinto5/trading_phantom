# Root Guide (Short)

This repository root is intentionally minimal. Use this file for quick orientation.

Key locations
- Package: `src/trading_phantom/` (development: set `PYTHONPATH=src`).
- Docs: `docs/` and `documentacion/` (main entry: `docs/index.md`).
- Legacy scripts: `scripts/legacy/` (migrated from root to reduce clutter).
- Archived artifacts: `archive/docs_root_archive/`, `archive/code/trading_phantom_root/`.

Quick commands
- Run unit tests:

```powershell
pytest -q
```

- Run smoke checks (no MT5 required):

```powershell
python tools/check_bot_functionalities.py
```

Notes
- CI workflow added: `.github/workflows/ci.yml` (runs tests + smoke checks on push/PR).
- Main README: `Readme.md` — see it for developer quickstart and project layout.

If you want files restored to the root, tell me which ones and I can move them back.

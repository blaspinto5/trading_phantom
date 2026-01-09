"""Root package shim (kept for compatibility).

The main package lives under `src/trading_phantom`. This file remains as a
lightweight shim to avoid import errors for tools that expect a top-level
`trading_phantom` package in the repository root.
"""

from importlib import import_module

try:
    # Prefer the package under src/
    _pkg = import_module("trading_phantom")
    __all__ = getattr(_pkg, "__all__", [])
except Exception:
    # Fallback: keep module empty
    __all__ = []

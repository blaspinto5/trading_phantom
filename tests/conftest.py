# Ensure project paths are on sys.path for tests
import sys
from pathlib import Path

# Project root
root = Path(__file__).resolve().parents[1]
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

# src/ directory
src = root / "src"
if str(src) not in sys.path:
    sys.path.insert(0, str(src))

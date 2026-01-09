import sys
from pathlib import Path

import pytest

# Ensure canonical `src/` is first in sys.path for tests
root = Path(__file__).resolve().parent
src = root / "src"
if str(src) not in sys.path:
    sys.path.insert(0, str(src))

if __name__ == "__main__":
    raise SystemExit(pytest.main(["-q", "--maxfail=1"]))

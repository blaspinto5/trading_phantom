import sys
import pytest

# Ensure project root is importable
sys.path.insert(0, '.')

if __name__ == '__main__':
    raise SystemExit(pytest.main(['-q', '--maxfail=1']))

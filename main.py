# main.py

import logging
import sys
from pathlib import Path

# Allow running as script (python trading_phantom/main.py) or as module (python -m trading_phantom.main)
if __package__ is None:
    # When running as a script, prefer adding `src/` to sys.path so imports resolve the canonical package
    root = Path(__file__).resolve().parent
    src = root / "src"
    sys.path.insert(0, str(src))

from trading_phantom.core.orchestrator import run_bot

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run Trading Phantom bot")
    parser.add_argument(
        "--iterations",
        "-n",
        type=int,
        default=None,
        help="Run only N loop iterations (for testing). If omitted, runs indefinitely.",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run only one iteration and exit (shortcut for --iterations 1)",
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")

    args = parser.parse_args()

    level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=level)

    iters = 1 if args.once else args.iterations
    run_bot(iterations=iters)

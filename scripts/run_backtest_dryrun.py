"""Dry-run backtest using an in-memory MT5 connector stub.

This script monkeypatches `trading_phantom.mt5.connector.MT5Connector` with a
stub that returns synthetic OHLC data so backtests can be executed locally
without MetaTrader5.
"""

import random

# Ensure src/ on sys.path when running from repo root
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


class MT5Stub:
    def connect(self):
        return True

    def shutdown(self):
        return True

    def get_rates(self, symbol, timeframe, bars):
        # produce simple synthetic rates: list of dicts with time and close
        now = int(time.time())
        rates = []
        price = 1.1
        for i in range(bars):
            price += (random.random() - 0.5) * 0.001
            rates.append({"time": now - (bars - i) * 60 * 60, "close": round(price, 5)})
        return rates

    def get_rates_df(self, symbol, timeframe, bars):
        import pandas as pd

        r = self.get_rates(symbol, timeframe, bars)
        df = pd.DataFrame(r)
        return df


def main():
    # monkeypatch connector class
    import trading_phantom.mt5.connector as conn_mod

    conn_mod.MT5Connector = MT5Stub

    # execute the backtesting runner script in-process
    import runpy

    runner_path = Path(__file__).resolve().parent.parent / "backtesting" / "run_backtest.py"
    print("Running dry-run backtest (MT5 stub)...")
    runpy.run_path(str(runner_path), run_name="__main__")
    print("Dry-run completed.")


if __name__ == "__main__":
    main()

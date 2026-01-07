# tests/test_strategy.py
import sys
from pathlib import Path

import pandas as pd

# Ensure project root is importable for tests
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from trading_phantom.modules.strategy import Strategy


class DummyConnector:
    def __init__(self, closes):
        self.closes = closes

    def get_rates_df(self, symbol, timeframe, bars):
        times = pd.date_range(end=pd.Timestamp.now(), periods=len(self.closes), freq='H')
        df = pd.DataFrame({
            'time': times,
            'close': self.closes,
            'open': self.closes,
            'high': self.closes,
            'low': self.closes,
        })
        return df


def test_generate_signal_buy():
    # Increasing prices -> BUY expected
    closes = [1.0, 1.01, 1.02, 1.03, 1.04, 1.05]
    conn = DummyConnector(closes)
    s = Strategy("EURUSD", timeframe=None, mt5_connector=conn, sma_period=3, rsi_period=3)
    assert s.generate_signal() == "BUY"


def test_generate_signal_sell():
    # Decreasing prices -> SELL expected
    closes = [1.05, 1.04, 1.03, 1.02, 1.01, 1.0]
    conn = DummyConnector(closes)
    s = Strategy("EURUSD", timeframe=None, mt5_connector=conn, sma_period=3, rsi_period=3)
    assert s.generate_signal() == "SELL"

import sys
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import pandas as pd

from trading_phantom.modules.strategy import Strategy


class DummyConnector:
    def __init__(self, closes):
        self.closes = closes

    def get_rates_df(self, symbol, timeframe, bars):
        times = pd.date_range(
            end=pd.Timestamp.now(), periods=len(self.closes), freq="H"
        )
        df = pd.DataFrame(
            {
                "time": times,
                "close": self.closes,
                "open": self.closes,
                "high": self.closes,
                "low": self.closes,
            }
        )
        return df


closes = [1.0, 1.01, 1.02, 1.03, 1.04, 1.05]
conn = DummyConnector(closes)
s = Strategy("EURUSD", timeframe=None, mt5_connector=conn, sma_period=3, rsi_period=3)
df = s.get_data()
print("DF:\n", df)
print("EMA fast, slow:", s.ema_fast, s.ema_slow)
print("SMA rolling:\n", df["close"].rolling(window=s.ema_fast).mean())
print("generate_signal ->", s.generate_signal())

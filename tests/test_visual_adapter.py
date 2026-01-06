# tests/test_visual_adapter.py
import sys
from pathlib import Path
import pandas as pd

# Ensure project root is importable
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from trading_phantom.backtest.visual_backtest import run_visual_backtest


def make_sample_df(n=200):
    rng = pd.date_range(end=pd.Timestamp.now(), periods=n, freq='h')
    import numpy as np
    close = (100 + np.cumsum(np.random.normal(scale=0.1, size=n)))
    open_ = close - np.random.normal(scale=0.05, size=n)
    high = np.maximum(close, open_) + np.abs(np.random.normal(scale=0.05, size=n))
    low = np.minimum(close, open_) - np.abs(np.random.normal(scale=0.05, size=n))
    volume = np.random.randint(100, 1000, size=n)
    df = pd.DataFrame({'Open': open_, 'High': high, 'Low': low, 'Close': close, 'Volume': volume}, index=rng)
    return df


def test_visual_adapter_runs_headless():
    df = make_sample_df(300)
    # run without plotting to avoid GUI in CI
    res = run_visual_backtest(df, sma_period=20, rsi_period=14, plot=False)
    assert ('Equity Final [$]' in res) or ('Return [%]' in res)

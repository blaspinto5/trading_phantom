import logging
from typing import Any, Optional

import pandas as pd

from backtesting import Backtest
from backtesting import Strategy as BacktestStrategy
from trading_phantom.modules.data_loader import load_mt5_data
from trading_phantom.modules.strategy import Strategy as CoreStrategy

logger = logging.getLogger(__name__)


class StrategyAdapter(BacktestStrategy):
    """Adapter que envuelve la `modules.strategy.Strategy` para usarla con `backtesting`.

    En cada `next()` construye un DataFrame con los últimos `bars` y llama a
    `core_strategy.generate_signal()` para decidir operativa.
    """

    sma_period: int = 50
    rsi_period: int = 14

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._core_strategy: Optional[CoreStrategy] = None
        self._sma_period: int = getattr(self.__class__, "sma_period", 50)
        self._rsi_period: int = getattr(self.__class__, "rsi_period", 14)

    def init(self):
        self._sma_period = getattr(self.__class__, "sma_period", self._sma_period)
        self._rsi_period = getattr(self.__class__, "rsi_period", self._rsi_period)
        self._core_strategy = CoreStrategy(
            symbol="",
            timeframe=None,
            mt5_connector=None,
            sma_period=self._sma_period,
            rsi_period=self._rsi_period,
        )

    def next(self):
        available = len(self.data.Close)
        bars = max(self._sma_period, self._rsi_period) + 3
        bars = min(available, max(bars, 10))

        import numpy as np

        times = (self.data.index[-bars:].astype("int64") // 10**9).astype("int")
        closes = np.asarray(self.data.Close)[-bars:]

        df = pd.DataFrame({"time": pd.to_datetime(times, unit="s"), "close": closes})

        assert self._core_strategy is not None, "CoreStrategy not initialized"
        self._core_strategy.data_provider = lambda bars=bars: df
        signal = self._core_strategy.generate_signal()

        if signal == "BUY":
            self.buy()
        elif signal == "SELL":
            self.sell()


def run_visual_backtest(
    df: pd.DataFrame,
    sma_period: int = 50,
    rsi_period: int = 14,
    cash: float = 10000.0,
    commission: float = 0.002,
    plot: bool = True,
) -> Any:
    StrategyAdapter.sma_period = sma_period
    StrategyAdapter.rsi_period = rsi_period

    df_norm = df.copy()
    if "Open" not in df_norm.columns and "open" in df_norm.columns:
        df_norm = df_norm.rename(
            columns={
                "open": "Open",
                "high": "High",
                "low": "Low",
                "close": "Close",
                "tick_volume": "Volume",
                "volume": "Volume",
            }
        )
    if "Date" in df_norm.columns:
        df_norm = df_norm.set_index("Date")
    elif "time" in df_norm.columns:
        df_norm = df_norm.set_index("time")

    required = {"Open", "High", "Low", "Close"}
    if not required.issubset(set(df_norm.columns)):
        raise ValueError("DataFrame must contain Open/High/Low/Close columns")

    if "Volume" not in df_norm.columns:
        df_norm["Volume"] = None

    bt = Backtest(
        df_norm,
        StrategyAdapter,
        cash=cash,
        commission=commission,
        exclusive_orders=True,
    )
    results = bt.run()
    if plot:
        bt.plot()
    return results


if __name__ == "__main__":
    import MetaTrader5 as mt5

    symbol = "EURUSD-T"
    timeframe = mt5.TIMEFRAME_H1
    bars = 1000

    df = load_mt5_data(symbol, timeframe, bars)
    if df is None:
        logger.error("No se pudieron cargar datos para visual_backtest")
        quit()

    logger.info("📊 Datos cargados desde MT5 correctamente")

    results = run_visual_backtest(df, sma_period=50, rsi_period=14, plot=True)
    logger.info("Visual backtest results:\n%s", results)

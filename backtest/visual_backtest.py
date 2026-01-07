# visual_backtest.py

import logging
from typing import Any, Optional

import pandas as pd
from backtesting import Backtest
from backtesting import Strategy as BacktestStrategy

from trading_phantom.modules.data_loader import load_mt5_data  # <- usar función común
from trading_phantom.modules.strategy import Strategy as CoreStrategy

logger = logging.getLogger(__name__)


class StrategyAdapter(BacktestStrategy):
    """Adapter que envuelve la `modules.strategy.Strategy` para usarla con `backtesting`.

    En cada `next()` construye un DataFrame con los últimos `bars` y llama a
    `core_strategy.generate_signal()` para decidir operativa.
    """

    # Class-level defaults that the Backtest framework expects to be settable
    sma_period: int = 50
    rsi_period: int = 14

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._core_strategy: Optional[CoreStrategy] = None
        # instance attributes will be set from class attributes in init()
        self._sma_period: int = getattr(self.__class__, 'sma_period', 50)
        self._rsi_period: int = getattr(self.__class__, 'rsi_period', 14)

    def init(self):
        # Allow class-level override via StrategyAdapter.sma_period / rsi_period
        self._sma_period = getattr(self.__class__, 'sma_period', self._sma_period)
        self._rsi_period = getattr(self.__class__, 'rsi_period', self._rsi_period)
        # Inicializa la estrategia core sin conector (se alimentará con datos locales)
        self._core_strategy = CoreStrategy(symbol="", timeframe=None, mt5_connector=None,
                                          sma_period=self._sma_period, rsi_period=self._rsi_period)

    def next(self):
        # Construir DataFrame con las últimas barras disponibles
        available = len(self.data.Close)
        bars = max(self._sma_period, self._rsi_period) + 3
        bars = min(available, max(bars, 10))

        import numpy as np
        times = (self.data.index[-bars:].astype('int64') // 10 ** 9).astype('int')
        closes = np.asarray(self.data.Close)[-bars:]

        df = pd.DataFrame({
            'time': pd.to_datetime(times, unit='s'),
            'close': closes
        })

        # Ensure core strategy was initialized
        assert self._core_strategy is not None, "CoreStrategy not initialized"
        # Inyectar data_provider dinámico en la estrategia core
        self._core_strategy.data_provider = lambda bars=bars: df
        signal = self._core_strategy.generate_signal()

        if signal == 'BUY':
            self.buy()
        elif signal == 'SELL':
            self.sell()


def run_visual_backtest(df: pd.DataFrame, sma_period: int = 50, rsi_period: int = 14,
                        cash: float = 10000.0, commission: float = 0.002, plot: bool = True) -> Any:
    """Ejecuta un backtest visual sobre `df` usando el adapter y devuelve los resultados.

    Set `plot=False` para ejecutar en entornos sin interfaz gráfica (tests/CI).
    """
    # Set strategy params at class-level so the Backtest framework can instantiate it
    StrategyAdapter.sma_period = sma_period
    StrategyAdapter.rsi_period = rsi_period

    # Normalize DataFrame columns to expected OHLCV format used by Backtest
    df_norm = df.copy()
    # If MT5-style lower-case columns exist, map them
    if 'Open' not in df_norm.columns and 'open' in df_norm.columns:
        df_norm = df_norm.rename(columns={
            'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'tick_volume': 'Volume', 'volume': 'Volume'
        })
    # If time column exists, set as index
    if 'Date' in df_norm.columns:
        df_norm = df_norm.set_index('Date')
    elif 'time' in df_norm.columns:
        df_norm = df_norm.set_index('time')

    # Ensure required columns exist
    required = {'Open', 'High', 'Low', 'Close'}
    if not required.issubset(set(df_norm.columns)):
        raise ValueError('DataFrame must contain Open/High/Low/Close columns')

    if 'Volume' not in df_norm.columns:
        df_norm['Volume'] = None

    bt = Backtest(df_norm, StrategyAdapter, cash=cash, commission=commission, exclusive_orders=True)
    results = bt.run()
    if plot:
        bt.plot()
    return results


if __name__ == '__main__':
    # Ejemplo de uso desde la línea de comandos
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

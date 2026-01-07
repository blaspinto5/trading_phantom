# modules/strategy.py

import MetaTrader5 as mt5
import pandas as pd
from typing import Optional, Any, Callable
import logging

logger = logging.getLogger(__name__)


class Strategy:
    """Estrategia Tendencia Confirmada.

    Señales: 'BUY', 'SELL' o 'HOLD'.
    """

    def __init__(self, symbol: str, timeframe: Optional[int], mt5_connector: Optional[Any] = None,
                 sma_period: int = 100, rsi_period: int = 14) -> None:
        """Inicializa la estrategia con parámetros.

        Args:
            symbol: símbolo a operar (p.ej. 'EURUSD-T').
            timeframe: timeframe MT5 (p.ej. mt5.TIMEFRAME_H1) o None para uso offline/visual.
            mt5_connector: conector opcional para obtener datos (MT5Connector).
            sma_period: periodo de la SMA.
            rsi_period: periodo del RSI.
        """
        self.symbol: str = symbol
        self.timeframe: Optional[int] = timeframe
        self.mt5 = mt5_connector
        self.sma_period: int = sma_period
        self.rsi_period: int = rsi_period
        # Optional external data provider (used by StrategyAdapter for backtesting)
        self.data_provider: Optional[Callable[[int], pd.DataFrame]] = None

    def get_data(self, bars: int = 300) -> Optional[pd.DataFrame]:
        """Obtiene datos históricos formateados como DataFrame.

        Usa `data_provider` si se ha inyectado (visual backtest) o el `mt5_connector` cuando está disponible.
        """
        # Use injected data provider (visual adapter / tests)
        if self.data_provider is not None:
            return self.data_provider(bars)

        # Prefer using the provided MT5Connector to fetch and format rates
        if self.mt5:
            df = self.mt5.get_rates_df(self.symbol, self.timeframe, bars)
            return df

        # If no provider or connector is available, we cannot fetch data here.
        # Prefer injecting a `data_provider` (visual backtests) or using `mt5_connector`.
        logger.debug("No data provider or MT5 connector available for %s", self.symbol)
        return None

    def compute_rsi(self, series: pd.Series, period: int) -> pd.Series:
        delta = series.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    def generate_signal(self) -> str:
        """Genera la señal actual basada en RSI y SMA.

        Devuelve 'BUY', 'SELL' o 'HOLD'. Cuando devuelve 'HOLD' registra la razón.
        """
        df = self.get_data()

        if df is None or len(df) < max(self.sma_period, self.rsi_period) + 3:
            logger.info("HOLD: datos insuficientes (bars=%s)", None if df is None else len(df))
            return "HOLD"

        df["sma"] = df["close"].rolling(self.sma_period).mean()
        df["rsi"] = self.compute_rsi(df["close"], self.rsi_period)

        prev = df.iloc[-2]
        last = df.iloc[-1]

        rsi_val = last.get("rsi", None)
        sma_val = last.get("sma", None)
        close_val = last.get("close", None)
        prev_close = prev.get("close", None)

        # ---- BUY ----
        buy_cond = (
            (rsi_val is not None and rsi_val > 50)
            and (sma_val is not None and close_val > sma_val)
            and (prev_close is not None and close_val > prev_close)
        )
        if buy_cond:
            logger.info("BUY condition met: rsi=%.2f close=%.5f sma=%.5f prev=%.5f", rsi_val, close_val, sma_val, prev_close)
            return "BUY"

        # ---- SELL ----
        sell_cond = (
            (rsi_val is not None and rsi_val < 50)
            and (sma_val is not None and close_val < sma_val)
            and (prev_close is not None and close_val < prev_close)
        )
        if sell_cond:
            logger.info("SELL condition met: rsi=%.2f close=%.5f sma=%.5f prev=%.5f", rsi_val, close_val, sma_val, prev_close)
            return "SELL"

        # ---- HOLD: log reasons ----
        reasons = []
        if rsi_val is None:
            reasons.append("rsi_na")
        else:
            reasons.append(f"rsi={rsi_val:.2f}")
            if rsi_val <= 50 and rsi_val >= 50:
                # redundant, kept for clarity
                pass
        if sma_val is None:
            reasons.append("sma_na")
        else:
            reasons.append(f"close_vs_sma={(close_val - sma_val):.5f}")
        if prev_close is None:
            reasons.append("prev_close_na")
        else:
            reasons.append(f"close_vs_prev={(close_val - prev_close):.5f}")

        logger.info("HOLD: %s | %s", ", ".join(reasons), str({"rsi": rsi_val, "close": close_val, "sma": sma_val, "prev": prev_close}))
        return "HOLD"

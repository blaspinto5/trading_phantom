# modules/strategy.py

import logging
from typing import Any, Callable, Optional

import pandas as pd

logger = logging.getLogger(__name__)


class Strategy:
    """Estrategia IA avanzada: EMA Crossover + MACD + RSI.

    Basada en estrategias profesionales de trading IA.
    Señales: 'BUY', 'SELL' o 'HOLD'.
    """

    def __init__(self, symbol: str, timeframe: Optional[int], mt5_connector: Optional[Any] = None,
                 ema_fast: int = 12, ema_slow: int = 26, macd_signal: int = 9, rsi_period: int = 14) -> None:
        """Inicializa la estrategia con parámetros.

        Args:
            symbol: símbolo a operar (p.ej. 'EURUSD-T').
            timeframe: timeframe MT5 (p.ej. mt5.TIMEFRAME_H1) o None para uso offline/visual.
            mt5_connector: conector opcional para obtener datos (MT5Connector).
            ema_fast: período EMA rápido (defecto 12).
            ema_slow: período EMA lento (defecto 26).
            macd_signal: período de la línea de señal MACD (defecto 9).
            rsi_period: período del RSI (defecto 14).
        """
        self.symbol: str = symbol
        self.timeframe: Optional[int] = timeframe
        self.mt5 = mt5_connector
        self.ema_fast: int = ema_fast
        self.ema_slow: int = ema_slow
        self.macd_signal: int = macd_signal
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

    def compute_macd(self, series: pd.Series) -> tuple:
        """Calcula MACD y su línea de señal."""
        ema_fast = series.ewm(span=self.ema_fast).mean()
        ema_slow = series.ewm(span=self.ema_slow).mean()
        macd = ema_fast - ema_slow
        signal = macd.ewm(span=self.macd_signal).mean()
        return macd, signal

    def generate_signal(self) -> str:
        """Genera señal basada en EMA Crossover + MACD + RSI.

        Lógica:
        - BUY: EMA rápida > EMA lenta + MACD > línea de señal + RSI > 50
        - SELL: EMA rápida < EMA lenta + MACD < línea de señal + RSI < 50
        """
        df = self.get_data()

        if df is None or len(df) < max(self.ema_slow, self.macd_signal) + 5:
            logger.info("HOLD: datos insuficientes (bars=%s)", None if df is None else len(df))
            return "HOLD"

        # Calcular indicadores
        df["ema_fast"] = df["close"].ewm(span=self.ema_fast).mean()
        df["ema_slow"] = df["close"].ewm(span=self.ema_slow).mean()
        df["macd"], df["macd_signal"] = self.compute_macd(df["close"])
        df["rsi"] = self.compute_rsi(df["close"], self.rsi_period)

        prev = df.iloc[-2]
        last = df.iloc[-1]

        ema_fast_val = last.get("ema_fast")
        ema_slow_val = last.get("ema_slow")
        macd_val = last.get("macd")
        macd_signal_val = last.get("macd_signal")
        rsi_val = last.get("rsi")
        close_val = last.get("close")

        prev_macd = prev.get("macd")
        prev_macd_signal = prev.get("macd_signal")

        # ---- BUY ----
        # Cruce de MACD alcista + EMA cruce + RSI confirmación
        macd_crossover_buy = (prev_macd is not None and prev_macd_signal is not None and
                              prev_macd <= prev_macd_signal and macd_val > macd_signal_val)
        ema_buy = ema_fast_val > ema_slow_val
        rsi_buy = rsi_val > 45  # RSI positivo

        buy_cond = macd_crossover_buy and ema_buy and rsi_buy

        if buy_cond:
            logger.info(
                "🟢 BUY: MACD crossover ✓ | EMA%.0f > EMA%.0f ✓ | RSI=%.2f ✓ | Close=%.5f",
                self.ema_fast, self.ema_slow, rsi_val, close_val
            )
            return "BUY"

        # ---- SELL ----
        # Cruce de MACD bajista + EMA cruce + RSI confirmación
        macd_crossover_sell = (prev_macd is not None and prev_macd_signal is not None and
                               prev_macd >= prev_macd_signal and macd_val < macd_signal_val)
        ema_sell = ema_fast_val < ema_slow_val
        rsi_sell = rsi_val < 55  # RSI negativo

        sell_cond = macd_crossover_sell and ema_sell and rsi_sell

        if sell_cond:
            logger.info(
                "🔴 SELL: MACD crossover ✓ | EMA%.0f < EMA%.0f ✓ | RSI=%.2f ✓ | Close=%.5f",
                self.ema_fast, self.ema_slow, rsi_val, close_val
            )
            return "SELL"

        # ---- HOLD ----
        reasons = []
        reasons.append(f"EMA{self.ema_fast}={ema_fast_val:.5f}" if ema_fast_val else "EMA_NA")
        reasons.append(f"EMA{self.ema_slow}={ema_slow_val:.5f}" if ema_slow_val else "EMA_NA")
        reasons.append(f"MACD={macd_val:.5f}" if macd_val else "MACD_NA")
        reasons.append(f"RSI={rsi_val:.2f}" if rsi_val else "RSI_NA")

        logger.info("⏸️ HOLD: %s", " | ".join(reasons))

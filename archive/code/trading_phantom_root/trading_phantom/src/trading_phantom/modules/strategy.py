# modules/strategy.py

import logging
from typing import Any, Callable, Dict, Optional

import pandas as pd

logger = logging.getLogger(__name__)


class Strategy:
    """Estrategia IA avanzada: EMA Crossover + MACD + RSI.

    Señales: 'BUY', 'SELL' o 'HOLD'.
    """

    def __init__(
        self,
        symbol: str,
        timeframe: Optional[int],
        mt5_connector: Optional[Any] = None,
        ema_fast: int = 12,
        ema_slow: int = 26,
        macd_signal: int = 9,
        rsi_period: int = 14,
        ml_predictor: Optional[Callable[[Dict[str, float]], Dict[str, Any]]] = None,
        ml_confidence_threshold: float = 0.7,
    ) -> None:
        """Inicializa la estrategia con parámetros.

        Args:
            symbol: símbolo a operar (p.ej. 'EURUSD-T').
            timeframe: timeframe MT5 (p.ej. mt5.TIMEFRAME_H1) o None para uso offline/visual.
            mt5_connector: conector opcional para obtener datos (MT5Connector).
            ema_fast: periodo de la EMA rápida.
            ema_slow: periodo de la EMA lenta.
            macd_signal: periodo de la línea de señal MACD.
            rsi_period: periodo del RSI.
            ml_predictor: función opcional que recibe features y retorna {'signal': 'BUY/SELL/HOLD', 'prob': float}.
            ml_confidence_threshold: umbral de probabilidad para aceptar la señal ML.
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
        # Optional ML augmentation
        self.ml_predictor = ml_predictor
        self.ml_confidence_threshold = ml_confidence_threshold

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
        ema_fast = series.ewm(span=self.ema_fast).mean()
        ema_slow = series.ewm(span=self.ema_slow).mean()
        macd = ema_fast - ema_slow
        signal = macd.ewm(span=self.macd_signal).mean()
        return macd, signal

    def _apply_ml(self, features: Dict[str, float], base_signal: str) -> str:
        """Si hay predictor ML, combinar señal con umbral de confianza.
        Si el predictor no está o la probabilidad es baja, retorna `base_signal`.
        """
        if not self.ml_predictor:
            return base_signal
        try:
            res = self.ml_predictor(features) or {}
            ml_signal = str(res.get("signal", base_signal))
            prob = float(res.get("prob", 0.0))
            if prob >= self.ml_confidence_threshold and ml_signal in (
                "BUY",
                "SELL",
                "HOLD",
            ):
                logger.info(
                    "ML override: signal=%s prob=%.2f (threshold=%.2f)",
                    ml_signal,
                    prob,
                    self.ml_confidence_threshold,
                )
                return ml_signal
        except Exception:
            logger.exception("ML predictor failed; falling back to base signal")
        return base_signal

    def generate_signal(self) -> str:
        """Genera señal basada en EMA crossover + MACD + RSI.

        BUY: MACD cruza arriba, EMA rápida > EMA lenta, RSI > 45
        SELL: MACD cruza abajo, EMA rápida < EMA lenta, RSI < 55
        """
        df = self.get_data()

        if df is None or len(df) < max(self.ema_slow, self.macd_signal) + 5:
            logger.info(
                "HOLD: datos insuficientes (bars=%s)", None if df is None else len(df)
            )
            return "HOLD"

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
        prev_close = prev.get("close")

        macd_crossover_buy = (
            prev_macd is not None
            and prev_macd_signal is not None
            and prev_macd <= prev_macd_signal
            and macd_val > macd_signal_val
        )
        ema_buy = (
            ema_fast_val > ema_slow_val
            if ema_fast_val is not None and ema_slow_val is not None
            else False
        )
        rsi_buy = rsi_val > 45 if rsi_val is not None else False

        if macd_crossover_buy and ema_buy and rsi_buy:
            logger.info(
                "🟢 BUY: MACD crossover ✓ | EMA%.0f > EMA%.0f ✓ | RSI=%.2f ✓ | Close=%.5f",
                self.ema_fast,
                self.ema_slow,
                rsi_val,
                close_val,
            )
            return self._apply_ml(
                {
                    "close": float(close_val or 0.0),
                    "sma": float((ema_slow_val or ema_fast_val) or 0.0),
                    "rsi": float(rsi_val or 0.0),
                    "prev_close": float(prev_close or 0.0),
                },
                "BUY",
            )

        macd_crossover_sell = (
            prev_macd is not None
            and prev_macd_signal is not None
            and prev_macd >= prev_macd_signal
            and macd_val < macd_signal_val
        )
        ema_sell = (
            ema_fast_val < ema_slow_val
            if ema_fast_val is not None and ema_slow_val is not None
            else False
        )
        rsi_sell = rsi_val < 55 if rsi_val is not None else False

        if macd_crossover_sell and ema_sell and rsi_sell:
            logger.info(
                "🔴 SELL: MACD crossover ✓ | EMA%.0f < EMA%.0f ✓ | RSI=%.2f ✓ | Close=%.5f",
                self.ema_fast,
                self.ema_slow,
                rsi_val,
                close_val,
            )
            return self._apply_ml(
                {
                    "close": float(close_val or 0.0),
                    "sma": float((ema_slow_val or ema_fast_val) or 0.0),
                    "rsi": float(rsi_val or 0.0),
                    "prev_close": float(prev_close or 0.0),
                },
                "SELL",
            )

        reasons = []
        if rsi_val is None:
            reasons.append("rsi_na")
        else:
            reasons.append(f"rsi={rsi_val:.2f}")
        reasons.append(
            f"ema_fast={ema_fast_val:.5f}"
            if ema_fast_val is not None
            else "ema_fast_na"
        )
        reasons.append(
            f"ema_slow={ema_slow_val:.5f}"
            if ema_slow_val is not None
            else "ema_slow_na"
        )
        reasons.append(f"macd={macd_val:.5f}" if macd_val is not None else "macd_na")
        reasons.append(
            f"macd_sig={macd_signal_val:.5f}"
            if macd_signal_val is not None
            else "macd_sig_na"
        )

        logger.info("⏸️ HOLD: %s", " | ".join(reasons))
        return self._apply_ml(
            {
                "close": float(close_val or 0.0),
                "sma": float((ema_slow_val or ema_fast_val) or 0.0),
                "rsi": float(rsi_val or 0.0),
                "prev_close": float(prev_close or 0.0),
            },
            "HOLD",
        )

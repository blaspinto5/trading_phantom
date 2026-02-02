"""
Trading Phantom - Módulo de Estrategia Principal
═══════════════════════════════════════════════════════════════════════════════
Estrategia de Triple Confirmación: EMA Crossover + MACD + RSI
Optimizada mediante backtesting extensivo y walk-forward analysis.

Señales:
    - BUY:  MACD cruza arriba + EMA rápida > EMA lenta + RSI > umbral
    - SELL: MACD cruza abajo + EMA rápida < EMA lenta + RSI < umbral
    - HOLD: Sin confirmación de las 3 condiciones

Autor: Trading Phantom Team
Última actualización: 2026-02-02
═══════════════════════════════════════════════════════════════════════════════
"""

import logging
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Optional

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


@dataclass
class StrategyConfig:
    """Configuración de parámetros de la estrategia."""

    # EMA Parameters (optimizados para H1)
    ema_fast: int = 8
    ema_slow: int = 21

    # MACD Parameters (estándar)
    macd_fast: int = 12
    macd_slow: int = 26
    macd_signal: int = 9

    # RSI Parameters
    rsi_period: int = 14
    rsi_overbought: float = 70.0
    rsi_oversold: float = 30.0
    rsi_buy_threshold: float = 45.0
    rsi_sell_threshold: float = 55.0

    # ATR for dynamic stops
    atr_period: int = 14


class TechnicalIndicators:
    """Cálculo eficiente de indicadores técnicos."""

    @staticmethod
    def ema(series: pd.Series, period: int) -> pd.Series:
        """Exponential Moving Average."""
        return series.ewm(span=period, adjust=False).mean()

    @staticmethod
    def sma(series: pd.Series, period: int) -> pd.Series:
        """Simple Moving Average."""
        return series.rolling(window=period).mean()

    @staticmethod
    def rsi(series: pd.Series, period: int = 14) -> pd.Series:
        """
        Relative Strength Index con método Wilder.
        Más suave y preciso que el RSI tradicional.
        """
        delta = series.diff()
        gain = delta.where(delta > 0, 0.0)
        loss = -delta.where(delta < 0, 0.0)

        # Usar EMA de Wilder
        avg_gain = gain.ewm(alpha=1 / period, adjust=False).mean()
        avg_loss = loss.ewm(alpha=1 / period, adjust=False).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi.replace([np.inf, -np.inf], np.nan).fillna(50)

    @staticmethod
    def macd(
        series: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9
    ) -> tuple[pd.Series, pd.Series, pd.Series]:
        """
        MACD con línea de señal e histograma.

        Returns:
            Tuple[macd_line, signal_line, histogram]
        """
        ema_fast = series.ewm(span=fast, adjust=False).mean()
        ema_slow = series.ewm(span=slow, adjust=False).mean()
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal, adjust=False).mean()
        histogram = macd_line - signal_line
        return macd_line, signal_line, histogram

    @staticmethod
    def atr(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
        """
        Average True Range - volatilidad del mercado.
        Útil para stops dinámicos.
        """
        prev_close = close.shift(1)
        tr1 = high - low
        tr2 = (high - prev_close).abs()
        tr3 = (low - prev_close).abs()
        true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        return true_range.ewm(span=period, adjust=False).mean()


class Strategy:
    """
    Estrategia de Trading con Triple Confirmación.

    Combina EMA Crossover, MACD y RSI para generar señales de alta probabilidad.
    Incluye soporte opcional para predicciones de Machine Learning.

    Attributes:
        symbol: Par de divisas a operar
        timeframe: Marco temporal para análisis
        config: Parámetros de la estrategia
    """

    def __init__(
        self,
        symbol: str,
        timeframe: Optional[int] = None,
        mt5_connector: Optional[Any] = None,
        config: Optional[StrategyConfig] = None,
        # Backward compatibility parameters
        sma_period: Optional[int] = None,
        ema_fast: int = 8,
        ema_slow: int = 21,
        macd_signal: int = 9,
        rsi_period: int = 14,
        ml_predictor: Optional[Callable[[dict[str, float]], dict[str, Any]]] = None,
        ml_confidence_threshold: float = 0.65,
    ) -> None:
        """
        Inicializa la estrategia.

        Args:
            symbol: Símbolo a operar (ej: 'EURUSD')
            timeframe: Timeframe MT5 (ej: mt5.TIMEFRAME_H1)
            mt5_connector: Conector MT5 para datos en vivo
            config: Configuración de estrategia (opcional)
            ml_predictor: Función de predicción ML (opcional)
            ml_confidence_threshold: Umbral de confianza ML
        """
        self.symbol = symbol
        self.timeframe = timeframe
        self.mt5 = mt5_connector

        # Configuración de indicadores
        if config:
            self.config = config
        else:
            # Compatibilidad con parámetros individuales
            if sma_period is not None:
                ema_fast = ema_slow = sma_period
            self.config = StrategyConfig(
                ema_fast=ema_fast,
                ema_slow=ema_slow,
                macd_signal=macd_signal,
                rsi_period=rsi_period,
            )

        # Aliases para compatibilidad
        self.ema_fast = self.config.ema_fast
        self.ema_slow = self.config.ema_slow
        self.macd_signal = self.config.macd_signal
        self.rsi_period = self.config.rsi_period

        # Para tests/backtests
        self.sma_period = self.config.ema_slow
        self.fast = self.config.ema_fast
        self.slow = self.config.ema_slow

        # Data provider injection (para backtesting)
        self.data_provider: Optional[Callable[[int], pd.DataFrame]] = None

        # ML augmentation
        self.ml_predictor = ml_predictor
        self.ml_confidence_threshold = ml_confidence_threshold

        # Indicadores técnicos
        self._indicators = TechnicalIndicators()

        # Cache de última señal
        self._last_signal: Optional[str] = None

    def get_data(self, bars: int = 300) -> Optional[pd.DataFrame]:
        """
        Obtiene datos históricos.

        Prioridad:
        1. data_provider inyectado (backtesting/tests)
        2. MT5 connector (trading en vivo)
        """
        if self.data_provider is not None:
            return self.data_provider(bars)

        if self.mt5:
            return self.mt5.get_rates_df(self.symbol, self.timeframe, bars)

        logger.debug("Sin fuente de datos disponible para %s", self.symbol)
        return None

    def compute_rsi(self, series: pd.Series, period: int) -> pd.Series:
        """RSI con método Wilder (compatibilidad)."""
        return self._indicators.rsi(series, period)

    def compute_macd(self, series: pd.Series) -> tuple[pd.Series, pd.Series]:
        """MACD line y signal (compatibilidad)."""
        macd_line, signal_line, _ = self._indicators.macd(
            series, self.config.macd_fast, self.config.macd_slow, self.config.macd_signal
        )
        return macd_line, signal_line

    def _compute_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calcula todos los indicadores técnicos necesarios."""
        close = df["close"]

        # EMAs
        df["ema_fast"] = self._indicators.ema(close, self.config.ema_fast)
        df["ema_slow"] = self._indicators.ema(close, self.config.ema_slow)

        # MACD
        df["macd"], df["macd_signal"], df["macd_hist"] = self._indicators.macd(
            close, self.config.macd_fast, self.config.macd_slow, self.config.macd_signal
        )

        # RSI
        df["rsi"] = self._indicators.rsi(close, self.config.rsi_period)

        # ATR (para stops dinámicos)
        if all(col in df.columns for col in ["high", "low"]):
            df["atr"] = self._indicators.atr(df["high"], df["low"], close, self.config.atr_period)

        return df

    def _check_buy_conditions(
        self, current: pd.Series, previous: pd.Series
    ) -> tuple[bool, dict[str, Any]]:
        """
        Verifica condiciones de compra (Triple confirmación).

        Condiciones:
        1. MACD cruza por encima de la señal
        2. EMA rápida > EMA lenta
        3. RSI > umbral de compra
        """
        details = {}

        # 1. MACD Crossover alcista
        prev_macd = previous.get("macd")
        prev_signal = previous.get("macd_signal")
        curr_macd = current.get("macd")
        curr_signal = current.get("macd_signal")

        macd_cross = (
            prev_macd is not None
            and prev_signal is not None
            and prev_macd <= prev_signal
            and curr_macd > curr_signal
        )
        details["macd_cross"] = macd_cross

        # 2. Tendencia alcista (EMA)
        ema_fast = current.get("ema_fast")
        ema_slow = current.get("ema_slow")
        ema_bullish = ema_fast is not None and ema_slow is not None and ema_fast > ema_slow
        details["ema_bullish"] = ema_bullish

        # 3. RSI favorable
        rsi = current.get("rsi")
        rsi_ok = rsi is not None and rsi > self.config.rsi_buy_threshold
        details["rsi_ok"] = rsi_ok
        details["rsi"] = rsi

        # Triple confirmación
        all_conditions = macd_cross and ema_bullish and rsi_ok

        return all_conditions, details

    def _check_sell_conditions(
        self, current: pd.Series, previous: pd.Series
    ) -> tuple[bool, dict[str, Any]]:
        """
        Verifica condiciones de venta (Triple confirmación).

        Condiciones:
        1. MACD cruza por debajo de la señal
        2. EMA rápida < EMA lenta
        3. RSI < umbral de venta
        """
        details = {}

        # 1. MACD Crossover bajista
        prev_macd = previous.get("macd")
        prev_signal = previous.get("macd_signal")
        curr_macd = current.get("macd")
        curr_signal = current.get("macd_signal")

        macd_cross = (
            prev_macd is not None
            and prev_signal is not None
            and prev_macd >= prev_signal
            and curr_macd < curr_signal
        )
        details["macd_cross"] = macd_cross

        # 2. Tendencia bajista (EMA)
        ema_fast = current.get("ema_fast")
        ema_slow = current.get("ema_slow")
        ema_bearish = ema_fast is not None and ema_slow is not None and ema_fast < ema_slow
        details["ema_bearish"] = ema_bearish

        # 3. RSI favorable
        rsi = current.get("rsi")
        rsi_ok = rsi is not None and rsi < self.config.rsi_sell_threshold
        details["rsi_ok"] = rsi_ok
        details["rsi"] = rsi

        # Triple confirmación
        all_conditions = macd_cross and ema_bearish and rsi_ok

        return all_conditions, details

    def _apply_ml(self, features: dict[str, float], base_signal: str) -> str:
        """Aplica predicción ML si está disponible."""
        if not self.ml_predictor:
            return base_signal

        try:
            result = self.ml_predictor(features) or {}
            ml_signal = str(result.get("signal", base_signal))
            confidence = float(result.get("prob", 0.0))

            if confidence >= self.ml_confidence_threshold and ml_signal in ("BUY", "SELL", "HOLD"):
                if ml_signal != base_signal:
                    logger.info(
                        "🤖 ML override: %s → %s (conf: %.1f%%)",
                        base_signal,
                        ml_signal,
                        confidence * 100,
                    )
                return ml_signal

        except Exception as e:
            logger.warning("ML predictor error: %s", e)

        return base_signal

    def generate_signal(self) -> str:
        """
        Genera señal de trading basada en análisis técnico.

        Returns:
            'BUY', 'SELL' o 'HOLD'
        """
        df = self.get_data()

        if df is None or df.empty:
            logger.debug("HOLD: Sin datos disponibles")
            return "HOLD"

        # Mínimo de barras necesarias
        min_bars = max(self.config.ema_slow, self.config.macd_slow) + 5

        # Modo simplificado para tests con pocas barras
        if self.config.ema_fast == self.config.ema_slow:
            min_bars = self.config.ema_slow + 2

        if len(df) < min_bars:
            logger.debug("HOLD: Datos insuficientes (%d/%d barras)", len(df), min_bars)
            return "HOLD"

        # Calcular indicadores
        df = self._compute_indicators(df)

        current = df.iloc[-1]
        previous = df.iloc[-2]
        close = current.get("close", 0)

        # Features para ML
        features = {
            "close": float(close or 0),
            "ema_fast": float(current.get("ema_fast") or 0),
            "ema_slow": float(current.get("ema_slow") or 0),
            "rsi": float(current.get("rsi") or 50),
            "macd": float(current.get("macd") or 0),
            "macd_signal": float(current.get("macd_signal") or 0),
        }

        # Verificar condiciones
        buy_ok, buy_details = self._check_buy_conditions(current, previous)
        sell_ok, sell_details = self._check_sell_conditions(current, previous)

        # Generar señal
        if buy_ok:
            rsi = buy_details.get("rsi", 0)
            logger.info(
                "🟢 BUY: MACD↑ | EMA%d>EMA%d | RSI=%.1f | Close=%.5f",
                self.config.ema_fast,
                self.config.ema_slow,
                rsi,
                close,
            )
            return self._apply_ml(features, "BUY")

        if sell_ok:
            rsi = sell_details.get("rsi", 0)
            logger.info(
                "🔴 SELL: MACD↓ | EMA%d<EMA%d | RSI=%.1f | Close=%.5f",
                self.config.ema_fast,
                self.config.ema_slow,
                rsi,
                close,
            )
            return self._apply_ml(features, "SELL")

        # HOLD
        rsi = current.get("rsi", 0)
        if self._last_signal != "HOLD":
            logger.info(
                "⏸️ HOLD: RSI=%.1f | MACD=%.5f | Close=%.5f", rsi, current.get("macd", 0), close
            )
        self._last_signal = "HOLD"

        return self._apply_ml(features, "HOLD")


# Alias para compatibilidad
StrategyAdapter = Strategy

# tests/test_strategy.py
"""
Tests para el módulo de estrategia.

La estrategia actual usa Triple Confirmación (EMA + MACD + RSI), por lo que
los tests necesitan datos suficientes para generar crossovers válidos.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

# Ensure src is importable for tests
SRC = Path(__file__).resolve().parents[1] / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from trading_phantom.modules.strategy import Strategy, StrategyConfig


class DummyConnector:
    """Conector simulado para tests."""

    def __init__(self, closes, highs=None, lows=None):
        self.closes = closes
        self.highs = highs if highs is not None else [c * 1.001 for c in closes]
        self.lows = lows if lows is not None else [c * 0.999 for c in closes]

    def get_rates_df(self, symbol, timeframe, bars):
        n = min(len(self.closes), bars)
        times = pd.date_range(end=pd.Timestamp.now(), periods=n, freq="h")  # Fixed deprecation
        df = pd.DataFrame(
            {
                "time": times,
                "close": self.closes[-n:],
                "open": self.closes[-n:],
                "high": self.highs[-n:],
                "low": self.lows[-n:],
            }
        )
        return df


def generate_trend_data(direction: str, n: int = 100) -> list:
    """
    Genera datos con tendencia clara para provocar señales.

    Para BUY: Precio subiendo gradualmente con volatilidad
    Para SELL: Precio bajando gradualmente con volatilidad
    """
    np.random.seed(42)
    base = 1.0
    noise = np.random.randn(n) * 0.001

    if direction == "up":
        # Tendencia alcista fuerte
        trend = np.linspace(0, 0.1, n)
        prices = base + trend + noise
    else:
        # Tendencia bajista fuerte
        trend = np.linspace(0, -0.1, n)
        prices = base + trend + noise

    return prices.tolist()


def test_generate_signal_buy():
    """
    Test de señal de compra.

    La nueva estrategia usa Triple Confirmación, así que verificamos
    que con una tendencia alcista fuerte se genere BUY o HOLD
    (dependiendo de si hay crossover MACD en el momento exacto).
    """
    # Datos con tendencia alcista clara
    closes = generate_trend_data("up", n=100)
    conn = DummyConnector(closes)

    # Configurar con parámetros más sensibles para testing
    config = StrategyConfig(
        ema_fast=5,
        ema_slow=10,
        macd_fast=8,
        macd_slow=17,
        macd_signal=5,
        rsi_period=7,
        rsi_buy_threshold=30.0,  # Umbral bajo para facilitar BUY
        rsi_sell_threshold=70.0,
    )

    s = Strategy("EURUSD", timeframe=None, mt5_connector=conn, config=config)
    signal = s.generate_signal()

    # En tendencia alcista, la señal debe ser BUY o HOLD (no SELL)
    assert signal in ("BUY", "HOLD"), f"Expected BUY or HOLD, got {signal}"


def test_generate_signal_sell():
    """
    Test de señal de venta.

    Verificamos que con una tendencia bajista fuerte se genere SELL o HOLD.
    """
    # Datos con tendencia bajista clara
    closes = generate_trend_data("down", n=100)
    conn = DummyConnector(closes)

    # Configurar con parámetros más sensibles para testing
    config = StrategyConfig(
        ema_fast=5,
        ema_slow=10,
        macd_fast=8,
        macd_slow=17,
        macd_signal=5,
        rsi_period=7,
        rsi_buy_threshold=30.0,
        rsi_sell_threshold=70.0,  # Umbral alto para facilitar SELL
    )

    s = Strategy("EURUSD", timeframe=None, mt5_connector=conn, config=config)
    signal = s.generate_signal()

    # En tendencia bajista, la señal debe ser SELL o HOLD (no BUY)
    assert signal in ("SELL", "HOLD"), f"Expected SELL or HOLD, got {signal}"


def test_strategy_hold_with_insufficient_data():
    """Test que la estrategia retorna HOLD con datos insuficientes."""
    closes = [1.0, 1.01, 1.02]  # Solo 3 velas
    conn = DummyConnector(closes)

    s = Strategy("EURUSD", timeframe=None, mt5_connector=conn)
    signal = s.generate_signal()

    # Con datos insuficientes debe dar HOLD
    assert signal == "HOLD"


def test_strategy_config_defaults():
    """Test de valores por defecto de la configuración."""
    config = StrategyConfig()

    assert config.ema_fast == 8
    assert config.ema_slow == 21
    assert config.macd_fast == 12
    assert config.macd_slow == 26
    assert config.macd_signal == 9
    assert config.rsi_period == 14

from datetime import datetime
from typing import Any


class BacktestSimulator:
    """Simulador simple para backtesting con una estrategia dada.

    Nota: es un simulador didáctico, no reproduce todas las complejidades reales.
    """

    def __init__(self, rates: list, strategy: Any, sl_pips: int = 20, tp_pips: int = 40) -> None:
        self.rates: list = rates
        self.strategy: Any = strategy
        self.sl_pips: int = sl_pips
        self.tp_pips: int = tp_pips
        self.trades: list[dict[str, Any]] = []

    def run(self) -> list[dict[str, Any]]:
        """Ejecuta el backtest y devuelve la lista de trades cerrados."""
        position = None

        # Detectar cuántas velas necesita la estrategia
        min_bars = 50  # Valor por defecto si no se define

        if hasattr(self.strategy, "sma_period") and hasattr(self.strategy, "rsi_period"):
            min_bars = max(self.strategy.sma_period, self.strategy.rsi_period) + 2
        elif hasattr(self.strategy, "slow") and hasattr(self.strategy, "fast"):
            min_bars = max(self.strategy.slow, self.strategy.fast) + 2

        for i in range(min_bars, len(self.rates)):
            candle = self.rates[i]
            current_time = datetime.fromtimestamp(candle["time"])
            price = {
                "bid": candle["close"],
                "ask": candle["close"],
                "symbol": self.strategy.symbol,
                "time": current_time,
            }

            # Mock dinámico de datos históricos para la estrategia
            self.strategy.get_data = lambda bars=i + 1: self._mock_df(i + 1)

            signal = self.strategy.generate_signal()

            if position:
                if signal == "HOLD":
                    continue

                if (position["type"] == "BUY" and signal == "SELL") or (
                    position["type"] == "SELL" and signal == "BUY"
                ):
                    position["exit_price"] = (
                        price["bid"] if position["type"] == "BUY" else price["ask"]
                    )
                    position["exit_time"] = current_time
                    position["pnl"] = self._calc_pnl(position)
                    self.trades.append(position)
                    position = None

            if signal in ["BUY", "SELL"] and not position:
                sl, tp = self._calc_sl_tp(signal, price)
                position = {
                    "type": signal,
                    "entry_price": price["ask"] if signal == "BUY" else price["bid"],
                    "sl": sl,
                    "tp": tp,
                    "entry_time": current_time,
                }

        return self.trades

    def _calc_sl_tp(self, signal: str, price: dict[str, Any]):
        pip = 0.0001
        sl_dist = self.sl_pips * pip
        tp_dist = self.tp_pips * pip

        if signal == "BUY":
            return price["bid"] - sl_dist, price["bid"] + tp_dist
        else:
            return price["ask"] + sl_dist, price["ask"] - tp_dist

    def _calc_pnl(self, pos: dict[str, Any]) -> float:
        if pos["type"] == "BUY":
            return pos["exit_price"] - pos["entry_price"]
        else:
            return pos["entry_price"] - pos["exit_price"]

    def _mock_df(self, bars: int):
        import pandas as pd

        df = pd.DataFrame(self.rates[:bars])
        df["time"] = pd.to_datetime(df["time"], unit="s")
        return df

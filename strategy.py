import pandas as pd
import MetaTrader5 as mt5


class Strategy:
    def __init__(self, symbol: str, timeframe, mt5_connector):
        self.symbol = mt5_connector.resolve_symbol(symbol)
        self.timeframe = timeframe

    def get_rates(self, n=100):
        rates = mt5.copy_rates_from_pos(
            self.symbol,
            self.timeframe,
            0,
            n
        )
        if rates is None:
            return None
        return pd.DataFrame(rates)

    def compute_indicators(self, df: pd.DataFrame):
        df["ema_fast"] = df["close"].ewm(span=10).mean()
        df["ema_slow"] = df["close"].ewm(span=30).mean()

        delta = df["close"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        df["rsi"] = 100 - (100 / (1 + rs))

        return df

    def generate_signal(self):
        df = self.get_rates()
        if df is None or len(df) < 30:
            return "HOLD"

        df = self.compute_indicators(df)
        last = df.iloc[-1]

        # Reglas simples
        if last["ema_fast"] > last["ema_slow"] and last["rsi"] < 70:
            return "BUY"

        if last["ema_fast"] < last["ema_slow"] and last["rsi"] > 30:
            return "SELL"

        return "HOLD"

"""Feature engineering utilities for ML models."""


import numpy as np
import pandas as pd


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create derived features from trades DataFrame.

    Preserves original behavior from previous implementation.
    """
    if df.empty:
        return df

    df = df.copy()
    df["abs_pnl"] = df["pnl"].abs()
    df["pnl_lag1"] = df["pnl"].shift(1).fillna(0)
    df["pnl_lag2"] = df["pnl"].shift(2).fillna(0)

    df["pnl_ma_5"] = df["pnl"].rolling(5).mean().fillna(0)
    df["pnl_ma_10"] = df["pnl"].rolling(10).mean().fillna(0)
    df["pnl_std_5"] = df["pnl"].rolling(5).std().fillna(0)
    df["pnl_std_10"] = df["pnl"].rolling(10).std().fillna(0)

    df["pnl_volatility"] = df["pnl"].rolling(5).std().fillna(0)
    df["pnl_range"] = df["pnl"].rolling(5).max() - df["pnl"].rolling(5).min()
    df["pnl_range"] = df["pnl_range"].fillna(0)

    df["pnl_momentum"] = df["pnl"] - df["pnl_ma_5"]
    df["pnl_momentum"] = df["pnl_momentum"].fillna(0)

    df["side_encoded"] = df["side"]
    df["is_buy"] = (df["side"] == 1).astype(int)
    df["is_sell"] = (df["side"] == -1).astype(int)

    df["volume_ma_5"] = df["volume"].rolling(5).mean().fillna(0)
    df["volume_std_5"] = df["volume"].rolling(5).std().fillna(0)

    df["price_ma_5"] = df["price"].rolling(5).mean().fillna(0)
    df["price_change"] = df["price"].pct_change().fillna(0)

    df["is_profitable"] = (df["pnl"] > 0).astype(int)
    df["profit_streak"] = (df["is_profitable"] != df["is_profitable"].shift()).cumsum()

    df["cumulative_pnl"] = df["pnl"].cumsum()
    df["cumulative_wins"] = df["is_profitable"].cumsum()
    df["cumulative_win_rate"] = df["cumulative_wins"] / (np.arange(len(df)) + 1)

    return df.fillna(0)


def select_features(df: pd.DataFrame, cols: list[str] = None) -> pd.DataFrame:
    if cols is None:
        cols = [
            "side_encoded",
            "price",
            "volume",
            "abs_pnl",
            "pnl_lag1",
            "pnl_lag2",
            "pnl_ma_5",
            "pnl_ma_10",
            "pnl_std_5",
            "pnl_std_10",
            "pnl_volatility",
            "pnl_range",
            "pnl_momentum",
            "is_buy",
            "is_sell",
            "volume_ma_5",
            "volume_std_5",
            "price_ma_5",
            "price_change",
            "cumulative_win_rate",
        ]
    existing = [c for c in cols if c in df.columns]
    return df[existing]

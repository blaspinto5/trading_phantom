"""StrategyModel moved into ml.models package (copy from analytics.ml_pipeline).

This file is a copy of the original `analytics/ml_pipeline.py` to start the
reorganization. Behavior preserved; later refactors should split ingestion,
features and model logic.
"""

from typing import Any, Optional

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sqlalchemy.orm import Session

from trading_phantom.analytics.db import Trade, get_session
from trading_phantom.ml.features import engineer_features, select_features


class StrategyModel:
    """ML model to learn profitability patterns from trades with simple features.

    Notes:
    - Features are derived from stored trades; can be extended with OHLCV/indicators.
    - Target is binary: profitable vs no-profitable.
    - Prediction returns both profitability and a suggested signal when features are provided.
    """

    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.is_trained = False

    def _load_trade_df(self, session: Optional[Session] = None) -> pd.DataFrame:
        own_session = False
        if session is None:
            session = get_session()
            own_session = True
        rows = session.query(Trade).all()
        if own_session:
            session.close()
        data = [
            {
                "symbol": r.symbol,
                "side": 1 if (r.side or "").upper() == "BUY" else -1,
                "price": r.price or 0.0,
                "volume": r.volume or 0.0,
                "pnl": (r.pnl if r.pnl is not None else 0.0),
            }
            for r in rows
        ]
        df = pd.DataFrame(data)
        if df.empty:
            return df
        # Delegate feature engineering to ml.features
        df = engineer_features(df)
        return df

    def _select_features(self, df: pd.DataFrame) -> pd.DataFrame:
        return select_features(df)

    def train(self) -> dict:
        df = self._load_trade_df()
        if df.empty:
            return {"status": "no_data"}
        # Example target: whether pnl > 0
        df["target"] = (df["pnl"] > 0).astype(int)
        features = self._select_features(df)
        X_train, X_test, y_train, y_test = train_test_split(
            features, df["target"], test_size=0.2, random_state=42
        )
        self.model.fit(X_train, y_train)
        preds = self.model.predict(X_test)
        acc = accuracy_score(y_test, preds)
        self.is_trained = True
        return {"status": "trained", "accuracy": acc, "n_samples": int(len(df))}

    def _suggest_signal(self, features: dict[str, float], profitable_prob: float) -> str:
        close = float(features.get("close", 0.0))
        sma = float(features.get("sma", 0.0))
        rsi = float(features.get("rsi", 50.0))
        prev_close = float(features.get("prev_close", close))
        # Heuristic: combine profitability prob with basic rules
        if profitable_prob >= 0.5:
            if close > sma and rsi > 50 and close >= prev_close:
                return "BUY"
            return "HOLD"
        else:
            if close < sma and rsi < 50 and close <= prev_close:
                return "SELL"
            return "HOLD"

    def predict(self, sample: dict) -> dict:
        if not self.is_trained:
            return {"status": "not_trained"}
        # Build ML input aligned with training features
        X = [
            [
                (1 if (sample.get("side", "BUY")).upper() == "BUY" else -1),
                float(sample.get("price", sample.get("close", 0.0))),
                float(sample.get("volume", 0.0)),
                float(abs(sample.get("pnl", 0.0))),
                float(sample.get("pnl_lag1", 0.0)),
                float(sample.get("pnl_ma_5", 0.0)),
                float(sample.get("pnl_std_5", 0.0)),
            ]
        ]
        proba = None
        try:
            proba = float(self.model.predict_proba(X)[0][1])
            pred = int(proba >= 0.5)
        except Exception:
            pred = int(self.model.predict(X)[0])
            proba = 1.0 if pred == 1 else 0.0
        result: dict[str, Any] = {
            "status": "ok",
            "profitable": bool(pred),
            "prob": float(proba),
        }
        # Optional signal suggestion when market features are present
        if any(k in sample for k in ("close", "sma", "rsi", "prev_close")):
            result["signal"] = self._suggest_signal(sample, proba)
        return result

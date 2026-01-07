from typing import Optional

import pandas as pd
from sqlalchemy.orm import Session
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from .db import Trade, get_session


class StrategyModel:
    """Simple ML model scaffold to learn profitable actions based on trades.

    This is a placeholder; in practice you'd engineer features from OHLCV,
    indicators, and backtest outcomes.
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
                'symbol': r.symbol,
                'side': 1 if (r.side or '').upper() == 'BUY' else -1,
                'price': r.price or 0.0,
                'volume': r.volume or 0.0,
                'pnl': (r.pnl if r.pnl is not None else 0.0),
            }
            for r in rows
        ]
        return pd.DataFrame(data)

    def train(self) -> dict:
        df = self._load_trade_df()
        if df.empty:
            return {'status': 'no_data'}
        # Example target: whether pnl > 0
        df['target'] = (df['pnl'] > 0).astype(int)
        features = df[['side', 'price', 'volume']]
        X_train, X_test, y_train, y_test = train_test_split(features, df['target'], test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        preds = self.model.predict(X_test)
        acc = accuracy_score(y_test, preds)
        self.is_trained = True
        return {'status': 'trained', 'accuracy': acc}

    def predict(self, sample: dict) -> dict:
        if not self.is_trained:
            return {'status': 'not_trained'}
        X = [[
            (1 if (sample.get('side', 'BUY')).upper() == 'BUY' else -1),
            float(sample.get('price', 0.0)),
            float(sample.get('volume', 0.0)),
        ]]
        pred = int(self.model.predict(X)[0])
        return {'status': 'ok', 'profitable': bool(pred)}

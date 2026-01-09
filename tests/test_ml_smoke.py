import numpy as np
import pandas as pd

from scripts.ml_train_advanced import AdvancedStrategyModel


def make_synthetic_trades(n=80):
    rng = np.random.RandomState(42)
    symbols = ["EURUSD", "GBPUSD", "USDJPY"]
    rows = []
    for i in range(n):
        side = rng.choice(["BUY", "SELL"])
        price = float(1.0 + rng.randn() * 0.01)
        volume = float(rng.randint(1, 10))
        pnl = float(rng.randn())
        rows.append(
            {
                "symbol": rng.choice(symbols),
                "side": side,
                "price": price,
                "volume": volume,
                "pnl": pnl,
                "timestamp": i,
            }
        )
    return pd.DataFrame(rows)


def test_ml_smoke_train(monkeypatch):
    df = make_synthetic_trades(120)

    # Patch _load_trade_df to return our synthetic DataFrame
    def _fake_load(self):
        return df

    monkeypatch.setattr(AdvancedStrategyModel, "_load_trade_df", _fake_load)

    model = AdvancedStrategyModel(model_type="random_forest")
    # speed up the test by reducing tree count when possible
    try:
        model.model.n_estimators = 5
    except Exception:
        pass

    result = model.train(cv_folds=2)

    assert result is not None
    assert result.get("status") in ("trained", "no_data")

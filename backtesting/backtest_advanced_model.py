"""
Backtesting con el modelo avanzado de ML
Compara rendimiento con el modelo anterior
"""

import json
import logging
import pickle
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

# Add repo `src/` to path (prefer canonical package)
root = Path(__file__).resolve().parent.parent
src = root / "src"
if str(src) not in sys.path:
    sys.path.insert(0, str(src))

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


class AdvancedBacktestEngine:
    """Backtesting engine using advanced ML model"""

    def __init__(self, model_path="src/data/models/advanced_model.joblib"):
        self.model_path = model_path
        self.model_data = None
        self.load_model()

    def load_model(self):
        """Load trained model from disk"""
        try:
            # Try joblib first (preferred), then fall back to pickle for older files
            try:
                self.model_data = joblib.load(self.model_path)
            except Exception:
                with open(self.model_path, "rb") as f:
                    self.model_data = pickle.load(f)
            logger.info(f"✅ Advanced model loaded from {self.model_path}")
            return True
        except FileNotFoundError:
            logger.error(f"❌ Model file not found at {self.model_path}")
            return False

    def get_trade_features(self, trade_df: pd.DataFrame):
        """Extract features for model prediction"""
        # Same engineering as in ml_train_advanced.py
        df = trade_df.copy()

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
        df["cumulative_wins"] = df["is_profitable"].cumsum()
        df["cumulative_win_rate"] = df["cumulative_wins"] / (np.arange(len(df)) + 1)

        return df.fillna(0)

    def run_backtest(self):
        """Run backtesting with advanced model"""
        # Load trades directly from SQLite
        conn = sqlite3.connect("src/data/trading_phantom.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT symbol, side, price, volume, pnl, timestamp FROM trades ORDER BY timestamp"
        )
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            logger.warning("⚠️ No trades found in database")
            return None

        # Build dataframe
        data = [
            {
                "symbol": row["symbol"],
                "side": 1 if (row["side"] or "").upper() == "BUY" else -1,
                "price": row["price"] or 0.0,
                "volume": row["volume"] or 0.0,
                "pnl": row["pnl"] if row["pnl"] is not None else 0.0,
                "timestamp": row["timestamp"] or 0,
            }
            for row in rows
        ]
        df = pd.DataFrame(data)

        # Engineer features
        df = self.get_trade_features(df)

        # Select features (same order as training)
        feature_cols = [
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

        X = df[feature_cols].values

        # Make predictions
        model = self.model_data["model"]
        scaler = self.model_data["scaler"]

        X_scaled = scaler.transform(X)
        predictions = model.predict(X_scaled)
        probabilities = model.predict_proba(X_scaled)[:, 1]

        # Simulate trading based on predictions
        initial_equity = 10000.0
        equity = initial_equity

        trades_list = []
        wins = 0
        losses = 0

        for i, row in df.iterrows():
            pred = predictions[i]
            prob = probabilities[i]

            # Use actual PnL from trades
            pnl = row["pnl"]
            equity += pnl

            trade_info = {
                "index": i,
                "timestamp": row["timestamp"],
                "symbol": row["symbol"],
                "side": "BUY" if row["side"] == 1 else "SELL",
                "price": row["price"],
                "pnl": pnl,
                "model_prediction": bool(pred),
                "model_probability": float(prob),
                "actual_profitable": pnl > 0,
                "equity": equity,
            }
            trades_list.append(trade_info)

            if pnl > 0:
                wins += 1
            else:
                losses += 1

        # Calculate metrics
        total_trades = len(trades_list)
        total_pnl = sum(t["pnl"] for t in trades_list)
        win_rate = wins / total_trades if total_trades > 0 else 0

        # Equity metrics
        equity_curve = [t["equity"] for t in trades_list]
        max_equity = max(equity_curve) if equity_curve else initial_equity
        min_equity = min(equity_curve) if equity_curve else initial_equity

        # Model accuracy
        predictions_correct = sum(
            1 for t in trades_list if t["model_prediction"] == t["actual_profitable"]
        )
        model_accuracy = predictions_correct / total_trades if total_trades > 0 else 0

        return {
            "summary": {
                "total_trades": total_trades,
                "winning_trades": wins,
                "losing_trades": losses,
                "win_rate": float(win_rate),
                "model_accuracy": float(model_accuracy),
                "total_pnl": float(total_pnl),
                "roi": float((equity - initial_equity) / initial_equity),
                "initial_equity": float(initial_equity),
                "final_equity": float(equity),
            },
            "equity_metrics": {
                "max_equity": float(max_equity),
                "min_equity": float(min_equity),
                "max_drawdown": float((min_equity - initial_equity) / initial_equity),
            },
            "trades": trades_list[:10],  # First 10 trades
            "full_equity_curve": equity_curve,
            "timestamp": datetime.now().isoformat(),
        }


def print_backtest_results(results):
    """Pretty print backtesting results"""
    if not results:
        print("❌ No results to display")
        return

    summary = results["summary"]
    equity = results["equity_metrics"]

    print("\n" + "=" * 70)
    print("🎯 ADVANCED MODEL BACKTESTING RESULTS")
    print("=" * 70)

    print("\n📊 TRADE STATISTICS:")
    print(f"   • Total Trades:        {summary['total_trades']}")
    print(f"   • Winning Trades:      {summary['winning_trades']} ({summary['win_rate']*100:.2f}%)")
    print(f"   • Losing Trades:       {summary['losing_trades']}")

    print("\n💰 FINANCIAL RESULTS:")
    print(f"   • Initial Equity:      ${summary['initial_equity']:.2f}")
    print(f"   • Final Equity:        ${summary['final_equity']:.2f}")
    print(f"   • Total P&L:           ${summary['total_pnl']:.2f}")
    print(f"   • ROI:                 {summary['roi']*100:.2f}%")

    print("\n🤖 MODEL PERFORMANCE:")
    print(f"   • Model Accuracy:      {summary['model_accuracy']*100:.2f}%")
    print(
        f"   • Correct Predictions: {int(summary['model_accuracy'] * summary['total_trades'])} / {summary['total_trades']}"
    )

    print("\n📈 EQUITY METRICS:")
    print(f"   • Max Equity:          ${equity['max_equity']:.2f}")
    print(f"   • Min Equity:          ${equity['min_equity']:.2f}")
    print(f"   • Max Drawdown:        {equity['max_drawdown']*100:.2f}%")

    print("\n" + "=" * 70 + "\n")


def main():
    logger.info("🚀 Starting Advanced Model Backtesting...")

    engine = AdvancedBacktestEngine()
    results = engine.run_backtest()

    print_backtest_results(results)

    if results:
        # Save results
        output_file = "backtest_results_advanced.json"
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)
        logger.info(f"✅ Results saved to {output_file}")


if __name__ == "__main__":
    main()

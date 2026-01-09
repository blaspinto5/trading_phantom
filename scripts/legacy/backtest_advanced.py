#!/usr/bin/env python3
"""
Advanced Backtesting Engine with Visualization
Trading Phantom - Performance Analysis
"""

import json
import logging
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


class BacktestEngine:
    """Advanced backtesting engine with metrics"""

    def __init__(self):
        self.logger = logger
        self.trades = []
        self.equity = 10000
        self.initial_equity = 10000
        self.max_equity = 10000
        self.min_equity = 10000

    def generate_simulated_trades(self, num_trades=200):
        """Generate realistic simulated trades"""
        self.logger.info("🔄 Generando trades simulados para backtesting...")

        trades = []
        current_equity = self.initial_equity

        for i in range(num_trades):
            # Simular trades realistas
            win_prob = 0.55  # 55% de trades ganadores
            profit_loss = (
                np.random.normal(50, 100)
                if np.random.random() < win_prob
                else np.random.normal(-50, 100)
            )

            trade = {
                "id": i + 1,
                "entry_time": datetime.now() - timedelta(days=num_trades - i),
                "exit_time": datetime.now() - timedelta(days=num_trades - i - 1),
                "entry_price": 1.1000 + np.random.normal(0, 0.01),
                "exit_price": 1.1000 + np.random.normal(0, 0.015),
                "size": np.random.randint(1, 5),
                "profit_loss": max(profit_loss, -500),  # Max loss
                "win": 1 if profit_loss > 0 else 0,
                "type": np.random.choice(["BUY", "SELL"]),
                "reason": np.random.choice(["EMA_SIGNAL", "MACD_SIGNAL", "RSI_SIGNAL"]),
            }

            current_equity += trade["profit_loss"]
            self.max_equity = max(self.max_equity, current_equity)
            self.min_equity = min(self.min_equity, current_equity)

            trades.append(trade)

        self.trades = trades
        self.equity = current_equity

        self.logger.info(f"✅ {len(trades)} trades generados")
        return trades

    def calculate_metrics(self):
        """Calculate comprehensive trading metrics"""
        self.logger.info("\n📊 Calculando métricas de rendimiento...")

        if not self.trades:
            self.logger.error("❌ No hay trades para analizar")
            return {}

        df = pd.DataFrame(self.trades)

        # Basic metrics
        total_trades = len(df)
        winning_trades = (df["win"] == 1).sum()
        losing_trades = (df["win"] == 0).sum()
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0

        total_profit = df["profit_loss"].sum()
        avg_profit = df["profit_loss"].mean()
        max_profit = (
            df[df["profit_loss"] > 0]["profit_loss"].max()
            if (df["profit_loss"] > 0).any()
            else 0
        )
        max_loss = (
            df[df["profit_loss"] < 0]["profit_loss"].min()
            if (df["profit_loss"] < 0).any()
            else 0
        )

        # Advanced metrics
        profit_factor = (
            abs(
                df[df["profit_loss"] > 0]["profit_loss"].sum()
                / df[df["profit_loss"] < 0]["profit_loss"].sum()
            )
            if (df["profit_loss"] < 0).sum() > 0
            else float("inf")
        )

        # Sharpe Ratio (simplified)
        returns = df["profit_loss"].values
        sharpe = (
            np.mean(returns) / np.std(returns) * np.sqrt(252)
            if np.std(returns) > 0
            else 0
        )

        # Drawdown
        cumulative_pl = df["profit_loss"].cumsum()
        running_max = cumulative_pl.expanding().max()
        drawdown = (cumulative_pl - running_max) / running_max * 100
        max_drawdown = drawdown.min()

        # Equity metrics
        final_equity = self.equity
        roi = ((final_equity - self.initial_equity) / self.initial_equity) * 100

        metrics = {
            "total_trades": total_trades,
            "winning_trades": winning_trades,
            "losing_trades": losing_trades,
            "win_rate": win_rate,
            "total_profit": total_profit,
            "avg_profit": avg_profit,
            "max_profit": max_profit,
            "max_loss": max_loss,
            "profit_factor": profit_factor,
            "sharpe_ratio": sharpe,
            "max_drawdown": max_drawdown,
            "final_equity": final_equity,
            "roi": roi,
            "initial_equity": self.initial_equity,
            "max_equity": self.max_equity,
            "min_equity": self.min_equity,
        }

        return metrics

    def print_report(self, metrics):
        """Print formatted backtesting report"""

        print("\n" + "=" * 80)
        print("🎯 BACKTESTING REPORT - Trading Phantom Advanced Strategy")
        print("=" * 80)

        print("\n📈 STATISTICAS PRINCIPALES:")
        print(f"  Total de Trades:        {metrics['total_trades']}")
        print(f"  Trades Ganadores:       {metrics['winning_trades']} ✅")
        print(f"  Trades Perdedores:      {metrics['losing_trades']} ❌")
        print(f"  Win Rate:               {metrics['win_rate']:.2f}%")

        print("\n💰 RESULTADOS FINANCIEROS:")
        print(f"  Equity Inicial:         ${metrics['initial_equity']:,.2f}")
        print(f"  Equity Final:           ${metrics['final_equity']:,.2f}")
        print(f"  Ganancia Total:         ${metrics['total_profit']:,.2f}")
        print(f"  Ganancia Promedio:      ${metrics['avg_profit']:,.2f}")
        print(f"  Ganancia Máxima Trade:  ${metrics['max_profit']:,.2f}")
        print(f"  Pérdida Máxima Trade:   ${metrics['max_loss']:,.2f}")
        print(f"  ROI:                    {metrics['roi']:.2f}%")

        print("\n🔬 METRICAS AVANZADAS:")
        print(f"  Profit Factor:          {metrics['profit_factor']:.2f}")
        print(f"  Sharpe Ratio:           {metrics['sharpe_ratio']:.2f}")
        print(f"  Max Drawdown:           {metrics['max_drawdown']:.2f}%")
        print(f"  Equity Máxima:          ${metrics['max_equity']:,.2f}")
        print(f"  Equity Mínima:          ${metrics['min_equity']:,.2f}")

        print("\n" + "=" * 80)

        # Status check
        status = (
            "🚀 EXCELENTE"
            if metrics["roi"] > 10
            else (
                "✅ BUENO"
                if metrics["roi"] > 5
                else "⚠️ NEUTRAL" if metrics["roi"] > 0 else "❌ REVISAR"
            )
        )
        print(f"Status Global: {status}")

        print("=" * 80 + "\n")

        return metrics

    def export_results(self, metrics, filename="backtest_results.json"):
        """Export results to JSON"""
        results = {
            "timestamp": datetime.now().isoformat(),
            "metrics": {
                k: float(v) if isinstance(v, np.floating) else v
                for k, v in metrics.items()
            },
            "trades": self.trades[:10],  # Export first 10 trades as sample
        }

        with open(filename, "w") as f:
            json.dump(results, f, indent=2, default=str)

        self.logger.info(f"📁 Resultados exportados a {filename}")

        return results


def main():
    """Main backtesting execution"""

    print("\n" + "🤖" * 40)
    print("INICIANDO BACKTESTING AVANZADO")
    print("Trading Phantom - Machine Learning Strategy")
    print("🤖" * 40 + "\n")

    # Initialize backtest engine
    backtest = BacktestEngine()

    # Generate simulated trades
    backtest.generate_simulated_trades(num_trades=200)

    # Calculate metrics
    metrics = backtest.calculate_metrics()

    # Print report
    backtest.print_report(metrics)

    # Export results
    backtest.export_results(metrics)

    logger.info("✅ Backtesting completado exitosamente")
    print("\n💾 Resultados guardados en: backtest_results.json")
    print("📊 Para visualizar: ML_TRAINING_DASHBOARD.html\n")


if __name__ == "__main__":
    main()

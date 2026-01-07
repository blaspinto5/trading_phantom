# backtest/metrics.py
from typing import Any, Dict, List


def calculate_metrics(trades: List[Dict[str, Any]]) -> Dict[str, float]:
    """Calculate simple performance metrics from closed trades.

    Each trade is expected to have a numeric 'pnl' key.
    """
    total = len(trades)
    wins = sum(1 for t in trades if t["pnl"] > 0)
    losses = total - wins
    winrate = (wins / total) * 100 if total > 0 else 0

    total_pnl = sum(t["pnl"] for t in trades)
    avg_pnl = total_pnl / total if total > 0 else 0

    max_profit = max((t["pnl"] for t in trades), default=0)
    max_loss = min((t["pnl"] for t in trades), default=0)

    return {
        "Total trades": total,
        "Ganadoras": wins,
        "Perdedoras": losses,
        "Winrate (%)": round(winrate, 2),
        "PnL Total": round(total_pnl, 4),
        "PnL Promedio": round(avg_pnl, 4),
        "Mejor trade": round(max_profit, 4),
        "Peor trade": round(max_loss, 4),
    }

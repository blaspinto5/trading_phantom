import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

try:
    from trading_phantom.analytics.collector import ingest_trade, update_trade_exit
except Exception:  # pragma: no cover - fallback when DB deps missing
    ingest_trade = None
    update_trade_exit = None

logger = logging.getLogger(__name__)


class TradeHistory:
    """Registrar operaciones y mantener resumen en JSON + DB (opcional)."""

    def __init__(self, history_file: str = "logs/trade_history.json"):
        self.history_file = Path(history_file)
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        self.trades: List[Dict[str, Any]] = self._load_history()

    def _load_history(self) -> List[Dict[str, Any]]:
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except Exception as e:  # keep running even if file is corrupted
                logger.error("Error cargando historial: %s", e)
                return []
        return []

    def _save_history(self) -> None:
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.trades, f, indent=2)
        except Exception as e:
            logger.error("Error guardando historial: %s", e)

    def add_trade(self, ticket: Optional[int], symbol: str, signal: str, volume: float,
                  entry_price: float, sl: float, tp: float) -> None:
        trade = {
            "ticket": ticket,
            "symbol": symbol,
            "signal": signal,
            "type": "BUY" if signal == "BUY" else "SELL",
            "volume": volume,
            "entry_price": entry_price,
            "sl": sl,
            "tp": tp,
            "entry_time": datetime.utcnow().isoformat(),
            "exit_time": None,
            "exit_price": None,
            "profit_loss": None,
            "status": "OPEN"
        }
        self.trades.append(trade)
        self._save_history()

        # Persist also to DB if available
        if ingest_trade:
            try:
                ingest_trade({
                    "ticket": ticket,
                    "symbol": symbol,
                    "side": trade["type"],
                    "price": entry_price,
                    "volume": volume,
                    "sl": sl,
                    "tp": tp,
                    "meta": {"entry_time": trade["entry_time"]}
                })
            except Exception as e:
                logger.warning("No se pudo persistir en DB: %s", e)

        logger.info("📝 Trade abierto: %s | Ticket: %s | Precio: %.5f", signal, ticket, entry_price)

    def close_trade(self, ticket: int, exit_price: float, profit_loss: float) -> None:
        for trade in self.trades:
            if trade["ticket"] == ticket:
                trade["exit_time"] = datetime.utcnow().isoformat()
                trade["exit_price"] = exit_price
                trade["profit_loss"] = profit_loss
                trade["status"] = "CLOSED"
                self._save_history()

                if update_trade_exit:
                    try:
                        update_trade_exit(ticket, exit_price, profit_loss)
                    except Exception as e:
                        logger.warning("No se pudo actualizar la DB para ticket %s: %s", ticket, e)

                logger.info("🔒 Trade cerrado: Ticket %s | P/L: $%.2f", ticket, profit_loss)
                return
        logger.warning("⚠️ No se encontró trade con ticket %s", ticket)

    def get_summary(self) -> Dict[str, Any]:
        closed_trades = [t for t in self.trades if t["status"] == "CLOSED"]
        open_trades = [t for t in self.trades if t["status"] == "OPEN"]

        if not closed_trades:
            return {
                "total_trades": 0,
                "open_trades": len(open_trades),
                "won_trades": 0,
                "lost_trades": 0,
                "win_rate": 0,
                "total_profit": 0,
                "total_loss": 0,
                "net_profit": 0,
                "best_trade": None,
                "worst_trade": None
            }

        profits = [t["profit_loss"] for t in closed_trades if t["profit_loss"] is not None]
        won = sum(1 for p in profits if p > 0)
        lost = sum(1 for p in profits if p < 0)
        total_profit = sum(p for p in profits if p > 0)
        total_loss = sum(p for p in profits if p < 0)
        net_profit = sum(profits)

        return {
            "total_trades": len(closed_trades),
            "open_trades": len(open_trades),
            "won_trades": won,
            "lost_trades": lost,
            "win_rate": (won / len(closed_trades) * 100) if closed_trades else 0,
            "total_profit": round(total_profit, 2),
            "total_loss": round(total_loss, 2),
            "net_profit": round(net_profit, 2),
            "best_trade": max(profits) if profits else None,
            "worst_trade": min(profits) if profits else None
        }

    def print_summary(self) -> None:
        summary = self.get_summary()
        logger.info("=" * 60)
        logger.info("📊 RESUMEN DE OPERACIONES")
        logger.info("=" * 60)
        logger.info("Total de operaciones cerradas: %s", summary['total_trades'])
        logger.info("Operaciones abiertas: %s", summary['open_trades'])
        logger.info("✅ Operaciones ganadas: %s", summary['won_trades'])
        logger.info("❌ Operaciones perdidas: %s", summary['lost_trades'])
        logger.info("📈 Tasa de ganadoras: %.2f%%", summary['win_rate'])
        logger.info("💰 Ganancia total: $%.2f", summary['total_profit'])
        logger.info("💸 Pérdida total: $%.2f", summary['total_loss'])
        logger.info("🎯 PROFIT NETO: $%.2f", summary['net_profit'])
        if summary['best_trade']:
            logger.info("🚀 Mejor trade: $%.2f", summary['best_trade'])
        if summary['worst_trade']:
            logger.info("📉 Peor trade: $%.2f", summary['worst_trade'])
        logger.info("=" * 60)

    def get_recent_trades(self, limit: int = 10) -> List[Dict[str, Any]]:
        return self.trades[-limit:]

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class TradeHistory:
    """Módulo para registrar y analizar el historial de operaciones."""

    def __init__(self, history_file: str = "logs/trade_history.json"):
        self.history_file = Path(history_file)
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        self.trades: list[dict[str, Any]] = self._load_history()

    def _load_history(self) -> list[dict[str, Any]]:
        """Carga el historial desde archivo."""
        if self.history_file.exists():
            try:
                with open(self.history_file) as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error cargando historial: {e}")
                return []
        return []

    def _save_history(self) -> None:
        """Guarda el historial en archivo."""
        try:
            with open(self.history_file, "w") as f:
                json.dump(self.trades, f, indent=2)
        except Exception as e:
            logger.error(f"Error guardando historial: {e}")

    def add_trade(
        self,
        ticket: int,
        symbol: str,
        signal: str,
        volume: float,
        entry_price: float,
        sl: float,
        tp: float,
    ) -> None:
        """Registra una operación de entrada."""
        trade = {
            "ticket": ticket,
            "symbol": symbol,
            "signal": signal,
            "type": "BUY" if signal == "BUY" else "SELL",
            "volume": volume,
            "entry_price": entry_price,
            "sl": sl,
            "tp": tp,
            "entry_time": datetime.now().isoformat(),
            "exit_time": None,
            "exit_price": None,
            "profit_loss": None,
            "status": "OPEN",
        }
        self.trades.append(trade)
        self._save_history()
        logger.info(f"📝 Trade abierto: {signal} | Ticket: {ticket} | Precio: {entry_price}")

    def close_trade(self, ticket: int, exit_price: float, profit_loss: float) -> None:
        """Cierra una operación registrando salida y P/L."""
        for trade in self.trades:
            if trade["ticket"] == ticket:
                trade["exit_time"] = datetime.now().isoformat()
                trade["exit_price"] = exit_price
                trade["profit_loss"] = profit_loss
                trade["status"] = "CLOSED"
                self._save_history()
                logger.info(f"🔒 Trade cerrado: Ticket {ticket} | P/L: ${profit_loss:.2f}")
                return
        logger.warning(f"⚠️ No se encontró trade con ticket {ticket}")

    def get_summary(self) -> dict[str, Any]:
        """Retorna un resumen de estadísticas."""
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
                "worst_trade": None,
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
            "worst_trade": min(profits) if profits else None,
        }

    def print_summary(self) -> None:
        """Imprime un resumen formateado en los logs."""
        summary = self.get_summary()

        logger.info("=" * 60)
        logger.info("📊 RESUMEN DE OPERACIONES")
        logger.info("=" * 60)
        logger.info(f"Total de operaciones cerradas: {summary['total_trades']}")
        logger.info(f"Operaciones abiertas: {summary['open_trades']}")
        logger.info(f"✅ Operaciones ganadas: {summary['won_trades']}")
        logger.info(f"❌ Operaciones perdidas: {summary['lost_trades']}")
        logger.info(f"📈 Tasa de ganadoras: {summary['win_rate']:.2f}%")
        logger.info(f"💰 Ganancia total: ${summary['total_profit']:.2f}")
        logger.info(f"💸 Pérdida total: ${summary['total_loss']:.2f}")
        logger.info(f"🎯 PROFIT NETO: ${summary['net_profit']:.2f}")
        if summary["best_trade"]:
            logger.info(f"🚀 Mejor trade: ${summary['best_trade']:.2f}")
        if summary["worst_trade"]:
            logger.info(f"📉 Peor trade: ${summary['worst_trade']:.2f}")
        logger.info("=" * 60)

    def get_recent_trades(self, limit: int = 10) -> list[dict[str, Any]]:
        """Retorna los últimos N trades."""
        return self.trades[-limit:]

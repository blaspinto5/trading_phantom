import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)


class Trader:
    """Encapsula la lógica de ejecución de órdenes con validación de riesgo."""

    def __init__(self, mt5_connector: Any, risk_manager: Any) -> None:
        self.mt5 = mt5_connector
        self.risk = risk_manager

    # =========================
    # EJECUTAR OPERACIÓN
    # =========================
    def execute(self, signal: str, price: dict[str, Any]) -> Optional[dict[str, Any]]:
        """
        Ejecuta una orden si el risk_manager lo permite.

        Returns:
            Dict con detalles del trade o None si fue bloqueado.
        """

        check = self.risk.check(signal, price)

        if not check["allowed"]:
            logger.info("⛔ Trade bloqueado: %s", check.get("reason"))
            return None

        logger.info(
            "🚀 Ejecutando %s | Lote: %s | SL: %s | TP: %s",
            check["signal"],
            check["volume"],
            check["sl"],
            check["tp"],
        )

        result = self.mt5.send_order(
            symbol=price["symbol"],
            order_type=check["signal"],
            volume=check["volume"],
            sl=check["sl"],
            tp=check["tp"],
            deviation=self.risk.config["orders"]["deviation"],
        )

        if result is None:
            logger.error("❌ Error enviando orden")
            return None

        if getattr(result, "retcode", None) != 10009:  # TRADE_RETCODE_DONE
            logger.error("❌ Orden rechazada: %s", getattr(result, "retcode", None))
            return None

        ticket = getattr(result, "order", None)
        logger.info("✅ Orden ejecutada correctamente | Ticket: %s", ticket)

        # Retornar diccionario con detalles del trade
        return {
            "ticket": ticket,
            "signal": signal,
            "symbol": price["symbol"],
            "volume": check["volume"],
            "entry_price": price["bid"] if signal == "SELL" else price["ask"],
            "sl": check["sl"],
            "tp": check["tp"],
            "result": result,
        }

    # =========================
    # CERRAR TODAS LAS POSICIONES
    # =========================
    def close_all(self, symbol: str = None) -> None:
        positions = self.mt5.get_positions(symbol)

        if not positions:
            logger.info("ℹ️ No hay posiciones abiertas")
            return

        for pos in positions:
            result = self.mt5.close_position(pos)
            if result and getattr(result, "retcode", None) == 10009:
                logger.info("🔒 Posición %s cerrada", getattr(pos, "ticket", None))
            else:
                logger.error("❌ Error cerrando posición %s", getattr(pos, "ticket", None))

    # =========================
    # ACTUALIZAR PÉRDIDA DIARIA
    # =========================
    def update_daily_loss_from_history(self) -> None:
        """Actualiza la pérdida diaria leyendo el historial de órdenes cerradas"""
        deals = self.mt5.get_positions()
        if not deals:
            return

        profit = sum(pos.profit for pos in deals)
        self.risk.update_daily_loss(profit)

class Trader:
    def __init__(self, mt5_connector, risk_manager):
        self.mt5 = mt5_connector
        self.risk = risk_manager

    # =========================
    # EJECUTAR OPERACIÓN
    # =========================
    def execute(self, signal: str, price: dict):
        """
        Ejecuta una orden si el risk_manager lo permite
        """

        check = self.risk.check(signal, price)

        if not check["allowed"]:
            print(f"⛔ Trade bloqueado: {check.get('reason')}")
            return None

        print(
            f"🚀 Ejecutando {check['signal']} | "
            f"Lote: {check['volume']} | "
            f"SL: {check['sl']} | "
            f"TP: {check['tp']}"
        )

        result = self.mt5.send_order(
            symbol=price["symbol"],
            order_type=check["signal"],
            volume=check["volume"],
            sl=check["sl"],
            tp=check["tp"],
            deviation=self.risk.config["orders"]["deviation"]
        )

        if result is None:
            print("❌ Error enviando orden")
            return None

        if result.retcode != 10009:  # TRADE_RETCODE_DONE
            print(f"❌ Orden rechazada: {result.retcode}")
            return None

        print(f"✅ Orden ejecutada correctamente | Ticket: {result.order}")
        return result

    # =========================
    # CERRAR TODAS LAS POSICIONES
    # =========================
    def close_all(self, symbol: str = None):
        positions = self.mt5.get_positions(symbol)

        if not positions:
            print("ℹ️ No hay posiciones abiertas")
            return

        for pos in positions:
            result = self.mt5.close_position(pos)
            if result and result.retcode == 10009:
                print(f"🔒 Posición {pos.ticket} cerrada")
            else:
                print(f"❌ Error cerrando posición {pos.ticket}")

    # =========================
    # ACTUALIZAR PÉRDIDA DIARIA
    # =========================
    def update_daily_loss_from_history(self):
        """
        Actualiza la pérdida diaria leyendo el historial de órdenes cerradas
        """
        deals = self.mt5.get_positions()
        if not deals:
            return

        profit = sum(pos.profit for pos in deals)
        self.risk.update_daily_loss(profit)

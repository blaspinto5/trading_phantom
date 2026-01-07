import MetaTrader5 as mt5
from datetime import date
from typing import Any, Optional, Tuple


class RiskManager:
    """Comprueba si un trade puede ejecutarse y calcula lotajes y SL/TP seguros."""
    def __init__(self, config: dict, mt5_connector: Any) -> None:
        self.config: dict = config
        self.mt5: Any = mt5_connector
        self.daily_loss: float = 0.0
        self.last_reset: date = date.today()
    # =========================
    # RESET DIARIO
    # =========================
    def reset_daily_loss_if_new_day(self):
        today = date.today()
        if today != self.last_reset:
            self.daily_loss = 0.0
            self.last_reset = today

    # =========================
    # CÁLCULO DE LOTE (MT5 + BROKER SAFE)
    # =========================
    def calculate_lot(self, sl_pips: float) -> float:
        risk_cfg = self.config["risk"]

        # 1️⃣ Lote fijo
        if risk_cfg["fixed_lot"] is not None:
            return float(risk_cfg["fixed_lot"])

        # 2️⃣ Cuenta
        account = self.mt5.account_info()
        balance = account.balance
        risk_amount = balance * risk_cfg["risk_per_trade"]

        # 3️⃣ Símbolo
        symbol = self.mt5.resolve_symbol(self.config["symbol"])
        info = mt5.symbol_info(symbol)
        if info is None:
            return info.volume_min if info else 0.01

        contract_size = info.trade_contract_size
        point = info.point

        # 4️⃣ Valor pip por lote
        pip_value_per_lot = contract_size * point * 10
        if pip_value_per_lot <= 0:
            return info.volume_min

        # 5️⃣ Lote teórico
        lot = risk_amount / (sl_pips * pip_value_per_lot)

        # 6️⃣ Límites broker
        min_lot = info.volume_min
        max_lot = info.volume_max
        lot_step = info.volume_step

        USER_MAX_LOT = 0.3  # seguro para Admirals demo
        hard_cap = min(max_lot, USER_MAX_LOT)

        lot = min(lot, hard_cap)
        lot = max(min_lot, lot)
        lot = round(lot / lot_step) * lot_step

        return round(lot, 2)

    # =========================
    # SL / TP (BROKER SAFE)
    # =========================
    def calculate_sl_tp(self, signal: str, price: dict):
        sl_pips = self.config["orders"]["sl_pips"]
        tp_pips = self.config["orders"]["tp_pips"]

        info = mt5.symbol_info(price["symbol"])
        point = info.point

        # 🔒 STOP LEVEL del broker (en precio)
        stops_level_price = info.trade_stops_level * point

        sl_distance = max(sl_pips * point, stops_level_price)
        tp_distance = max(tp_pips * point, stops_level_price)

        if signal == "BUY":
            sl = price["bid"] - sl_distance
            tp = price["bid"] + tp_distance
        elif signal == "SELL":
            sl = price["ask"] + sl_distance
            tp = price["ask"] - tp_distance
        else:
            return None, None

        return round(sl, 5), round(tp, 5)

    # =========================
    # CHEQUEO PRINCIPAL
    # =========================
    def check(self, signal: str, price: dict) -> dict:
        self.reset_daily_loss_if_new_day()

        # 1️⃣ HOLD
        if signal == "HOLD":
            return {"allowed": False, "reason": "HOLD"}

        # 2️⃣ Máx posiciones
        positions = self.mt5.get_positions()
        if positions and len(positions) >= self.config["max_positions"]:
            return {"allowed": False, "reason": "MAX_POSITIONS"}

        # 3️⃣ Pérdida diaria
        if abs(self.daily_loss) >= self.config["risk"]["max_daily_loss"]:
            return {"allowed": False, "reason": "MAX_DAILY_LOSS"}

        # 4️⃣ SL / TP
        sl, tp = self.calculate_sl_tp(signal, price)
        if sl is None or tp is None:
            return {"allowed": False, "reason": "SL_TP_ERROR"}

        # 5️⃣ Lote
        lot = self.calculate_lot(self.config["orders"]["sl_pips"])
        if lot <= 0:
            return {"allowed": False, "reason": "LOT_ERROR"}

        return {
            "allowed": True,
            "signal": signal,
            "volume": lot,
            "sl": sl,
            "tp": tp
        }

    # =========================
    # ACTUALIZAR PÉRDIDA
    # =========================
    def update_daily_loss(self, profit: float):
        self.daily_loss += profit

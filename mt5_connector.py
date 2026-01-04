import MetaTrader5 as mt5
from datetime import datetime


class MT5Connector:
    def __init__(self):
        self.connected = False

    # -----------------------------
    # CONEXIÓN
    # -----------------------------
    def connect(self) -> bool:
        if not mt5.initialize():
            print("❌ MT5 initialize failed")
            print(mt5.last_error())
            return False

        self.connected = True
        print("✅ Conectado a MetaTrader 5")
        return True

    def shutdown(self):
        mt5.shutdown()
        self.connected = False
        print("🛑 Conexión MT5 cerrada")

    # -----------------------------
    # INFO DE CUENTA
    # -----------------------------
    def account_info(self):
        return mt5.account_info()

    # -----------------------------
    # RESOLUCIÓN DE SÍMBOLOS
    # -----------------------------
    def resolve_symbol(self, symbol: str):
        info = mt5.symbol_info(symbol)
        if info is not None:
            return symbol

        for s in mt5.symbols_get():
            if s.name.startswith(symbol):
                return s.name

        return None

    # -----------------------------
    # DATOS DE MERCADO
    # -----------------------------
    def get_price(self, symbol: str):
        resolved = self.resolve_symbol(symbol)
        if resolved is None:
            print(f"❌ Símbolo no encontrado: {symbol}")
            return None

        info = mt5.symbol_info(resolved)
        if not info.visible:
            mt5.symbol_select(resolved, True)

        tick = mt5.symbol_info_tick(resolved)
        if tick is None:
            return None

        return {
            "symbol": resolved,
            "bid": tick.bid,
            "ask": tick.ask,
            "time": datetime.fromtimestamp(tick.time)
        }

    # -----------------------------
    # POSICIONES
    # -----------------------------
    def get_positions(self, symbol: str = None):
        if symbol:
            resolved = self.resolve_symbol(symbol)
            return mt5.positions_get(symbol=resolved)
        return mt5.positions_get()

    # -----------------------------
    # EJECUCIÓN DE ÓRDENES (PENDING – CLAVE)
    # -----------------------------
    def send_order(
        self,
        symbol: str,
        order_type: str,
        volume: float,
        sl: float = None,
        tp: float = None,
        deviation: int = 50
    ):
        resolved = self.resolve_symbol(symbol)
        if resolved is None:
            print(f"❌ Símbolo no encontrado: {symbol}")
            return None

        info = mt5.symbol_info(resolved)
        if not info.visible:
            mt5.symbol_select(resolved, True)

        tick = mt5.symbol_info_tick(resolved)
        if tick is None:
            return None

        # 🔴 USAMOS PENDING ORDERS (NO MARKET)
        if order_type == "BUY":
            mt5_type = mt5.ORDER_TYPE_BUY_LIMIT
            price = tick.bid - 2 * info.point
        elif order_type == "SELL":
            mt5_type = mt5.ORDER_TYPE_SELL_LIMIT
            price = tick.ask + 2 * info.point
        else:
            raise ValueError("order_type debe ser BUY o SELL")

        request = {
            "action": mt5.TRADE_ACTION_PENDING,
            "symbol": resolved,
            "volume": float(volume),
            "type": mt5_type,
            "price": round(price, info.digits),
            "sl": sl,
            "tp": tp,
            "deviation": deviation,
            "magic": 10001,
            "comment": "Trading Phantom",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN,
        }

        return mt5.order_send(request)

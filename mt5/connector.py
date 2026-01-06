import MetaTrader5 as mt5
import logging
import pandas as pd
import time
from datetime import datetime
from typing import Optional, Any, List, Dict

logger = logging.getLogger(__name__)


class MT5Connector:
    """Wrapper for MetaTrader5 providing centralized connection and helpers.

    Methods return native MT5 structures or pandas DataFrames for rates.
    """
    def __init__(self) -> None:
        self.connected: bool = False

    # -----------------------------
    # CONEXIÓN
    # -----------------------------
    def connect(self, max_retries: int = 3, backoff_factor: float = 0.5) -> bool:
        """Attempt to initialize MT5 with retry/backoff.

        Args:
            max_retries: number of attempts before giving up.
            backoff_factor: base seconds to wait between retries (exponential backoff).
        """
        attempt = 0
        while attempt < max_retries:
            try:
                initialized = mt5.initialize()
            except Exception as e:
                logger.warning("MT5.initialize() raised exception on attempt %s: %s", attempt + 1, e)
                initialized = False

            if initialized:
                self.connected = True
                logger.info("✅ Conectado a MetaTrader 5")
                return True

            # not initialized -> log and wait
            last_err = None
            try:
                last_err = mt5.last_error()
            except Exception:
                last_err = None
            logger.warning("⚠️ MT5 initialize failed (attempt %s/%s): %s", attempt + 1, max_retries, last_err)
            attempt += 1
            time.sleep(backoff_factor * (2 ** (attempt - 1)))

        logger.error("❌ MT5 initialize failed after %s attempts", max_retries)
        return False

    def shutdown(self):
        try:
            mt5.shutdown()
        finally:
            self.connected = False
            logger.info("🛑 Conexión MT5 cerrada")

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
    def get_rates(self, symbol: str, timeframe, bars: int, max_retries: int = 3, backoff_factor: float = 0.5) -> Optional[list]:
        """Return raw rates array from MT5 for the given symbol/timeframe/bars with retry/backoff."""
        resolved = self.resolve_symbol(symbol)
        if resolved is None:
            logger.error("❌ Símbolo no encontrado: %s", symbol)
            return None

        attempt = 0
        while attempt < max_retries:
            try:
                rates = mt5.copy_rates_from_pos(resolved, timeframe, 0, bars)
            except Exception as e:
                logger.warning("⚠️ mt5.copy_rates_from_pos raised on attempt %s: %s", attempt + 1, e)
                rates = None

            if rates is not None and len(rates) > 0:
                return rates

            logger.warning("⚠️ No se pudieron obtener datos para %s (attempt %s/%s)", resolved, attempt + 1, max_retries)
            attempt += 1
            time.sleep(backoff_factor * (2 ** (attempt - 1)))

        logger.error("❌ No se pudieron obtener datos para %s tras %s intentos", resolved, max_retries)
        return None

    def get_rates_df(self, symbol: str, timeframe, bars: int) -> Optional[pd.DataFrame]:
        """Return a pandas DataFrame with properly parsed time column for the rates."""
        rates = self.get_rates(symbol, timeframe, bars)
        if rates is None:
            return None
        df = pd.DataFrame(rates)
        df["time"] = pd.to_datetime(df["time"], unit="s")
        return df

    # -----------------------------
    # DATOS DE MERCADO
    # -----------------------------
    def get_price(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Return latest tick information for symbol as dict or None."""
        resolved = self.resolve_symbol(symbol)
        if resolved is None:
            logger.error("❌ Símbolo no encontrado: %s", symbol)
            return None

        info = mt5.symbol_info(resolved)
        if info is None:
            logger.error("❌ No se pudo obtener symbol_info para %s", resolved)
            return None

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
    ) -> Any:
        """Send a pending order (BUY/SELL) and return MT5 response."""
        resolved = self.resolve_symbol(symbol)
        if resolved is None:
            logger.error("❌ Símbolo no encontrado: %s", symbol)
            return None

        info = mt5.symbol_info(resolved)
        if info is None:
            logger.error("❌ No se pudo obtener symbol_info para %s", resolved)
            return None

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

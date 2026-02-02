"""
Trading Phantom - Gestión de Riesgo Profesional
═══════════════════════════════════════════════════════════════════════════════
Módulo de gestión de riesgo con:
- Position sizing basado en % de riesgo por trade
- Stop Loss / Take Profit dinámicos
- Control de pérdida diaria máxima
- Validación de límites del broker

Principios aplicados:
- Regla del 1%: Nunca arriesgar más del 1% por operación
- Risk:Reward ratio mínimo 1:2
- Circuit breaker por pérdida diaria

Autor: Trading Phantom Team
Última actualización: 2026-02-02
═══════════════════════════════════════════════════════════════════════════════
"""

import logging
from dataclasses import dataclass
from datetime import date
from typing import Any, Optional

logger = logging.getLogger(__name__)


@dataclass
class RiskConfig:
    """Configuración de gestión de riesgo."""

    risk_per_trade: float = 0.01  # 1% por trade
    max_daily_loss: float = 0.03  # 3% pérdida diaria máxima
    max_drawdown: float = 0.10  # 10% drawdown máximo
    fixed_lot: Optional[float] = None  # None = cálculo automático
    max_lot: float = 0.5  # Lote máximo absoluto
    min_lot: float = 0.01  # Lote mínimo


@dataclass
class OrderConfig:
    """Configuración de órdenes."""

    sl_pips: float = 25  # Stop Loss en pips
    tp_pips: float = 50  # Take Profit en pips
    deviation: int = 20  # Slippage máximo
    trailing_stop: bool = True  # Activar trailing stop
    trailing_pips: float = 15  # Distancia del trailing
    breakeven_pips: float = 20  # Mover a breakeven después de X pips


class RiskManager:
    """
    Gestor de Riesgo Profesional.

    Valida y calcula parámetros de riesgo para cada operación,
    incluyendo position sizing, SL/TP y control de pérdidas.

    Attributes:
        config: Configuración general del bot
        mt5: Conector MT5
        daily_loss: Pérdida acumulada del día
    """

    def __init__(self, config: dict, mt5_connector: Any) -> None:
        """
        Inicializa el gestor de riesgo.

        Args:
            config: Configuración del bot (dict con secciones 'risk', 'orders', etc.)
            mt5_connector: Conector MT5 para info de cuenta y símbolos
        """
        self.config = config
        self.mt5 = mt5_connector

        # Tracking de pérdidas diarias
        self.daily_loss: float = 0.0
        self.daily_trades: int = 0
        self.last_reset: date = date.today()

        # Métricas de sesión
        self.session_pnl: float = 0.0
        self.winning_trades: int = 0
        self.losing_trades: int = 0

        logger.info("✅ RiskManager inicializado")

    def _reset_daily_stats_if_new_day(self) -> None:
        """Resetea estadísticas diarias si es un nuevo día."""
        today = date.today()
        if today != self.last_reset:
            logger.info(
                "📅 Nuevo día - Reset stats (PnL anterior: %.2f, Trades: %d)",
                self.daily_loss,
                self.daily_trades,
            )
            self.daily_loss = 0.0
            self.daily_trades = 0
            self.last_reset = today

    def _get_symbol_info(self, symbol: str) -> Optional[Any]:
        """
        Obtiene información del símbolo de forma segura.

        Returns:
            SymbolInfo o None si no está disponible
        """
        try:
            # Intentar importar MT5 dinámicamente para casos de testing
            try:
                import MetaTrader5 as mt5

                resolved = self.mt5.resolve_symbol(symbol)
                if resolved:
                    return mt5.symbol_info(resolved)
            except ImportError:
                pass

            # Fallback: usar método del connector si existe
            if hasattr(self.mt5, "symbol_info"):
                return self.mt5.symbol_info(symbol)

        except Exception as e:
            logger.warning("Error obteniendo symbol_info para %s: %s", symbol, e)

        return None

    def calculate_lot(self, sl_pips: float) -> float:
        """
        Calcula el tamaño de posición basado en riesgo.

        Fórmula: Lote = (Balance × Riesgo%) / (SL_pips × Valor_pip_por_lote)

        Args:
            sl_pips: Stop loss en pips

        Returns:
            Tamaño de lote calculado (dentro de límites del broker)
        """
        risk_cfg = self.config.get("risk", {})

        # 1️⃣ Lote fijo configurado
        fixed = risk_cfg.get("fixed_lot")
        if fixed is not None and fixed > 0:
            return float(fixed)

        # 2️⃣ Obtener balance de cuenta
        try:
            account = self.mt5.account_info()
            balance = getattr(account, "balance", 10000)  # Default para tests
        except Exception:
            balance = 10000

        # 3️⃣ Calcular monto en riesgo
        risk_pct = risk_cfg.get("risk_per_trade", 0.01)
        risk_amount = balance * risk_pct

        # 4️⃣ Obtener info del símbolo
        symbol = self.config.get("symbol", "EURUSD")
        info = self._get_symbol_info(symbol)

        if info is None:
            logger.warning("Sin info del símbolo, usando lote mínimo")
            return risk_cfg.get("min_lot", 0.01)

        # 5️⃣ Calcular valor pip
        contract_size = getattr(info, "trade_contract_size", 100000)
        point = getattr(info, "point", 0.00001)

        # Para pares XXX/USD: pip_value = contract_size * point * 10
        # Para otros pares se necesita conversión de divisa
        pip_value_per_lot = contract_size * point * 10

        if pip_value_per_lot <= 0:
            return getattr(info, "volume_min", 0.01)

        # 6️⃣ Calcular lote teórico
        lot = risk_amount / (sl_pips * pip_value_per_lot)

        # 7️⃣ Aplicar límites del broker
        min_lot = getattr(info, "volume_min", 0.01)
        max_lot = getattr(info, "volume_max", 100.0)
        lot_step = getattr(info, "volume_step", 0.01)

        # Límite de seguridad del usuario
        user_max = risk_cfg.get("max_lot", 0.5)
        hard_cap = min(max_lot, user_max)

        # Ajustar a límites
        lot = min(lot, hard_cap)
        lot = max(lot, min_lot)

        # Redondear al step del broker
        if lot_step > 0:
            lot = round(lot / lot_step) * lot_step

        return round(lot, 2)

    def calculate_sl_tp(
        self, signal: str, price: dict[str, Any]
    ) -> tuple[Optional[float], Optional[float]]:
        """
        Calcula Stop Loss y Take Profit respetando límites del broker.

        Considera:
        - trade_stops_level mínimo del broker
        - Distancia SL/TP configurada
        - Precisión de decimales del símbolo

        Args:
            signal: 'BUY' o 'SELL'
            price: Dict con 'symbol', 'bid', 'ask'

        Returns:
            Tuple (sl, tp) o (None, None) si hay error
        """
        if signal not in ("BUY", "SELL"):
            return None, None

        orders_cfg = self.config.get("orders", {})
        sl_pips = orders_cfg.get("sl_pips", 25)
        tp_pips = orders_cfg.get("tp_pips", 50)

        symbol = price.get("symbol", self.config.get("symbol"))
        info = self._get_symbol_info(symbol)

        if info is None:
            # Fallback sin info de símbolo
            point = 0.00001
            stops_level = 10
            digits = 5
        else:
            point = getattr(info, "point", 0.00001)
            stops_level = getattr(info, "trade_stops_level", 10)
            digits = getattr(info, "digits", 5)

        # Distancia mínima del broker (en precio)
        min_distance = stops_level * point

        # Calcular distancias (respetando mínimo del broker)
        sl_distance = max(sl_pips * point, min_distance)
        tp_distance = max(tp_pips * point, min_distance)

        # Calcular SL/TP según dirección
        bid = price.get("bid", 0)
        ask = price.get("ask", 0)

        if signal == "BUY":
            # BUY: SL debajo del precio, TP arriba
            sl = bid - sl_distance
            tp = bid + tp_distance
        else:  # SELL
            # SELL: SL arriba del precio, TP debajo
            sl = ask + sl_distance
            tp = ask - tp_distance

        return round(sl, digits), round(tp, digits)

    def check(self, signal: str, price: dict[str, Any]) -> dict[str, Any]:
        """
        Valida si una operación puede ejecutarse.

        Verificaciones:
        1. Señal válida (no HOLD)
        2. Máximo de posiciones abiertas
        3. Pérdida diaria no excedida
        4. SL/TP calculados correctamente
        5. Lote dentro de límites

        Args:
            signal: 'BUY', 'SELL' o 'HOLD'
            price: Dict con info de precio actual

        Returns:
            Dict con 'allowed': bool y detalles de la operación
        """
        self._reset_daily_stats_if_new_day()

        # 1️⃣ HOLD = no operar
        if signal == "HOLD":
            return {"allowed": False, "reason": "HOLD"}

        # 2️⃣ Verificar máximo de posiciones
        try:
            positions = self.mt5.get_positions()
            max_pos = self.config.get("max_positions", 3)
            if positions and len(positions) >= max_pos:
                logger.info("⛔ Máximo de posiciones alcanzado (%d/%d)", len(positions), max_pos)
                return {"allowed": False, "reason": "MAX_POSITIONS"}
        except Exception as e:
            logger.warning("Error verificando posiciones: %s", e)

        # 3️⃣ Verificar pérdida diaria
        risk_cfg = self.config.get("risk", {})
        max_daily = risk_cfg.get("max_daily_loss", 0.03)

        try:
            account = self.mt5.account_info()
            balance = getattr(account, "balance", 10000)
            max_loss_amount = balance * max_daily

            if abs(self.daily_loss) >= max_loss_amount:
                logger.warning(
                    "⛔ Circuit breaker activado: Pérdida diaria %.2f >= límite %.2f",
                    abs(self.daily_loss),
                    max_loss_amount,
                )
                return {"allowed": False, "reason": "MAX_DAILY_LOSS"}
        except Exception:
            pass

        # 4️⃣ Calcular SL/TP
        sl, tp = self.calculate_sl_tp(signal, price)
        if sl is None or tp is None:
            logger.error("❌ Error calculando SL/TP")
            return {"allowed": False, "reason": "SL_TP_ERROR"}

        # 5️⃣ Calcular lote
        orders_cfg = self.config.get("orders", {})
        sl_pips = orders_cfg.get("sl_pips", 25)
        lot = self.calculate_lot(sl_pips)

        if lot <= 0:
            logger.error("❌ Lote calculado inválido: %.2f", lot)
            return {"allowed": False, "reason": "LOT_ERROR"}

        # ✅ Operación permitida
        logger.info("✅ Trade validado: %s | Lote: %.2f | SL: %.5f | TP: %.5f", signal, lot, sl, tp)

        return {
            "allowed": True,
            "signal": signal,
            "volume": lot,
            "sl": sl,
            "tp": tp,
        }

    def update_daily_loss(self, profit: float) -> None:
        """
        Actualiza el tracking de pérdida diaria.

        Args:
            profit: P&L de la operación cerrada (positivo o negativo)
        """
        self.daily_loss += profit
        self.daily_trades += 1
        self.session_pnl += profit

        if profit > 0:
            self.winning_trades += 1
        elif profit < 0:
            self.losing_trades += 1

        logger.info(
            "📊 PnL actualizado: Trade=%.2f | Día=%.2f | Sesión=%.2f",
            profit,
            self.daily_loss,
            self.session_pnl,
        )

    def get_stats(self) -> dict[str, Any]:
        """
        Obtiene estadísticas de la sesión.

        Returns:
            Dict con métricas de riesgo y performance
        """
        total_trades = self.winning_trades + self.losing_trades
        win_rate = (self.winning_trades / total_trades * 100) if total_trades > 0 else 0

        return {
            "daily_loss": self.daily_loss,
            "daily_trades": self.daily_trades,
            "session_pnl": self.session_pnl,
            "winning_trades": self.winning_trades,
            "losing_trades": self.losing_trades,
            "win_rate": round(win_rate, 1),
            "last_reset": self.last_reset.isoformat(),
        }

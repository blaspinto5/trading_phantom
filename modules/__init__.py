"""
Trading Phantom - Core Modules
═══════════════════════════════════════════════════════════════════════════════

Core trading modules:
- Strategy: Signal generation with technical indicators
- RiskManager: Position sizing and risk control
- Trader: Order execution
- TradeHistory: Trade logging and analytics
"""

from modules.risk_manager import RiskManager
from modules.strategy import Strategy, StrategyConfig
from modules.trade_history import TradeHistory
from modules.trader import Trader

__all__ = [
    "Strategy",
    "StrategyConfig",
    "RiskManager",
    "Trader",
    "TradeHistory",
]

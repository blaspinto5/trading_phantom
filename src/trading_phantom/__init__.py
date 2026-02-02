"""
Trading Phantom - Professional Algorithmic Trading Framework
═══════════════════════════════════════════════════════════════════════════════

A modular framework for algorithmic trading on MetaTrader 5 with:
- Triple confirmation strategy (EMA + MACD + RSI)
- Professional risk management
- Machine learning integration
- Comprehensive backtesting

Usage:
    from trading_phantom.modules.strategy import Strategy
    from trading_phantom.modules.risk_manager import RiskManager
    from trading_phantom.modules.trader import Trader

Author: Trading Phantom Team
License: MIT
"""

__version__ = "1.0.0"
__author__ = "Trading Phantom Team"

from trading_phantom.modules.risk_manager import RiskManager

# Core exports
from trading_phantom.modules.strategy import Strategy, StrategyConfig

__all__ = [
    "Strategy",
    "StrategyConfig",
    "RiskManager",
    "__version__",
]

"""Compatibility shim: re-export StrategyModel from new ml package.

This shim keeps existing imports working while the ML package is reorganized.
"""

from trading_phantom.ml.models.strategy_model import StrategyModel

__all__ = ["StrategyModel"]

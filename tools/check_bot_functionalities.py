#!/usr/bin/env python3
"""Integration smoke tests for core bot components using a Dummy MT5 connector."""
import logging
import sys
from pathlib import Path
from types import SimpleNamespace

import pandas as pd

# Note: imports that depend on the package layout are performed inside
# `run_checks()` after ensuring `src/`/repo root is on `sys.path`.

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DummyMT5Connector:
    def __init__(self):
        self._balance = 10000.0

    def account_info(self):
        return SimpleNamespace(balance=self._balance)

    def resolve_symbol(self, symbol: str):
        return symbol

    def symbol_info(self, symbol: str):
        # minimal attributes used by RiskManager and MT5Connector
        return SimpleNamespace(
            trade_contract_size=100000,
            point=0.00001,
            volume_min=0.01,
            volume_max=100.0,
            volume_step=0.01,
            trade_stops_level=10,
            digits=5,
            visible=True,
        )

    def get_rates_df(self, symbol, timeframe, bars):
        # produce increasing closes to trigger BUY
        closes = [1.0 + i * 0.001 for i in range(10)]
        times = pd.date_range(end=pd.Timestamp.now(), periods=len(closes), freq="H")
        df = pd.DataFrame(
            {
                "time": times,
                "close": closes,
                "open": closes,
                "high": closes,
                "low": closes,
            }
        )
        return df

    def get_positions(self, symbol: str = None):
        return []

    def get_price(self, symbol: str):
        return {"symbol": symbol, "bid": 1.2345, "ask": 1.2347}

    def send_order(self, symbol, order_type, volume, sl=None, tp=None, deviation=50):
        # simulate successful order response
        return SimpleNamespace(retcode=10009, order=123456)

    def shutdown(self):
        logger.info("DummyMT5Connector.shutdown called")


def run_checks():
    logger.info("Loading config")
    # Ensure repo root is on sys.path so local packages import correctly
    ROOT = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(ROOT))

    # Import package modules after sys.path adjustment
    from config.config_loader import load_config
    from modules.risk_manager import RiskManager
    from modules.strategy import Strategy
    from modules.trade_history import TradeHistory
    from modules.trader import Trader

    config = load_config()

    mt5 = DummyMT5Connector()

    # Some modules import MetaTrader5 (mt5) at module scope and call mt5.symbol_info
    # directly. Patch the modules' mt5 reference to point to our dummy connector
    # so those functions use the fake symbols during smoke tests.
    import modules.risk_manager as _rm_mod

    _rm_mod.mt5 = mt5

    logger.info("Testing RiskManager")
    rm = RiskManager(config, mt5)
    lot = rm.calculate_lot(sl_pips=20)
    logger.info(f"Calculated lot: {lot}")

    price = {"symbol": config.get("symbol"), "bid": 1.2345, "ask": 1.2347}
    sl, tp = rm.calculate_sl_tp("BUY", price)
    logger.info(f"Calculated SL/TP: {sl}, {tp}")

    check = rm.check("BUY", price)
    logger.info(f"Risk check: {check}")

    logger.info("Testing Strategy")
    s = Strategy(config.get("symbol"), timeframe=None, mt5_connector=mt5)
    sig = s.generate_signal()
    logger.info(f"Strategy signal: {sig}")

    logger.info("Testing Trader")
    trader = Trader(mt5, rm)
    executed = trader.execute(sig if sig != "HOLD" else "BUY", price)
    logger.info(f"Trader execute returned: {executed}")

    logger.info("Testing TradeHistory")
    th = TradeHistory(history_file="logs/test_trade_history.json")
    th.add_trade(
        ticket=1,
        symbol=price["symbol"],
        signal="BUY",
        volume=lot,
        entry_price=price["bid"],
        sl=sl,
        tp=tp,
    )
    th.close_trade(ticket=1, exit_price=price["ask"], profit_loss=10.0)
    summary = th.get_summary()
    logger.info(f"TradeHistory summary: {summary}")

    logger.info("All checks completed successfully")


if __name__ == "__main__":
    run_checks()

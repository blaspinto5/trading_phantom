# backtest/run_backtest.py

import sys
from pathlib import Path
import logging
import MetaTrader5 as mt5

logger = logging.getLogger(__name__)

sys.path.append(str(Path(__file__).resolve().parent.parent))

from trading_phantom.mt5.connector import MT5Connector
# Luego ya puedes hacer:
from trading_phantom.modules.strategy import Strategy
from trading_phantom.backtest.simulation import BacktestSimulator
from trading_phantom.backtest.metrics import calculate_metrics


def run_backtest(symbol="EURUSD-T", timeframe=mt5.TIMEFRAME_H1, bars=1000):
    logger.info("📊 Ejecutando Backtest")

    connector = MT5Connector()
    if not connector.connect():
        logger.error("❌ Error al iniciar MT5")
        return

    rates = connector.get_rates(symbol, timeframe, bars)
    if rates is None or len(rates) == 0:
        logger.error("❌ No se pudo obtener datos")
        connector.shutdown()
        return

    strategy = Strategy(symbol, timeframe, None)
    simulator = BacktestSimulator(rates, strategy, sl_pips=20, tp_pips=40)

    trades = simulator.run()
    metrics = calculate_metrics(trades)

    logger.info("\n📈 Resultados del Backtest:")
    for key, value in metrics.items():
        logger.info("%s: %s", key, value)

    connector.shutdown()

if __name__ == "__main__":
    run_backtest()

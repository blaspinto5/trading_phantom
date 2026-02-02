import logging

import MetaTrader5 as mt5

from trading_phantom.backtest.metrics import calculate_metrics
from trading_phantom.backtest.simulation import BacktestSimulator
from trading_phantom.backtest.visual_backtest import run_visual_backtest
from trading_phantom.mt5.connector import MT5Connector

logger = logging.getLogger(__name__)


def run_backtest_and_visual(
    symbol: str = "EURUSD-T",
    timeframe=mt5.TIMEFRAME_H1,
    bars: int = 1000,
    sma_period: int = 50,
    rsi_period: int = 14,
    run_plot: bool = True,
):
    connector = MT5Connector()
    if not connector.connect():
        logger.error("No se pudo conectar a MT5 para backtest")
        return None

    rates = connector.get_rates(symbol, timeframe, bars)
    if rates is None or len(rates) == 0:
        logger.error("No se pudieron obtener rates para %s", symbol)
        connector.shutdown()
        return None

    from trading_phantom.modules.strategy import Strategy

    strategy = Strategy(symbol, timeframe, None, sma_period=sma_period, rsi_period=rsi_period)
    simulator = BacktestSimulator(rates, strategy, sl_pips=20, tp_pips=40)
    trades = simulator.run()
    metrics = calculate_metrics(trades)

    logger.info("Backtest numérico completo. Trades: %s", len(trades))

    df = connector.get_rates_df(symbol, timeframe, bars)
    if df is None:
        logger.error("No se pudo construir DataFrame para visual backtest")
        connector.shutdown()
        return {"metrics": metrics}

    visual_results = run_visual_backtest(
        df, sma_period=sma_period, rsi_period=rsi_period, plot=run_plot
    )

    connector.shutdown()

    return {"metrics": metrics, "visual_results": visual_results}


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    out = run_backtest_and_visual(run_plot=True)
    logger.info("Backtest output: %s", out)

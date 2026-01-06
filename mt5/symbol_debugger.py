import MetaTrader5 as mt5
import logging

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    mt5.initialize()

    symbol = "EURUSD"
    symbols = mt5.symbols_get()

    for s in symbols:
        if s.name.startswith(symbol):
            info = mt5.symbol_info(s.name)
            logger.info("================================")
            logger.info("SYMBOL: %s", s.name)
            logger.info("trade_mode: %s", info.trade_mode)
            logger.info("filling_mode: %s", info.filling_mode)
            logger.info("volume_min: %s", info.volume_min)
            logger.info("volume_max: %s", info.volume_max)
            logger.info("volume_step: %s", info.volume_step)
            logger.info("trade_allowed: %s", info.trade_allowed)
            logger.info("================================")

    mt5.shutdown()

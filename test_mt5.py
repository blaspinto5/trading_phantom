import logging
from trading_phantom.mt5.connector import MT5Connector

logger = logging.getLogger(__name__)


def main():
    mt5 = MT5Connector()
    mt5.connect()

    logger.info("%s", mt5.account_info())
    logger.info("%s", mt5.get_price("EURUSD"))

    mt5.shutdown()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()

# modules/data_loader.py

import logging

import pandas as pd

logger = logging.getLogger(__name__)

def load_mt5_data(symbol: str, timeframe, bars: int, mt5_connector=None):
    if mt5_connector:
        df = mt5_connector.get_rates_df(symbol, timeframe, bars)
        if df is None or len(df) == 0:
            logger.error("❌ No se pudieron obtener datos (connector)")
            return None
    else:
        # Prefer using the connector even in fallback paths to avoid duplicating MT5 initialization
        from trading_phantom.mt5.connector import MT5Connector
        connector = MT5Connector()
        if not connector.connect():
            logger.error("❌ No se pudo inicializar MT5 (connector)")
            return None
        df = connector.get_rates_df(symbol, timeframe, bars)
        connector.shutdown()

        if df is None or len(df) == 0:
            logger.error("❌ No se pudieron obtener datos")
            return None

    df["Date"] = pd.to_datetime(df["time"])
    df.rename(columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "tick_volume": "Volume"
    }, inplace=True)
    df = df[["Date", "Open", "High", "Low", "Close", "Volume"]]
    df.set_index("Date", inplace=True)

    return df

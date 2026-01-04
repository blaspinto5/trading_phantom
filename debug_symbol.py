import MetaTrader5 as mt5

mt5.initialize()

symbol = "EURUSD"
symbols = mt5.symbols_get()

for s in symbols:
    if s.name.startswith(symbol):
        info = mt5.symbol_info(s.name)
        print("================================")
        print("SYMBOL:", s.name)
        print("trade_mode:", info.trade_mode)
        print("filling_mode:", info.filling_mode)
        print("volume_min:", info.volume_min)
        print("volume_max:", info.volume_max)
        print("volume_step:", info.volume_step)
        print("trade_allowed:", info.trade_allowed)
        print("================================")

mt5.shutdown()

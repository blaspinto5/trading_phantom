from mt5_connector import MT5Connector

mt5 = MT5Connector()
mt5.connect()

print(mt5.account_info())
print(mt5.get_price("EURUSD"))

mt5.shutdown()

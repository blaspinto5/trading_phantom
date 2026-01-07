
from trading_phantom.mt5.connector import MT5Connector


class DummyMT5:
    def __init__(self):
        self._initialize_calls = 0
        self._copy_calls = 0

    def initialize(self):
        self._initialize_calls += 1
        # succeed on 3rd call
        return self._initialize_calls >= 3

    def last_error(self):
        return "simulated error"

    def copy_rates_from_pos(self, symbol, timeframe, pos, bars):
        self._copy_calls += 1
        # succeed on 2nd call
        if self._copy_calls >= 2:
            return [{"time": 1600000000, "open": 1, "high": 1, "low": 1, "close": 1}]
        return None


def test_connect_retries(monkeypatch):
    dummy = DummyMT5()
    # monkeypatch the mt5 module used inside connector
    import trading_phantom.mt5.connector as conn_mod

    monkeypatch.setattr(conn_mod, "mt5", dummy)

    m = MT5Connector()
    # Set backoff to 0 to avoid sleeping
    ok = m.connect(max_retries=5, backoff_factor=0)
    assert ok is True


def test_get_rates_retries(monkeypatch):
    dummy = DummyMT5()
    import trading_phantom.mt5.connector as conn_mod

    monkeypatch.setattr(conn_mod, "mt5", dummy)

    m = MT5Connector()
    # resolve_symbol expects actual behavior, so patch it to return the symbol
    monkeypatch.setattr(m, "resolve_symbol", lambda s: s)

    rates = m.get_rates("EURUSD", timeframe=1, bars=1, max_retries=3, backoff_factor=0)
    assert rates is not None
    assert isinstance(rates, list)
    assert len(rates) == 1

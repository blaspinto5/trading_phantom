from typing import Any, Dict

from .db import Trade, BacktestRun, get_session


def ingest_trade(trade: Dict[str, Any]) -> int:
    """Store a single executed trade into the database.

    Expected keys: symbol, side, price, volume, pnl (optional), meta (optional)
    Returns inserted row id.
    """
    session = get_session()
    obj = Trade(
        symbol=str(trade.get('symbol')),
        side=str(trade.get('side')),
        price=float(trade.get('price', 0.0)),
        volume=float(trade.get('volume', 0.0)),
        pnl=(None if trade.get('pnl') is None else float(trade.get('pnl'))),
        meta=(trade.get('meta') or None),
    )
    session.add(obj)
    session.commit()
    rid = obj.id
    session.close()
    return rid


def ingest_backtest(payload: Dict[str, Any]) -> int:
    """Store backtest run summary and raw results.

    Expected keys: symbol, bars, sma_period, rsi_period, metrics, details
    Returns inserted row id.
    """
    session = get_session()
    obj = BacktestRun(
        symbol=str(payload.get('symbol')),
        bars=int(payload.get('bars', 0)),
        sma_period=int(payload.get('sma_period', 0)),
        rsi_period=int(payload.get('rsi_period', 0)),
        metrics=(payload.get('metrics') or {}),
        details=(payload.get('details') or {}),
    )
    session.add(obj)
    session.commit()
    rid = obj.id
    session.close()
    return rid

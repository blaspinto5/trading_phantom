from typing import Any, Dict

from .db import BacktestRun, Trade, get_session


def ingest_trade(trade: Dict[str, Any]) -> int:
    """Store a single executed trade into the database.

    Expected keys: ticket, symbol, side, price, volume, sl, tp, pnl (optional), meta (optional)
    Returns inserted row id.
    """
    session = get_session()
    obj = Trade(
        ticket=(trade.get("ticket")),
        symbol=str(trade.get("symbol")),
        side=str(trade.get("side")),
        price=float(trade.get("price", 0.0)),
        volume=float(trade.get("volume", 0.0)),
        sl=(None if trade.get("sl") is None else float(trade.get("sl"))),
        tp=(None if trade.get("tp") is None else float(trade.get("tp"))),
        pnl=(None if trade.get("pnl") is None else float(trade.get("pnl"))),
        meta=(trade.get("meta") or None),
    )
    session.add(obj)
    session.commit()
    rid = obj.id
    session.close()
    return rid


def update_trade_exit(ticket: int, exit_price: float, pnl: float) -> None:
    """Update an existing trade with exit info and pnl."""
    from datetime import datetime

    session = get_session()
    try:
        obj = (
            session.query(Trade)
            .filter(Trade.ticket == ticket)
            .order_by(Trade.id.desc())
            .first()
        )
        if obj:
            obj.exit_price = float(exit_price)
            obj.exit_time = datetime.utcnow()
            obj.pnl = float(pnl)
            session.commit()
    finally:
        session.close()


def ingest_backtest(payload: Dict[str, Any]) -> int:
    """Store backtest run summary and raw results.

    Expected keys: symbol, bars, sma_period, rsi_period, metrics, details
    Returns inserted row id.
    """
    session = get_session()
    obj = BacktestRun(
        symbol=str(payload.get("symbol")),
        bars=int(payload.get("bars", 0)),
        sma_period=int(payload.get("sma_period", 0)),
        rsi_period=int(payload.get("rsi_period", 0)),
        metrics=(payload.get("metrics") or {}),
        details=(payload.get("details") or {}),
    )
    session.add(obj)
    session.commit()
    rid = obj.id
    session.close()
    return rid

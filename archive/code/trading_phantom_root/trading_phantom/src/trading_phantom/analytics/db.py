import os
from datetime import datetime

from sqlalchemy import (JSON, Column, DateTime, Float, Integer, String,
                        create_engine)
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class Trade(Base):
    __tablename__ = "trades"
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    ticket = Column(Integer, index=True, nullable=True)
    symbol = Column(String(50))
    side = Column(String(10))  # BUY/SELL
    price = Column(Float)
    volume = Column(Float)
    sl = Column(Float, nullable=True)
    tp = Column(Float, nullable=True)
    exit_price = Column(Float, nullable=True)
    exit_time = Column(DateTime, nullable=True)
    pnl = Column(Float, nullable=True)
    meta = Column(JSON, nullable=True)


class BacktestRun(Base):
    __tablename__ = "backtest_runs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    symbol = Column(String(50))
    bars = Column(Integer)
    sma_period = Column(Integer)
    rsi_period = Column(Integer)
    metrics = Column(JSON)
    details = Column(JSON)  # raw serialized results if needed


_engine = None
SessionLocal = None


def get_database_url() -> str:
    # Prefer env var DATABASE_URL; fallback to local SQLite
    url = os.getenv("DATABASE_URL")
    if url:
        return url
    data_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "data")
    )
    os.makedirs(data_dir, exist_ok=True)
    return f"sqlite:///{os.path.join(data_dir, 'trading_phantom.db')}"


def init_db() -> None:
    global _engine, SessionLocal
    if _engine is None:
        _engine = create_engine(get_database_url())
        SessionLocal = sessionmaker(bind=_engine)
        Base.metadata.create_all(_engine)


def get_session():
    if _engine is None:
        init_db()
    return SessionLocal()

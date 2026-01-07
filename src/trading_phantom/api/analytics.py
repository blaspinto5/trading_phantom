import logging
from flask import Blueprint, jsonify, request
from trading_phantom.analytics.collector import ingest_trade
from trading_phantom.analytics.ml_pipeline import StrategyModel
from trading_phantom.analytics.db import get_session, Trade, BacktestRun

bp = Blueprint('analytics', __name__)
logger = logging.getLogger(__name__)
_ml_model = StrategyModel()


@bp.route('/ingest/trade', methods=['POST'])
def api_ingest_trade():
    data = request.get_json() or {}
    try:
        rid = ingest_trade(data)
        return jsonify({'status': 'ok', 'id': rid})
    except Exception as e:
        logger.exception('Failed to ingest trade')
        return jsonify({'status': 'error', 'error': str(e)}), 500


@bp.route('/ml/train', methods=['POST'])
def api_ml_train():
    try:
        res = _ml_model.train()
        return jsonify(res)
    except Exception as e:
        logger.exception('ML training failed')
        return jsonify({'status': 'error', 'error': str(e)}), 500


@bp.route('/ml/predict', methods=['POST'])
def api_ml_predict():
    data = request.get_json() or {}
    try:
        res = _ml_model.predict(data)
        return jsonify(res)
    except Exception as e:
        logger.exception('ML predict failed')
        return jsonify({'status': 'error', 'error': str(e)}), 500


@bp.route('/analytics/export/trades', methods=['GET'])
def export_trades():
    fmt = (request.args.get('format') or 'json').lower()
    session = get_session()
    rows = session.query(Trade).all()
    session.close()
    data = [
        {
            'id': r.id,
            'timestamp': r.timestamp.isoformat() if r.timestamp else None,
            'symbol': r.symbol,
            'side': r.side,
            'price': r.price,
            'volume': r.volume,
            'pnl': r.pnl,
            'meta': r.meta,
        }
        for r in rows
    ]
    return jsonify({'format': fmt, 'data': data})


@bp.route('/analytics/export/backtests', methods=['GET'])
def export_backtests():
    fmt = (request.args.get('format') or 'json').lower()
    session = get_session()
    rows = session.query(BacktestRun).all()
    session.close()
    data = [
        {
            'id': r.id,
            'created_at': r.created_at.isoformat() if r.created_at else None,
            'symbol': r.symbol,
            'bars': r.bars,
            'sma_period': r.sma_period,
            'rsi_period': r.rsi_period,
            'metrics': r.metrics,
            'details': r.details,
        }
        for r in rows
    ]
    return jsonify({'format': fmt, 'data': data})

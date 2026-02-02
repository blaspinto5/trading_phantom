import io
import logging

import pandas as pd
from flask import Blueprint, Response, jsonify, request

from trading_phantom.analytics.collector import ingest_trade
from trading_phantom.analytics.db import BacktestRun, Trade, get_session
from trading_phantom.analytics.ml_pipeline import StrategyModel
from trading_phantom.analytics.model_store import load_latest_model

bp = Blueprint("analytics", __name__)
logger = logging.getLogger(__name__)
_ml_model = StrategyModel()


@bp.route("/ingest/trade", methods=["POST"])
def api_ingest_trade():
    data = request.get_json() or {}
    try:
        rid = ingest_trade(data)
        return jsonify({"status": "ok", "id": rid})
    except Exception as e:
        logger.exception("Failed to ingest trade")
        return jsonify({"status": "error", "error": str(e)}), 500


@bp.route("/ml/train", methods=["POST"])
def api_ml_train():
    try:
        res = _ml_model.train()
        return jsonify(res)
    except Exception as e:
        logger.exception("ML training failed")
        return jsonify({"status": "error", "error": str(e)}), 500


@bp.route("/ml/predict", methods=["POST"])
def api_ml_predict():
    data = request.get_json() or {}
    try:
        res = _ml_model.predict(data)
        return jsonify(res)
    except Exception as e:
        logger.exception("ML predict failed")
        return jsonify({"status": "error", "error": str(e)}), 500


@bp.route("/ml/models", methods=["GET"])
def api_ml_models_list():
    """List available saved models from src/data/models index."""
    try:
        import json
        from pathlib import Path

        idx = Path("src/data/models/models_index.json")
        if not idx.exists():
            return jsonify({"models": []})
        with open(idx, encoding="utf-8") as f:
            data = json.load(f)
        return jsonify({"models": data})
    except Exception as e:
        logger.exception("Failed listing models")
        return jsonify({"status": "error", "error": str(e)}), 500


@bp.route("/ml/models/load", methods=["POST"])
def api_ml_models_load():
    """Load a saved model into the in-memory StrategyModel instance.

    Body JSON: { "filename": "optional_filename.pkl" }
    If no filename provided, loads the latest available model.
    """
    payload = request.get_json() or {}
    filename = payload.get("filename")
    try:
        # If filename provided, attempt to open that file; otherwise use latest
        if filename:
            from pathlib import Path

            p = Path("src/data/models") / filename
            if not p.exists():
                return jsonify({"status": "error", "error": "file_not_found"}), 404
            # Try joblib first (new format), fall back to pickle for older files
            try:
                import joblib

                model_data = joblib.load(p)
            except Exception:
                import pickle

                with open(p, "rb") as f:
                    model_data = pickle.load(f)
        else:
            model_data = load_latest_model()

        if not model_data:
            return jsonify({"status": "error", "error": "no_model_available"}), 404

        # Inject model into in-memory StrategyModel
        try:
            _ml_model.model = model_data.get("model", _ml_model.model)
            _ml_model.is_trained = True
        except Exception:
            # best-effort assignment
            logger.exception("Failed attaching model to StrategyModel")

        return jsonify(
            {"status": "ok", "loaded": True, "meta": {"model_type": model_data.get("model_type")}}
        )
    except Exception as e:
        logger.exception("Failed loading model")
        return jsonify({"status": "error", "error": str(e)}), 500


def _export_response(data: list, fmt: str, filename: str) -> Response:
    if fmt == "json":
        return jsonify({"format": fmt, "data": data})
    df = pd.DataFrame(data)
    if fmt == "csv":
        csv_buf = io.StringIO()
        df.to_csv(csv_buf, index=False)
        return Response(
            csv_buf.getvalue(),
            mimetype="text/csv",
            headers={"Content-Disposition": f'attachment; filename="{filename}.csv"'},
        )
    if fmt == "parquet":
        try:
            import pyarrow  # noqa: F401
            import pyarrow.parquet as pq  # noqa: F401
        except Exception:
            return (
                jsonify(
                    {"error": "pyarrow not installed. Install pyarrow to enable Parquet export."}
                ),
                400,
            )
        buf = io.BytesIO()
        df.to_parquet(buf, index=False)
        return Response(
            buf.getvalue(),
            mimetype="application/octet-stream",
            headers={"Content-Disposition": f'attachment; filename="{filename}.parquet"'},
        )
    return jsonify({"error": f"Unsupported format: {fmt}"}), 400


@bp.route("/analytics/export/trades", methods=["GET"])
def export_trades():
    fmt = (request.args.get("format") or "json").lower()
    session = get_session()
    rows = session.query(Trade).all()
    session.close()
    data = [
        {
            "id": r.id,
            "timestamp": r.timestamp.isoformat() if r.timestamp else None,
            "symbol": r.symbol,
            "side": r.side,
            "price": r.price,
            "volume": r.volume,
            "pnl": r.pnl,
            "meta": r.meta,
        }
        for r in rows
    ]
    return _export_response(data, fmt, "trades")


@bp.route("/analytics/export/backtests", methods=["GET"])
def export_backtests():
    fmt = (request.args.get("format") or "json").lower()
    session = get_session()
    rows = session.query(BacktestRun).all()
    session.close()
    data = [
        {
            "id": r.id,
            "created_at": r.created_at.isoformat() if r.created_at else None,
            "symbol": r.symbol,
            "bars": r.bars,
            "sma_period": r.sma_period,
            "rsi_period": r.rsi_period,
            "metrics": r.metrics,
            "details": r.details,
        }
        for r in rows
    ]
    return _export_response(data, fmt, "backtests")

import logging
import threading
import uuid

from flask import Blueprint, jsonify, request

from trading_phantom.analytics.collector import ingest_backtest
from trading_phantom.backtest.run_and_visual import run_backtest_and_visual

bp = Blueprint("backtest", __name__)
logger = logging.getLogger(__name__)

_backtest_jobs = {}


def _make_jsonable(o):
    try:
        import numpy as _np
        import pandas as _pd
    except Exception:
        _np = None
        _pd = None
    if hasattr(o, "_asdict") and callable(o._asdict):
        try:
            return _make_jsonable(o._asdict())
        except Exception:
            return str(o)
    if _pd is not None and isinstance(o, _pd.Series):
        return _make_jsonable(o.to_dict())
    if _pd is not None and isinstance(o, _pd.DataFrame):
        return _make_jsonable(o.to_dict(orient="list"))
    if _np is not None and isinstance(o, _np.generic):
        return o.item()
    if isinstance(o, dict):
        return {str(k): _make_jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple, set)):
        return [_make_jsonable(v) for v in o]
    if isinstance(o, (str, int, float, bool)) or o is None:
        return o
    try:
        return str(o)
    except Exception:
        return None


@bp.route("/backtest", methods=["POST"])
def start_backtest():
    data = request.get_json() or {}
    symbol = data.get("symbol")
    timeframe = data.get("timeframe")
    bars = data.get("bars", 1000)
    sma = data.get("sma_period", 50)
    rsi = data.get("rsi_period", 14)

    job_id = str(uuid.uuid4())
    _backtest_jobs[job_id] = {"status": "running", "result": None}

    def worker():
        try:
            res = run_backtest_and_visual(
                symbol or "EURUSD-T",
                bars=bars,
                sma_period=sma,
                rsi_period=rsi,
                run_plot=False,
            )
            safe = _make_jsonable(res)
            _backtest_jobs[job_id]["status"] = "done"
            _backtest_jobs[job_id]["result"] = safe
        except Exception as e:
            logger.exception("Error running backtest")
            _backtest_jobs[job_id]["status"] = "error"
            _backtest_jobs[job_id]["result"] = {"error": str(e)}

    t = threading.Thread(target=worker, daemon=True)
    t.start()

    return jsonify({"job_id": job_id})


@bp.route("/backtest/<job_id>", methods=["GET"])
def backtest_status(job_id):
    job = _backtest_jobs.get(job_id)
    if not job:
        return jsonify({"error": "job not found"}), 404
    if job.get("status") == "done" and job.get("result"):
        try:
            res = job["result"]
            payload = {
                "symbol": res.get("symbol", "EURUSD-T"),
                "bars": res.get("bars", 0),
                "sma_period": res.get("sma_period", 0),
                "rsi_period": res.get("rsi_period", 0),
                "metrics": res.get("metrics", {}),
                "details": res,
            }
            ingest_backtest(payload)
        except Exception:
            logger.exception("Failed to ingest backtest result")
    return jsonify(job)

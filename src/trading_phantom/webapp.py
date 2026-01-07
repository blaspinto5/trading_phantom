# trading_phantom/webapp.py (moved to src package)

import logging
import os

from flask import Flask, render_template

from trading_phantom.analytics.db import init_db
from trading_phantom.api import register_blueprints

logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'), static_folder=os.path.join(os.path.dirname(__file__), 'static'))

try:
    init_db()
except Exception:
    logger.exception('Database initialization failed; falling back to file-based only')

# Register modular API blueprints (controlled by env flags)
register_blueprints(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/ingest/trade', methods=['POST'])
def api_ingest_trade():
    """Ingest executed trade into database."""
    data = request.get_json() or {}
    try:
        rid = ingest_trade(data)
        return jsonify({'status': 'ok', 'id': rid})
    except Exception as e:
        logger.exception('Failed to ingest trade')
        return jsonify({'status': 'error', 'error': str(e)}), 500


@app.route('/api/ml/train', methods=['POST'])
def api_ml_train():
    """Train simple ML model based on stored trades."""
    try:
        res = _ml_model.train()
        return jsonify(res)
    except Exception as e:
        logger.exception('ML training failed')
        return jsonify({'status': 'error', 'error': str(e)}), 500


@app.route('/api/ml/predict', methods=['POST'])
def api_ml_predict():
    """Predict profitability on a sample trade-like feature set."""
    data = request.get_json() or {}
    try:
        res = _ml_model.predict(data)
        return jsonify(res)
    except Exception as e:
        logger.exception('ML predict failed')
        return jsonify({'status': 'error', 'error': str(e)}), 500


def run_app(host='127.0.0.1', port=5000, debug=False):
    # Run the Flask app (used by launcher and for local testing)
    app.run(host=host, port=port, debug=debug, threaded=True)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    run_app()

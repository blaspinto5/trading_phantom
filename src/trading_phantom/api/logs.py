import os
import logging
from flask import Blueprint, jsonify, request

bp = Blueprint('logs', __name__)
logger = logging.getLogger(__name__)


@bp.route('/logs', methods=['GET'])
def get_logs():
    lines = int(request.args.get('lines', 200))
    want_bot = request.args.get('bot', '').lower() in ('1', 'true', 'yes')
    file_name = request.args.get('file')
    logs_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')

    if not os.path.isdir(logs_dir):
        return jsonify({'logs': ''})

    log_file = None
    if want_bot:
        candidate = os.path.join(logs_dir, 'bot.log')
        if os.path.exists(candidate):
            log_file = candidate
    if not log_file and file_name:
        safe = os.path.basename(file_name)
        candidate = os.path.join(logs_dir, safe)
        if os.path.exists(candidate):
            log_file = candidate
    if not log_file:
        logs = [os.path.join(logs_dir, f) for f in os.listdir(logs_dir) if f.endswith('.log')]
        if not logs:
            return jsonify({'logs': ''})
        logs.sort(key=lambda p: os.path.getmtime(p), reverse=True)
        log_file = logs[0]

    try:
        with open(log_file, 'r', encoding='utf-8') as fh:
            data = fh.readlines()
        return jsonify({'logs': ''.join(data[-lines:])})
    except Exception:
        logger.exception('Failed to read log file')
        return jsonify({'logs': ''})

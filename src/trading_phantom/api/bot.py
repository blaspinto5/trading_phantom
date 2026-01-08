import os
import sys
import subprocess
import threading
import logging
from flask import Blueprint, jsonify, request

bp = Blueprint('bot', __name__)
logger = logging.getLogger(__name__)

_bot_process = None
_bot_lock = threading.Lock()


@bp.route('/bot/start', methods=['POST'])
def bot_start():
    global _bot_process
    with _bot_lock:
        if _bot_process is not None and _bot_process.poll() is None:
            return jsonify({'status': 'already_running', 'pid': _bot_process.pid})

        body = request.get_json() or {}
        args = [sys.executable, '-m', 'trading_phantom.main']
        if body.get('debug'):
            args.append('--debug')
        if body.get('iterations'):
            args += ['--iterations', str(body['iterations'])]

        # Write logs under src/logs to match test expectations
        src_dir_for_logs = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        logs_dir = os.path.join(src_dir_for_logs, 'logs')
        try:
            os.makedirs(logs_dir, exist_ok=True)
        except Exception:
            logger.exception('Failed to create logs directory')

        bot_log = os.path.join(logs_dir, 'bot.log')

        try:
            env = os.environ.copy()
            src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
            existing = env.get('PYTHONPATH', '')
            env['PYTHONPATH'] = src_dir if not existing else (src_dir + os.pathsep + existing)
            try:
                proc = subprocess.Popen(
                    args,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    env=env,
                )
            except TypeError:
                # Some test doubles may not accept 'env' kwarg; fall back without it
                proc = subprocess.Popen(
                    args,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                )
        except Exception as e:
            logger.exception('Failed to start bot subprocess')
            return jsonify({'status': 'error', 'error': str(e)}), 500

        def _forward_output_to_log(pipe, logfile_path):
            try:
                with open(logfile_path, 'a', encoding='utf-8') as fh:
                    for line in pipe:
                        fh.write(line)
                        fh.flush()
            except Exception:
                logger.exception('Error while forwarding bot output to log')

        t = threading.Thread(target=_forward_output_to_log, args=(proc.stdout, bot_log), daemon=True)
        t.start()

        _bot_process = proc
        logger.info('Started bot subprocess pid=%s; logging to %s', _bot_process.pid, bot_log)
        return jsonify({'status': 'started', 'pid': _bot_process.pid})


@bp.route('/bot/stop', methods=['POST'])
def bot_stop():
    global _bot_process
    with _bot_lock:
        if _bot_process is None or _bot_process.poll() is not None:
            return jsonify({'status': 'not_running'})
        _bot_process.terminate()
        try:
            _bot_process.wait(timeout=5)
        except Exception:
            _bot_process.kill()
        pid = _bot_process.pid
        _bot_process = None
        logger.info('Stopped bot subprocess pid=%s', pid)
        return jsonify({'status': 'stopped', 'pid': pid})


@bp.route('/bot/status', methods=['GET'])
def bot_status():
    global _bot_process
    with _bot_lock:
        if _bot_process is None or _bot_process.poll() is not None:
            return jsonify({'running': False})
        return jsonify({'running': True, 'pid': _bot_process.pid})

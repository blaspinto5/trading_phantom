import os
import time
import subprocess

import pytest

import trading_phantom.webapp as webapp_mod


def test_bot_start_stop_writes_logs(tmp_path, monkeypatch):
    # Ensure logs dir exists and is empty
    logs_dir = os.path.abspath(os.path.join(os.path.dirname(webapp_mod.__file__), '..', 'logs'))
    os.makedirs(logs_dir, exist_ok=True)
    bot_log = os.path.join(logs_dir, 'bot.log')
    try:
        if os.path.exists(bot_log):
            os.remove(bot_log)
    except Exception:
        pass

    # Dummy Popen that yields two lines on stdout
    class DummyProc:
        def __init__(self):
            self.pid = 9999
            self.stdout = iter(["line1\n", "line2\n"])

        def poll(self):
            return None

        def terminate(self):
            pass

        def wait(self, timeout=None):
            pass

        def kill(self):
            pass

    def fake_popen(args, stdout, stderr, text, bufsize):
        return DummyProc()

    monkeypatch.setattr(subprocess, 'Popen', fake_popen)

    client = webapp_mod.app.test_client()

    # Start the bot
    rv = client.post('/api/bot/start', json={'iterations': 1})
    assert rv.status_code == 200
    data = rv.get_json()
    assert data['status'] == 'started'
    assert 'pid' in data

    # Wait briefly for the logging thread to write
    time.sleep(0.1)

    assert os.path.exists(bot_log)
    with open(bot_log, 'r', encoding='utf-8') as fh:
        content = fh.read()
    assert 'line1' in content
    assert 'line2' in content

    # Stop the bot
    rv2 = client.post('/api/bot/stop')
    assert rv2.status_code == 200
    assert rv2.get_json()['status'] in ('stopped', 'not_running')


def test_bot_status_not_running_after_stop(monkeypatch):
    # Make sure no bot is running
    client = webapp_mod.app.test_client()

    # Directly call stop to be idempotent
    client.post('/api/bot/stop')

    rv = client.get('/api/bot/status')
    assert rv.status_code == 200
    assert rv.get_json()['running'] is False

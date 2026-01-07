import os
from flask import Blueprint

# Environment toggles to enable specific modules (defaults True)
def _enabled(key: str) -> bool:
    return (os.getenv(key, 'true').lower() in ('1', 'true', 'yes'))


def register_blueprints(app):
    from . import backtest as bp_backtest
    from . import bot as bp_bot
    from . import logs as bp_logs
    from . import analytics as bp_analytics

    if _enabled('ENABLE_BACKTEST'):
        app.register_blueprint(bp_backtest.bp, url_prefix='/api')
    if _enabled('ENABLE_BOT'):
        app.register_blueprint(bp_bot.bp, url_prefix='/api')
    if _enabled('ENABLE_LOGS'):
        app.register_blueprint(bp_logs.bp, url_prefix='/api')
    if _enabled('ENABLE_ANALYTICS'):
        app.register_blueprint(bp_analytics.bp, url_prefix='/api')

# scripts/launcher.py

import argparse
import logging
import sys
import threading
import time
from pathlib import Path

# When frozen by PyInstaller, _MEIPASS contains extracted files; add to sys.path
if getattr(sys, "frozen", False):
    meipass = getattr(sys, "_MEIPASS", None)
    if meipass:
        sys.path.insert(0, str(meipass))
else:
    # development: prefer src/ layout; also add repo root as fallback
    root = Path(__file__).resolve().parent.parent
    src = root / "src"
    # Ensure canonical package resolution (prefer src/ over repo root)
    sys.path.insert(0, str(src))
    # Do not add repo root to sys.path to avoid accidentally importing legacy copies
    # Also set PYTHONPATH env for subprocesses/tools that rely on it
    import os

    os.environ.setdefault("PYTHONPATH", str(src))

# Defer importing trading_phantom.webapp until the server is actually started
# to avoid import-time errors in frozen executables where package discovery
# may behave differently. `webapp` will be set by `_start_flask`.
webapp = None


def _import_webapp():
    """Lazy import helper for trading_phantom.webapp with clear errors."""
    global webapp
    if webapp is not None:
        return webapp
    import importlib

    log = logging.getLogger(__name__)
    try:
        webapp = importlib.import_module("trading_phantom.webapp")
        return webapp
    except Exception as e:
        log.exception("Failed to import trading_phantom.webapp")
        raise


log = logging.getLogger(__name__)

try:
    import webview
except Exception:
    webview = None
    log.warning("pywebview not available; running without native window")


def _start_flask(host, port, debug):
    # When running Flask in a background thread, avoid debug reloader which uses signals
    log.info(
        "Starting Flask server on %s:%s (debug reloader disabled in threaded mode)",
        host,
        port,
    )
    # Import webapp lazily (helps when running from PyInstaller one-file exe)
    wb = _import_webapp()
    wb.run_app(host=host, port=port, debug=False)


def main():
    parser = argparse.ArgumentParser(description="Launch Trading Phantom Desktop app")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)

    t = threading.Thread(
        target=_start_flask, args=(args.host, args.port, args.debug), daemon=True
    )
    t.start()

    # Wait for server to start
    time.sleep(1.0)

    url = f"http://{args.host}:{args.port}/"
    if webview is not None:
        webview.create_window("Trading Phantom", url)
        webview.start()
    else:
        print("pywebview not installed. Open this URL in your browser: ", url)
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Shutting down...")


if __name__ == "__main__":
    try:
        main()
    except (
        Exception
    ) as exc:  # Capture any unhandled exception and make debugging easier
        import os
        import tempfile
        import traceback

        try:
            tb = traceback.format_exc()
            # write to temp file for post-mortem
            tmp = os.path.join(tempfile.gettempdir(), "trading_phantom_crash.log")
            with open(tmp, "w", encoding="utf-8") as f:
                f.write(tb)
            # print to stderr so console / run_exe_console.ps1 captures it
            print(
                "Unhandled exception in launcher; traceback written to:",
                tmp,
                file=sys.stderr,
            )
            print(tb, file=sys.stderr)
            # On Windows, show a message box with the first lines of the traceback
            try:
                import ctypes

                short = tb.splitlines()[-10:]
                ctypes.windll.user32.MessageBoxW(
                    None, "\n".join(short), "Unhandled exception in script", 0x00000010
                )
            except Exception:
                pass
        except Exception:
            # fallback: print whatever we have
            print("Failed to write crash log, exception:", exc, file=sys.stderr)
            import traceback as _tb

            _tb.print_exc()
        # re-raise so PyInstaller/GUIs still show error dialogs when appropriate
        raise

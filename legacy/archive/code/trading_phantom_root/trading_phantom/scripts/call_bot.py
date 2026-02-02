#!/usr/bin/env python3
"""Simple helper to start the bot via HTTP and print logs (for manual E2E checks)."""
import argparse
import time

import requests


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=5000)
    p.add_argument("--debug", action="store_true")
    p.add_argument("--iterations", type=int, default=1)
    args = p.parse_args()

    base = f"http://{args.host}:{args.port}"
    print("Starting bot...")
    r = requests.post(
        base + "/api/bot/start",
        json={"debug": args.debug, "iterations": args.iterations},
        timeout=5,
    )
    print("start response:", r.status_code, r.json())
    time.sleep(0.5)
    print("Fetching logs...")
    r2 = requests.get(base + "/api/logs?bot=true")
    print("logs:", r2.json().get("logs")[:1000])
    print("Stopping bot...")
    r3 = requests.post(base + "/api/bot/stop")
    print("stop response:", r3.status_code, r3.json())


if __name__ == "__main__":
    main()

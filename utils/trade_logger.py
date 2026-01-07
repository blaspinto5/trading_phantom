import csv
from datetime import datetime
from pathlib import Path

LOG_FILE = Path(__file__).resolve().parent / "trades.csv"

def log_trade(data: dict):
    file_exists = LOG_FILE.exists()

    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

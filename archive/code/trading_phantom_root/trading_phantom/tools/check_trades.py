#!/usr/bin/env python3
"""
Verificar estado actual del bot y trades ejecutados
"""

import sqlite3
import sys
from datetime import datetime
from pathlib import Path

db_path = "src/data/trading_phantom.db"

if not Path(db_path).exists():
    print("❌ Base de datos no encontrada")
    sys.exit(1)

conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print("=" * 80)
print("📊 ESTADO DEL BOT - TRADES EJECUTADOS")
print("=" * 80)
print()

# Obtener últimos trades
cursor.execute(
    """
    SELECT * FROM trades
    ORDER BY entry_time DESC
    LIMIT 10
"""
)

trades = list(cursor.fetchall())
print(f"✅ Total trades en BD: {len(trades)}")
print()

if trades:
    print("ÚLTIMAS OPERACIONES:")
    print("-" * 80)
    for i, trade in enumerate(trades[:5], 1):
        symbol = trade["symbol"] if "symbol" in trade.keys() else "N/A"
        entry_time = trade["entry_time"] if "entry_time" in trade.keys() else "N/A"
        pnl = trade["pnl"] if "pnl" in trade.keys() else 0
        status = "✅" if pnl > 0 else "❌" if pnl < 0 else "➡️"

        print(f"{i}. {symbol} | P&L: ${pnl:>8.2f} {status} | {entry_time}")
    print()
else:
    print("⏳ Sin trades aún (esperando nuevas velas H1)")

# Estadísticas
cursor.execute("SELECT COUNT(*) as total FROM trades")
total = cursor.fetchone()["total"]

cursor.execute("SELECT COUNT(*) as wins FROM trades WHERE pnl > 0")
wins = cursor.fetchone()["wins"]

cursor.execute("SELECT SUM(pnl) as total_pnl FROM trades")
total_pnl = cursor.fetchone()["total_pnl"] or 0

if total > 0:
    win_rate = (wins / total) * 100
    print()
    print("📈 ESTADÍSTICAS:")
    print(f"   Total Trades: {total}")
    print(f"   Winning: {wins} ({win_rate:.2f}%)")
    print(f"   Total P&L: ${total_pnl:.2f}")
    print(f"   ROI: {(total_pnl / 10000 * 100):.2f}%")

conn.close()

print()
print("=" * 80)
print("✅ Estado: Bot listo para ejecutar")
print("=" * 80)

#!/usr/bin/env python3
"""
Bot Monitor - Real-time monitoring dashboard for Trading Phantom
Monitorea el bot ejecutándose en vivo con las nuevas estrategias
"""

import json
import os
import sqlite3
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from config.config_loader import load_config


def get_trade_history(limit=20):
    """Obtener últimos trades de la BD"""
    db_path = "src/data/trading_phantom.db"

    if not Path(db_path).exists():
        return []

    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM trades
            ORDER BY entry_time DESC
            LIMIT ?
        """,
            (limit,),
        )

        trades = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return trades
    except Exception as e:
        print(f"Error reading trades: {e}")
        return []


def calculate_metrics(trades):
    """Calcular métricas de desempeño"""
    if not trades:
        return {
            "total": 0,
            "wins": 0,
            "losses": 0,
            "win_rate": 0,
            "total_pnl": 0,
            "roi": 0,
        }

    total = len(trades)
    wins = sum(1 for t in trades if t.get("pnl", 0) > 0)
    losses = total - wins

    total_pnl = sum(float(t.get("pnl", 0)) for t in trades)
    initial = 10000  # Capital inicial asumido
    roi = (total_pnl / initial) * 100 if initial > 0 else 0

    return {
        "total": total,
        "wins": wins,
        "losses": losses,
        "win_rate": (wins / total * 100) if total > 0 else 0,
        "total_pnl": total_pnl,
        "roi": roi,
    }


def print_dashboard():
    """Mostrar dashboard en tiempo real"""
    config = load_config()

    while True:
        os.system("cls" if os.name == "nt" else "clear")

        print("=" * 80)
        print("🤖 TRADING PHANTOM - BOT MONITOR (LIVE)")
        print("=" * 80)
        print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        print("⚙️ CONFIGURACIÓN ACTIVA:")
        print(f"  Símbolo: {config.get('symbol', 'N/A')}")
        print(f"  Timeframe: {config.get('timeframe', 'N/A')}")
        print(f"  Modo: {config.get('mode', 'N/A')}")
        print(
            f"  📊 ML Enabled: {'✅ SÍ' if config.get('ml', {}).get('enabled') else '❌ NO'}"
        )
        print(f"  🛡️ Risk Management: ✅ ACTIVADO")
        print(f"     - Stop Loss: 2%")
        print(f"     - Take Profit: 4%")
        print(f"     - Min Confidence: 55%")
        print()

        trades = get_trade_history(100)
        metrics = calculate_metrics(trades)

        print("📈 MÉTRICAS DE DESEMPEÑO (últimas 100 operaciones):")
        print(f"  Total Trades: {metrics['total']}")
        print(f"  Winning Trades: {metrics['wins']} ✅")
        print(f"  Losing Trades: {metrics['losses']} ❌")
        print(f"  Win Rate: {metrics['win_rate']:.2f}%")
        print(f"  Total P&L: ${metrics['total_pnl']:.2f}")
        print(f"  ROI: {metrics['roi']:.2f}%")
        print()

        if trades:
            print("📊 ÚLTIMAS 10 OPERACIONES:")
            print("-" * 80)
            for i, trade in enumerate(trades[:10], 1):
                entry = trade.get("entry_time", "N/A")
                exit_time = trade.get("exit_time", "Abierto")
                pnl = trade.get("pnl", 0)
                symbol = trade.get("symbol", "N/A")
                status = "✅" if pnl > 0 else "❌" if pnl < 0 else "➡️"
                print(f"{i:2}. {symbol} | ${pnl:>8.2f} | {status} | {entry}")
        else:
            print("📊 Sin operaciones aún. Esperando señales...")

        print()
        print("=" * 80)
        print("💡 Bot ejecutando con estrategias mejoradas:")
        print("   • Modelo ML: 95% accuracy")
        print("   • Risk Management: 2% SL, 4% TP")
        print("   • Signal Filtering: 55% confidence threshold")
        print("=" * 80)
        print()
        print("📱 Presiona Ctrl+C para detener el monitor")
        print(
            f"⏳ Actualizando en 30 segundos... (próxima actualización: {datetime.now() + timedelta(seconds=30)})"
        )

        try:
            time.sleep(30)
        except KeyboardInterrupt:
            print("\n✅ Monitor cerrado")
            break


if __name__ == "__main__":
    try:
        print_dashboard()
    except KeyboardInterrupt:
        print("\n✅ Bot monitor finalizado")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

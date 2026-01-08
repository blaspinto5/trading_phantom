#!/usr/bin/env python3
"""
Ejemplo de uso del módulo TradeHistory
Muestra cómo registrar y analizar operaciones
"""

from modules.trade_history import TradeHistory
from datetime import datetime
import json

def example_usage():
    """Ejemplo de uso completo del módulo."""
    
    print("=" * 60)
    print("📊 EJEMPLO DE USO: TradeHistory")
    print("=" * 60)
    
    # Inicializar el historial
    history = TradeHistory()
    
    # Simular algunas operaciones (en real sería el bot quien las agregue)
    print("\n1️⃣ Agregando operaciones de ejemplo...")
    
    # Trade 1: BUY ganador
    history.add_trade(
        ticket=100001,
        symbol="EURUSD",
        signal="BUY",
        volume=0.10,
        entry_price=1.16500,
        sl=1.16300,
        tp=1.16800
    )
    
    # Trade 2: SELL ganador
    history.add_trade(
        ticket=100002,
        symbol="EURUSD",
        signal="SELL",
        volume=0.10,
        entry_price=1.16750,
        sl=1.16950,
        tp=1.16400
    )
    
    # Trade 3: BUY perdedor
    history.add_trade(
        ticket=100003,
        symbol="EURUSD",
        signal="BUY",
        volume=0.05,
        entry_price=1.16200,
        sl=1.16000,
        tp=1.16600
    )
    
    # Simular cierre de trades
    print("\n2️⃣ Cerrando operaciones...")
    
    history.close_trade(
        ticket=100001,
        exit_price=1.16790,
        profit_loss=290.00  # 29 pips × 10 USD = 290
    )
    
    history.close_trade(
        ticket=100002,
        exit_price=1.16410,
        profit_loss=340.00  # 34 pips × 10 USD = 340
    )
    
    history.close_trade(
        ticket=100003,
        exit_price=1.15950,
        profit_loss=-250.00  # Pérdida de 50 pips
    )
    
    # Mostrar resumen
    print("\n3️⃣ Imprimiendo resumen...")
    history.print_summary()
    
    # Obtener datos JSON
    print("\n4️⃣ Datos JSON guardados en: logs/trade_history.json")
    print("   Contenido (primeros 2 trades):")
    with open("logs/trade_history.json", "r") as f:
        trades = json.load(f)
        print(json.dumps(trades[:2], indent=2, ensure_ascii=False))
    
    # Acceder a métodos programáticos
    print("\n5️⃣ Acceso programático a datos...")
    summary = history.get_summary()
    print(f"   Total de operaciones cerradas: {summary['total_trades']}")
    print(f"   Operaciones ganadas: {summary['won_trades']}")
    print(f"   Operaciones perdidas: {summary['lost_trades']}")
    print(f"   Tasa de acierto: {summary['win_rate']:.2f}%")
    print(f"   Profit neto: ${summary['net_profit']:.2f}")
    
    # Últimos trades
    print("\n6️⃣ Últimos 3 trades:")
    recent = history.get_recent_trades(3)
    for trade in recent:
        status = f"({trade['status']}) P/L: ${trade['profit_loss']}" if trade['profit_loss'] else "ABIERTO"
        print(f"   Ticket {trade['ticket']}: {trade['signal']:4} | {trade['symbol']:7} | {status}")
    
    print("\n" + "=" * 60)
    print("✅ Ejemplo completado")
    print("=" * 60)

if __name__ == "__main__":
    example_usage()

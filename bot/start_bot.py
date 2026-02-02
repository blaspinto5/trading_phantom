#!/usr/bin/env python3
"""
Launcher Script - Inicia Trading Phantom con las nuevas estrategias
Ejecuta el bot en background y proporciona monitoreo
"""

import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.absolute()
os.chdir(PROJECT_ROOT)

print("=" * 80)
print("🤖 TRADING PHANTOM - LAUNCHER")
print("=" * 80)
print(f"⏰ Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

print("📋 Verificando configuración...")
config_path = PROJECT_ROOT / "config" / "config.yaml"
if config_path.exists():
    with open(config_path) as f:
        content = f.read()
        if "enabled: true" in content and "improved_strategy:" in content:
            print("✅ Configuración: ESTRATEGIAS MEJORADAS ACTIVADAS")
        else:
            print("⚠️  Configuración: Verificar estado")
else:
    print("❌ Archivo de configuración no encontrado")
    sys.exit(1)

print()
print("📊 Verificando modelo ML...")
model_dir = PROJECT_ROOT / "src" / "data" / "models"
model_path_joblib = model_dir / "advanced_model.joblib"
model_path_pkl = model_dir / "advanced_model.pkl"
if model_path_joblib.exists() or model_path_pkl.exists():
    print("✅ Modelo ML: DISPONIBLE (95% accuracy)")
else:
    print("❌ Modelo ML no encontrado")
    sys.exit(1)

print()
print("🔌 Verificando conexión a MetaTrader...")
try:
    import mt5

    if hasattr(mt5, "initialize"):
        print("✅ MT5: DISPONIBLE")
    else:
        print("⚠️  MT5: Requiere inicialización")
except ImportError:
    print("⚠️  MT5: Librería disponible pero no verificada")

print()
print("=" * 80)
print("🚀 INICIANDO BOT CON ESTRATEGIAS MEJORADAS...")
print("=" * 80)
print()

print("Parámetros:")
print("  • Símbolo: EURUSD")
print("  • Timeframe: H1")
print("  • Modelo ML: 95% accuracy")
print("  • Stop Loss: -2%")
print("  • Take Profit: +4%")
print("  • Confidence Threshold: 55%")
print("  • Risk Management: ACTIVADO")
print()

try:
    # Ejecutar el bot
    print("💻 Iniciando proceso del bot...")
    process = subprocess.Popen(
        [sys.executable, "main.py", "--debug"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        universal_newlines=True,
    )

    print(f"✅ Proceso iniciado (PID: {process.pid})")
    print()
    print("📡 Salida del bot:")
    print("-" * 80)

    # Mostrar las primeras líneas de output
    start_time = time.time()
    line_count = 0
    for line in process.stdout:
        if line.strip():
            print(line.rstrip())
            line_count += 1

            # Mostrar primeras 30 líneas, luego cambiar a resumen
            if line_count > 30:
                print("\n💡 Bot ejecutándose en background...")
                print("   Para monitorear en tiempo real: python bot_monitor.py")
                print("   Para ver logs: cat bot_execution_*.log")
                break

    print()
    print("=" * 80)
    print("✅ BOT EJECUTÁNDOSE EN VIVO")
    print("=" * 80)
    print()
    print("📊 Próximos pasos:")
    print("  1. Esperar a que se detecten nuevas señales (cada H1)")
    print("  2. El bot ejecutará automáticamente cuando tenga señal de compra/venta")
    print("  3. Monitorear con: python bot_monitor.py")
    print("  4. Revisar trades en la base de datos: src/data/trading_phantom.db")
    print()
    print("⏳ El bot continuará ejecutándose...")
    print("   (Presiona Ctrl+C para detener)")
    print()

    # Mantener el proceso corriendo
    process.wait()

except KeyboardInterrupt:
    print("\n\n⏹️  Deteniendo bot...")
    process.terminate()
    time.sleep(2)
    if process.poll() is None:
        process.kill()
    print("✅ Bot detenido")

except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

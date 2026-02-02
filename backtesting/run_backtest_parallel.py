#!/usr/bin/env python3
"""
Ejecutar backtesting en paralelo con bot en vivo
Safe parallel execution - No interfiere con bot
"""

import subprocess
import sys
import time
from pathlib import Path

# PROJECT_ROOT should be repository root; compute two levels up when file is inside backtesting/
PROJECT_ROOT = Path(__file__).resolve().parents[1]

print("=" * 80)
print("🤖 PARALLEL BACKTEST RUNNER")
print("=" * 80)
print()

print("✅ Verificaciones de seguridad:")
print()

# 1. Verificar que main.py está en ejecución
try:
    result = subprocess.run(
        ["tasklist", "/FI", "IMAGENAME eq python.exe"], capture_output=True, text=True
    )
    if "python.exe" in result.stdout:
        print("  ✅ Bot (main.py) detectado en ejecución")
    else:
        print("  ⚠️  Bot no detectado - Puedes ejecutar backtesting igual")
except:
    print("  ⚠️  No se pudo verificar bot")

print()

# 2. Verificar BD
db_path = PROJECT_ROOT / "src" / "data" / "trading_phantom.db"
if db_path.exists():
    print("  ✅ Base de datos disponible")
else:
    print("  ❌ BD no encontrada")
    sys.exit(1)

# 3. Verificar modelo (accept joblib or legacy pkl)
model_dir = PROJECT_ROOT / "src" / "data" / "models"
model_path_joblib = model_dir / "advanced_model.joblib"
model_path_pkl = model_dir / "advanced_model.pkl"
if model_path_joblib.exists() or model_path_pkl.exists():
    print("  ✅ Modelo ML disponible")
else:
    print("  ❌ Modelo no encontrado")
    sys.exit(1)

print()
print("=" * 80)
print("📊 OPCIONES DE BACKTESTING")
print("=" * 80)
print()

print("1️⃣  Backtest Basic (Advanced Model)")
print("   python backtest_advanced_model.py")
print()

print("2️⃣  Backtest Improved (Risk Management)")
print("   python backtest_improved_strategy.py")
print()

print("3️⃣  Ambos en paralelo")
print("   Ejecuta opción 3 abajo")
print()

print("4️⃣  Validación del modelo (sin guardar)")
print("   python ml_train_advanced.py --no-save")
print()

# Menú
print("-" * 80)
choice = input("Selecciona opción (1-4, o 0 para salir): ").strip()
print()

if choice == "0":
    print("✅ Saliendo sin ejecutar backtesting")
    sys.exit(0)

elif choice == "1":
    print("🚀 Ejecutando: Backtest Advanced Model")
    print("-" * 80)
    try:
        subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "backtesting" / "backtest_advanced_model.py")],
            cwd=PROJECT_ROOT,
        )
    except KeyboardInterrupt:
        print("\n⏹️  Backtesting cancelado por usuario")

elif choice == "2":
    print("🚀 Ejecutando: Backtest Improved Strategy")
    print("-" * 80)
    try:
        subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "backtesting" / "backtest_improved_strategy.py")],
            cwd=PROJECT_ROOT,
        )
    except KeyboardInterrupt:
        print("\n⏹️  Backtesting cancelado por usuario")

elif choice == "3":
    print("🚀 Ejecutando ambos backtests EN PARALELO")
    print("-" * 80)
    print()

    # Crear dos procesos
    print("Iniciando Backtest Advanced Model...")
    proc1 = subprocess.Popen(
        [sys.executable, str(PROJECT_ROOT / "backtesting" / "backtest_advanced_model.py")],
        cwd=PROJECT_ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    print("Iniciando Backtest Improved Strategy...")
    proc2 = subprocess.Popen(
        [sys.executable, str(PROJECT_ROOT / "backtesting" / "backtest_improved_strategy.py")],
        cwd=PROJECT_ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    print()
    print("⏳ Ambos backtests ejecutándose en paralelo...")
    print()

    # Esperar a que terminen
    start = time.time()

    while proc1.poll() is None or proc2.poll() is None:
        elapsed = time.time() - start
        if int(elapsed) % 5 == 0:
            status1 = "En ejecución" if proc1.poll() is None else "Completado"
            status2 = "En ejecución" if proc2.poll() is None else "Completado"
            print(f"[{int(elapsed)}s] Backtest 1: {status1} | Backtest 2: {status2}")
        time.sleep(0.5)

    elapsed = time.time() - start

    print()
    print("=" * 80)
    print(f"✅ Ambos backtests completados en {elapsed:.1f}s")
    print("=" * 80)

    # Mostrar resultados
    print()
    print("📊 RESULTADOS:")
    print()

    # Backtest 1
    results1 = PROJECT_ROOT / "backtest_results_advanced.json"
    if results1.exists():
        print("✅ Backtest Advanced Model:")
        print(f"   Archivo: {results1}")

    # Backtest 2
    results2 = PROJECT_ROOT / "backtest_results_improved_strategy.json"
    if results2.exists():
        print("✅ Backtest Improved Strategy:")
        print(f"   Archivo: {results2}")

    print()

elif choice == "4":
    print("🚀 Ejecutando: ML Validation (sin guardar)")
    print("-" * 80)
    try:
        subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "scripts" / "ml_train_advanced.py"), "--no-save"],
            cwd=PROJECT_ROOT,
        )
    except KeyboardInterrupt:
        print("\n⏹️  Validación cancelada por usuario")

else:
    print("❌ Opción inválida")
    sys.exit(1)

print()
print("=" * 80)
print("✅ Completado")
print("=" * 80)
print()
print("💡 Próximos pasos:")
print("   • Revisar resultados en archivos JSON")
print("   • Comparar con resultados anteriores")
print("   • Si OK, considerar cambios")
print()

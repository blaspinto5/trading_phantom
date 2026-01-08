#!/usr/bin/env python3
"""
Verificación de la instalación de nuevas características
Ejecuta este script para validar que todo está correctamente instalado
"""

import sys
from pathlib import Path

def check_files():
    """Verifica que todos los archivos necesarios existan."""
    print("=" * 60)
    print("✅ VERIFICACIÓN DE INSTALACIÓN")
    print("=" * 60)
    
    checks = []
    
    # Archivos nuevos
    files_to_check = [
        ("modules/trade_history.py", "Módulo de Historial"),
        ("scripts/example_trade_history.py", "Ejemplo de Historial"),
        ("config/config.yaml", "Configuración"),
        ("CAMBIOS_REALIZADOS.md", "Documentación de cambios"),
        ("UPDATES_STRATEGY_AND_HISTORY.md", "Documentación de estrategia"),
        ("QUICK_START_NEW_FEATURES.md", "Guía rápida"),
        ("IMPLEMENTACION_COMPLETADA.txt", "Resumen de implementación"),
    ]
    
    print("\n📁 Verificando archivos:")
    print("-" * 60)
    
    all_exist = True
    for file_path, description in files_to_check:
        full_path = Path(file_path)
        if full_path.exists():
            print(f"✅ {description:35} ({file_path})")
            checks.append(True)
        else:
            print(f"❌ {description:35} ({file_path})")
            checks.append(False)
            all_exist = False
    
    return all_exist

def check_imports():
    """Verifica que los módulos pueden ser importados."""
    print("\n🔧 Verificando imports:")
    print("-" * 60)
    
    imports_to_check = [
        "modules.trade_history",
        "modules.strategy",
        "modules.trader",
        "core.orchestrator",
    ]
    
    all_imports_ok = True
    for module in imports_to_check:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module} - Error: {e}")
            all_imports_ok = False
    
    return all_imports_ok

def check_config():
    """Verifica la configuración."""
    print("\n⚙️  Verificando configuración:")
    print("-" * 60)
    
    try:
        from config.config_loader import load_config
        config = load_config()
        
        required_keys = ["symbol", "timeframe", "mode", "risk", "orders", "execution"]
        all_keys_present = True
        
        for key in required_keys:
            if key in config:
                print(f"✅ config['{key}']")
            else:
                print(f"❌ config['{key}'] FALTANTE")
                all_keys_present = False
        
        return all_keys_present
    except Exception as e:
        print(f"❌ Error cargando config: {e}")
        return False

def main():
    """Ejecuta todas las verificaciones."""
    
    print("\n")
    
    files_ok = check_files()
    imports_ok = check_imports()
    config_ok = check_config()
    
    print("\n" + "=" * 60)
    print("📊 RESULTADO DE VERIFICACIÓN")
    print("=" * 60)
    
    print(f"✅ Archivos:          {'OK' if files_ok else 'FALLA'}")
    print(f"✅ Imports:           {'OK' if imports_ok else 'FALLA'}")
    print(f"✅ Configuración:     {'OK' if config_ok else 'FALLA'}")
    
    if files_ok and imports_ok and config_ok:
        print("\n" + "🎉 " * 15)
        print("✅ VERIFICACIÓN EXITOSA - TODO ESTÁ CORRECTAMENTE INSTALADO")
        print("🎉 " * 15)
        print("\nAhora puedes ejecutar:")
        print("  .\RUN.bat")
        print("o")
        print("  .\RUN.ps1")
        print()
        return 0
    else:
        print("\n" + "❌ " * 15)
        print("⚠️  VERIFICACIÓN FALLIDA - REVISA LOS ERRORES ARRIBA")
        print("❌ " * 15)
        print()
        return 1

if __name__ == "__main__":
    sys.exit(main())

@echo off
REM RUN.bat - Ejecutar Trading Phantom (para usuarios sin PowerShell)
REM Doble-click para ejecutar

setlocal enabledelayedexpansion

if not exist ".venv\Scripts\activate.bat" (
    echo.
    echo ❌ Entorno virtual no encontrado.
    echo.
    echo Por favor ejecuta primero: INSTALL.bat
    echo.
    pause
    exit /b 1
)

echo.
echo ╔═══════════════════════════════════════════════════╗
echo ║       🚀 Trading Phantom - Iniciando...          ║
echo ╚═══════════════════════════════════════════════════╝
echo.
echo Abriendo en: http://127.0.0.1:5000
echo Presiona Ctrl+C para detener
echo.

call .venv\Scripts\activate.bat
python scripts/launcher.py --debug

pause

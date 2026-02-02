@echo off
REM INSTALL.bat - Instalación automatizada (para usuarios sin PowerShell)
REM Doble-click para ejecutar

setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                    Trading Phantom INSTALLER                   ║
echo ║                  Instalación automatizada (1-click)            ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Verificar Python
echo [1/5] Verificando Python 3.10+...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no encontrado. Descárgalo desde: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version') do set PYVER=%%i
echo ✅ %PYVER%
echo.

REM Crear venv
echo [2/5] Creando entorno virtual...
if exist ".venv" (
    echo ⚠️  .venv ya existe. Reutilizando...
) else (
    python -m venv .venv
    echo ✅ Entorno virtual creado
)
echo.

REM Instalar dependencias
echo [3/5] Instalando dependencias...
echo   - Actualizando pip...
call .venv\Scripts\python.exe -m pip install --upgrade pip setuptools wheel -q

echo   - Instalando requirements...
call .venv\Scripts\python.exe -m pip install -r requirements.txt -q
call .venv\Scripts\python.exe -m pip install -r requirements-dev.txt -q
echo ✅ Dependencias instaladas
echo.

REM Verificar instalación
echo [4/5] Verificando instalación...
call .venv\Scripts\python.exe -c "import flask; print('  Flask: OK')" 2>nul
if errorlevel 1 (
    echo ❌ Error en la instalación
    pause
    exit /b 1
)
echo.

REM Resumen
echo [5/5] Completado
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                    ✅ INSTALACIÓN COMPLETADA                   ║
echo ╠════════════════════════════════════════════════════════════════╣
echo ║                                                                ║
echo ║  🚀 Para iniciar la aplicación, ejecuta:                      ║
echo ║                                                                ║
echo ║     RUN.bat                   (Fácil - doble-click)           ║
echo ║                                                                ║
echo ║  O abre PowerShell y ejecuta:                                 ║
echo ║                                                                ║
echo ║     .\RUN.ps1                                                 ║
echo ║                                                                ║
echo ║  Para más información:                                         ║
echo ║                                                                ║
echo ║     • Ver: docs\README.md (guía completa)                      ║
echo ║     • Ver: docs\QUICKSTART.md (5 min setup)                    ║
echo ║     • Ver: docs\API.md (endpoints REST)                        ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
pause

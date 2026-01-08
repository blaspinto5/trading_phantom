@echo off
REM RUN_TESTS.bat - Ejecuta ruff y pytest

if not exist ".venv\Scripts\activate.bat" (
  echo ❌ Entorno virtual no encontrado. Ejecuta INSTALL.bat primero.
  pause
  exit /b 1
)

call .venv\Scripts\activate.bat
ruff check .
python -m pytest -q

echo ✅ Tests completados
pause

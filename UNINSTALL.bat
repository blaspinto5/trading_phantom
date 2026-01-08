@echo off
REM UNINSTALL.bat - Limpia venv, artefactos y logs

if exist ".venv" (
  echo Eliminando .venv...
  rmdir /S /Q .venv
)

for %%d in (dist build) do (
  if exist "%%d" (
    echo Eliminando %%d...
    rmdir /S /Q %%d
  )
)

for %%f in (dist_exe_stdout.log dist_exe_stderr.log exe_console.pid launcher.pid) do (
  if exist "%%f" del /Q "%%f"
)

echo ✅ Limpieza completada
pause

@echo off
REM BUILD_EXE.bat - Construye el ejecutable (.exe)

set ARG=
if "%1"=="-console" set ARG=-console

powershell -ExecutionPolicy Bypass -File scripts\build_exe.ps1 %ARG%

pause

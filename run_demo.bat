@echo off
REM Simple wrapper to run the bot in demo mode
REM Usage: run_demo.bat 40 debug
SET ITERATIONS=%1
IF "%ITERATIONS%"=="" SET ITERATIONS=40
SET DEBUG_FLAG=
IF "%2"=="debug" SET DEBUG_FLAG=--debug
python -m trading_phantom.main --iterations %ITERATIONS% %DEBUG_FLAG%

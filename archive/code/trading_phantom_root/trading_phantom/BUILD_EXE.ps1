# BUILD_EXE.ps1
# 📦 Construye el ejecutable con PyInstaller usando scripts/build_exe.ps1
# Uso: .\BUILD_EXE.ps1 [-console]

param([switch]$console)

$argsList = @()
if ($console) { $argsList += '-console' }

Write-Host "Iniciando build del EXE..." -ForegroundColor Cyan
& .\scripts\build_exe.ps1 @argsList

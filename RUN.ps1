# RUN.ps1
# 🚀 Ejecutar Trading Phantom (fácil)
# Uso: .\RUN.ps1

# Verificar si venv existe
if (-not (Test-Path .\.venv\Scripts\Activate.ps1)) {
    Write-Host "❌ Entorno virtual no encontrado." -ForegroundColor Red
    Write-Host "Ejecuta primero: .\INSTALL.ps1" -ForegroundColor Yellow
    exit 1
}

Write-Host @"
╔═══════════════════════════════════════════════════╗
║       🚀 Trading Phantom - Iniciando...          ║
╚═══════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan

# Activar venv silenciosamente
& .\.venv\Scripts\Activate.ps1 | Out-Null

# Iniciar aplicación
Write-Host "Abriendo en: http://127.0.0.1:5000" -ForegroundColor Green
Write-Host "Presiona Ctrl+C para detener" -ForegroundColor Yellow
Write-Host ""

python scripts/launcher.py --debug

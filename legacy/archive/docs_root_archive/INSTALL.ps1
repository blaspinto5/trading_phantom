# INSTALL.ps1
# 🚀 Instalación completa automatizada de Trading Phantom
# Uso: .\INSTALL.ps1

Write-Host @"
╔════════════════════════════════════════════════════════════════╗
║                    Trading Phantom INSTALLER                   ║
║                  Instalación automatizada (1-click)            ║
╚════════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan

# Validar Python
Write-Host "`n[1/5] Verificando Python 3.10+..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Python no encontrado. Descárgalo desde: https://www.python.org/downloads/" -ForegroundColor Red
    exit 1
}
Write-Host "✅ $pythonVersion" -ForegroundColor Green

# Crear venv
Write-Host "`n[2/5] Creando entorno virtual..." -ForegroundColor Yellow
if (Test-Path .\.venv) {
    Write-Host "⚠️  .venv ya existe. Reutilizando..." -ForegroundColor Cyan
} else {
    python -m venv .venv
    Write-Host "✅ Entorno virtual creado" -ForegroundColor Green
}

# Activar venv
Write-Host "`n[3/5] Activando entorno virtual..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error al activar venv" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Entorno activado" -ForegroundColor Green

# Instalar dependencias
Write-Host "`n[4/5] Instalando dependencias..." -ForegroundColor Yellow
Write-Host "  - Actualizando pip..." -ForegroundColor Gray
python -m pip install --upgrade pip setuptools wheel -q

Write-Host "  - Instalando requirements.txt..." -ForegroundColor Gray
pip install -r requirements.txt -q

Write-Host "  - Instalando requirements-dev.txt..." -ForegroundColor Gray
pip install -r requirements-dev.txt -q

Write-Host "✅ Dependencias instaladas" -ForegroundColor Green

# Verificar instalación
Write-Host "`n[5/5] Verificando instalación..." -ForegroundColor Yellow
python -c "import flask, pandas, numpy; print('  Flask: ✅'); print('  Pandas: ✅'); print('  Numpy: ✅')"

Write-Host @"
╔════════════════════════════════════════════════════════════════╗
║                    ✅ INSTALACIÓN COMPLETADA                   ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  🚀 Para iniciar la aplicación, ejecuta:                      ║
║                                                                ║
║     .\RUN.ps1                  (Recomendado - más fácil)      ║
║                                                                ║
║  O manualmente:                                                ║
║                                                                ║
║     python scripts/launcher.py --debug                        ║
║                                                                ║
║  Para ejecutar tests:                                          ║
║                                                                ║
║     python -m pytest -q                                        ║
║                                                                ║
║  Para más información:                                         ║
║                                                                ║
║     • Ver: docs/README.md (guía completa)                      ║
║     • Ver: docs/QUICKSTART.md (5 min setup)                    ║
║     • Ver: docs/API.md (endpoints REST)                        ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Green

# Ofrecer opción de ejecutar inmediatamente
$response = Read-Host "`n¿Deseas ejecutar la aplicación ahora? (s/n)"
if ($response -eq 's' -or $response -eq 'S' -or $response -eq 'yes') {
    Write-Host "`nIniciando Trading Phantom..." -ForegroundColor Cyan
    python scripts/launcher.py --debug
} else {
    Write-Host "`nPara ejecutar después: .\RUN.ps1" -ForegroundColor Yellow
}

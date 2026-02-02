# RUN_TESTS.ps1
# 🧪 Ejecuta tests y linter
# Uso: .\RUN_TESTS.ps1

if (-not (Test-Path .\.venv\Scripts\Activate.ps1)) {
    Write-Host "❌ Entorno virtual no encontrado. Ejecuta INSTALL.ps1 primero." -ForegroundColor Red
    exit 1
}

& .\.venv\Scripts\Activate.ps1

Write-Host "\n[1/3] Ruff (lint)..." -ForegroundColor Yellow
ruff check .

Write-Host "\n[2/3] Ruff fix (opcional)..." -ForegroundColor Yellow
$resp = Read-Host "¿Aplicar fixes automáticos? (s/n)"
if ($resp -match '^(s|S|yes)$') {
    ruff check --fix .
}

Write-Host "\n[3/3] Pytest..." -ForegroundColor Yellow
python -m pytest -q

Write-Host "\n✅ Tests completados" -ForegroundColor Green

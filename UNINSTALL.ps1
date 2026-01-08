# UNINSTALL.ps1
# 🔧 Limpieza del entorno: elimina venv, artefactos y logs
# Uso: .\UNINSTALL.ps1

Write-Host "\n[1/3] Eliminando entorno virtual (.venv)..." -ForegroundColor Yellow
if (Test-Path .\.venv) {
    try {
        Remove-Item -Recurse -Force .\.venv
        Write-Host "✅ .venv eliminado" -ForegroundColor Green
    } catch {
        Write-Host "❌ No se pudo eliminar .venv (ciérralo en otra terminal)" -ForegroundColor Red
    }
} else {
    Write-Host "ℹ️ No existe .venv" -ForegroundColor Cyan
}

Write-Host "\n[2/3] Eliminando artefactos de build (dist/, build/)..." -ForegroundColor Yellow
foreach ($dir in @('dist','build')) {
    if (Test-Path $dir) {
        try {
            Remove-Item -Recurse -Force $dir
            Write-Host "✅ $dir eliminado" -ForegroundColor Green
        } catch {
            Write-Host "❌ No se pudo eliminar $dir" -ForegroundColor Red
        }
    } else {
        Write-Host "ℹ️ $dir no existe" -ForegroundColor Cyan
    }
}

Write-Host "\n[3/3] Eliminando logs y PIDs..." -ForegroundColor Yellow
foreach ($file in @('dist_exe_stdout.log','dist_exe_stderr.log','exe_console.pid','launcher.pid')) {
    if (Test-Path $file) {
        Remove-Item -Force $file
        Write-Host "🗑️  Eliminado: $file" -ForegroundColor Green
    }
}

Write-Host "\n✅ Limpieza completada" -ForegroundColor Green

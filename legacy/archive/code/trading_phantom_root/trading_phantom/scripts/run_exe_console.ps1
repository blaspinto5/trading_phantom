$ErrorActionPreference='Stop'
if (Test-Path exe_console.pid) { Stop-Process -Id (Get-Content exe_console.pid) -ErrorAction SilentlyContinue; Remove-Item exe_console.pid -ErrorAction SilentlyContinue }
$stdout = Join-Path (Get-Location) 'dist_exe_stdout.log'
$stderr = Join-Path (Get-Location) 'dist_exe_stderr.log'
if (Test-Path $stdout) { Remove-Item $stdout -ErrorAction SilentlyContinue }
if (Test-Path $stderr) { Remove-Item $stderr -ErrorAction SilentlyContinue }
$p = Start-Process -FilePath '.\dist\TradingPhantom.exe' -ArgumentList '--debug' -RedirectStandardOutput $stdout -RedirectStandardError $stderr -PassThru
$p.Id | Out-File exe_console.pid
Write-Output "La exe se inició (PID $($p.Id)), esperaré 5s y mostraré logs..."
Start-Sleep -Seconds 5
try { Get-Content -Path $stdout -ErrorAction SilentlyContinue -Wait -Tail 200 } catch { }
try { Get-Content -Path $stderr -ErrorAction SilentlyContinue -Wait -Tail 200 } catch { }
# Stop process
Stop-Process -Id $p.Id -Force -ErrorAction SilentlyContinue
Remove-Item exe_console.pid -ErrorAction SilentlyContinue
Write-Output 'Proceso detenido.'

$ErrorActionPreference='Stop'
if (Test-Path exe.pid) { Stop-Process -Id (Get-Content exe.pid) -ErrorAction SilentlyContinue; Remove-Item exe.pid -ErrorAction SilentlyContinue }
$p = Start-Process -FilePath '.\dist\TradingPhantom.exe' -PassThru
$p.Id | Out-File exe.pid
Write-Output "Started exe with PID $($p.Id)"

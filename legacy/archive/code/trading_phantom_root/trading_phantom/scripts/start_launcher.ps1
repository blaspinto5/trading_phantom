$ErrorActionPreference='Stop'
if (Test-Path launcher.pid) { Stop-Process -Id (Get-Content launcher.pid) -ErrorAction SilentlyContinue; Remove-Item launcher.pid -ErrorAction SilentlyContinue }
$p = Start-Process -FilePath .\.venv\Scripts\python.exe -ArgumentList 'scripts\launcher.py','--debug' -PassThru
$p.Id | Out-File launcher.pid
Write-Output "Started launcher with PID $($p.Id)"

$ErrorActionPreference = 'Stop'
$body = @{iterations=1} | ConvertTo-Json
$r = Invoke-RestMethod -Uri 'http://127.0.0.1:5000/api/bot/start' -Method POST -Body $body -ContentType 'application/json' -TimeoutSec 30
Write-Output ($r | ConvertTo-Json -Depth 4)
Start-Sleep -Seconds 2
$status = Invoke-RestMethod -Uri 'http://127.0.0.1:5000/api/bot/status' -Method GET -TimeoutSec 10
Write-Output ($status | ConvertTo-Json -Depth 4)
# Stop if running
Invoke-RestMethod -Uri 'http://127.0.0.1:5000/api/bot/stop' -Method POST -TimeoutSec 10 | ConvertTo-Json -Depth 4 | Write-Output

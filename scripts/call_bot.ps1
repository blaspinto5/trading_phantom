# PowerShell helper to call /api/bot/start with correct JSON conversion
$payload = @{ debug = $true; iterations = 1 }
$body = $payload | ConvertTo-Json -Depth 5
Invoke-RestMethod -Uri http://127.0.0.1:5000/api/bot/start -Method Post -Body $body -ContentType 'application/json'

# View bot logs
Invoke-RestMethod -Uri 'http://127.0.0.1:5000/api/logs?bot=true' -Method Get

# Stop the bot
Invoke-RestMethod -Uri http://127.0.0.1:5000/api/bot/stop -Method Post
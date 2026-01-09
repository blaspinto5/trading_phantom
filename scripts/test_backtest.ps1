$ErrorActionPreference = 'Stop'
$uri = 'http://127.0.0.1:5000/api/backtest'
$body = '{}'
$job = Invoke-RestMethod -Uri $uri -Method POST -Body $body -ContentType 'application/json' -TimeoutSec 30
Write-Output "Job: $($job.job_id)"
$id = $job.job_id
for ($i=0; $i -lt 60; $i++) {
    Start-Sleep -Seconds 1
    $status = Invoke-RestMethod -Uri ("http://127.0.0.1:5000/api/backtest/" + $id) -Method GET -TimeoutSec 30
    if ($status.status -eq 'done' -or $status.status -eq 'error') {
        Write-Output (ConvertTo-Json $status -Depth 6)
        break
    } else {
        Write-Output "waiting... $i"
    }
}

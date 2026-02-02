# run_demo.ps1
# Run the bot in demo mode with configurable iterations. Usage:
# .\run_demo.ps1 -Iterations 40 -Debug
param(
    [int]$Iterations = 40,
    [switch]$Debug
)

$env:PYTHONUNBUFFERED = "1"
$script = "-m trading_phantom.main --iterations $Iterations"
if ($Debug) { $script += " --debug" }

Write-Host "▶ Running: python $script" -ForegroundColor Cyan
python $script

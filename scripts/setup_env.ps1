# setup_env.ps1
# Create a venv and install requirements (Windows PowerShell)
param(
    [string]$venvName = ".venv"
)

python -m venv $venvName
& .\$venvName\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
Write-Host "✅ Environment ready. Activate with: .\$venvName\Scripts\Activate.ps1" -ForegroundColor Green

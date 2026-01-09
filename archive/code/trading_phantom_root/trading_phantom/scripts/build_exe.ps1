# scripts/build_exe.ps1
# PowerShell helper to build a single-file .exe using PyInstaller

param(
  [string]$venvPath = ".venv",
  [string]$entry = "scripts\launcher.py",
  [string]$distName = "TradingPhantom.exe",
  [switch]$onefile,
  [switch]$windowed,
  [switch]$console
)

# Default behavior: generate a one-file windowed exe unless explicitly unset
if (-not $PSBoundParameters.ContainsKey('onefile')) { $onefile = $true }
if (-not $PSBoundParameters.ContainsKey('windowed')) { $windowed = $true }
# Allow forcing console mode via -console
if ($PSBoundParameters.ContainsKey('console')) { $windowed = $false }

# 1) Create and activate a venv (if missing)
if (!(Test-Path $venvPath)) {
  python -m venv $venvPath
}

# Activate
$activate = Join-Path $venvPath "Scripts\Activate.ps1"
Write-Host "Activating venv: $activate"
. $activate

pip install --upgrade pip
pip install -r trading_phantom/requirements.txt
pip install pyinstaller

# 2) Build with PyInstaller
$pyinstallerArgs = @()
$pyinstallerArgs += "--noconfirm"
if ($onefile) { $pyinstallerArgs += "--onefile" } else { $pyinstallerArgs += "--onedir" }
$pyinstallerArgs += @("--name", "TradingPhantom")
if ($windowed) { $pyinstallerArgs += "--windowed" }

# Include templates and static files so Flask can find them at runtime
$pyinstallerArgs += @(
  "--add-data", "trading_phantom\templates;trading_phantom\templates",
  "--add-data", "trading_phantom\static;trading_phantom\static",
  "--add-data", "trading_phantom\config\config.yaml;trading_phantom\config",
  "--add-data", "StrategyAdapter.html;.",
  "--add-data", "RSISMAStrategy.html;.",
  # Hidden imports often required for frozen apps
  "--hidden-import", "flask",
  "--hidden-import", "webview",
  "--hidden-import", "pkg_resources.py2_warn",
  # Collect all resources and submodules from the package to avoid missing modules
  "--collect-all", "trading_phantom"
)

# Append the entry script
$pyinstallerArgs += $entry

Write-Host "Running pyinstaller with args: $pyinstallerArgs"
pyinstaller @pyinstallerArgs

# 3) Move the generated executable to a predictable location
if ($onefile) {
  $built = Join-Path "dist" "TradingPhantom.exe"
  if (Test-Path $built) {
    Copy-Item $built -Destination (Join-Path (Get-Location) "dist\$distName") -Force
    Write-Host "Copied $built to dist\$distName"
  }
}

Write-Host "Build finished. Result in: dist\ (look for TradingPhantom.exe or the dist folder)"

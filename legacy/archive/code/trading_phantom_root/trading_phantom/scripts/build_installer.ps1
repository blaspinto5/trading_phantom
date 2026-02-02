# scripts/build_installer.ps1
# Helper to build the Inno Setup installer (requires Inno Setup installed and ISCC in PATH)

param(
  [string]$issFile = "installer\TradingPhantom.iss"
)

if (!(Test-Path $issFile)) {
  Write-Error "ISS file not found: $issFile"
  exit 1
}

# Build the installer
Write-Host "Running ISCC $issFile"
$iscc = "ISCC"
& $iscc $issFile

if ($LASTEXITCODE -eq 0) {
  Write-Host "Installer built. Check the installer directory."
} else {
  Write-Error "ISCC failed with exit code $LASTEXITCODE"
}

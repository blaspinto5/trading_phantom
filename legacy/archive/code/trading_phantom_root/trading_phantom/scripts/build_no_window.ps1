Set-Location -Path (Split-Path -Parent $MyInvocation.MyCommand.Definition)
$ErrorActionPreference='Stop'
. .\.venv\Scripts\Activate.ps1
. .\scripts\build_exe.ps1 -onefile -windowed:$false

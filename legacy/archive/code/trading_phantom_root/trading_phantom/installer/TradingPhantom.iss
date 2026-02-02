; installer/TradingPhantom.iss
; Inno Setup script template - edit paths as needed before running

[Setup]
AppName=Trading Phantom
AppVersion=1.0
DefaultDirName={pf}\Trading Phantom
DefaultGroupName=Trading Phantom
OutputDir=installer
OutputBaseFilename=TradingPhantom_Setup
Compression=lzma
SolidCompression=yes

[Files]
; Include the built exe (adjust path if you used --onefile or --onedir)
Source: "dist\TradingPhantom.exe"; DestDir: "{app}"; Flags: ignoreversion
; Include config and HTML resources if needed
Source: "StrategyAdapter.html"; DestDir: "{app}"; Flags: ignoreversion
Source: "RSISMAStrategy.html"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Trading Phantom"; Filename: "{app}\TradingPhantom.exe"

[Run]
Filename: "{app}\TradingPhantom.exe"; Description: "Launch Trading Phantom"; Flags: nowait postinstall skipifsilent

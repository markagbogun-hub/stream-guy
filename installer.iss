; installer.iss — Inno Setup script for RadioCastOS.
; Build with: iscc /DMyAppVersion=<x.y.z> installer.iss   (ISCC.exe from Inno Setup 6, on Windows or via CI)
; Produces:   Output\RadioCastOS-Setup.exe
;
; Expects the PyInstaller folder build at dist\RadioCastOS\ (see build.spec)
; to already exist before this runs — the CI workflow does both steps in order.

#define MyAppName "RadioCastOS"
; The version is NOT written here. It comes from src/version.py via
;   iscc /DMyAppVersion=<x.y.z> installer.iss
; (CI and local-build.bat do this using scripts/version_info.py).
#ifndef MyAppVersion
  #error MyAppVersion is not defined. Run: iscc /DMyAppVersion=$(python scripts/version_info.py) installer.iss
#endif
#define MyAppPublisher "CircuitBridge Technologies"
#define MyAppExeName "RadioCastOS.exe"

[Setup]
AppId={{B3E2B8B2-6B2C-4E4B-9C1A-7A1D5F4C9E20}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL=https://circuitbridgetechnologies.name.ng
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputDir=Output
OutputBaseFilename=RadioCastOS-Setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
LicenseFile=LICENSE
SetupIconFile=assets\icon.ico
; Comment ArchitecturesInstallIn64BitMode out if you need to support 32-bit
; Windows too; the bundled ffmpeg.exe determines what's actually required.
ArchitecturesInstallIn64BitMode=x64compatible
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
; Code signing. Only active when iscc is given /DSignToolName=<name> and /S<name>=<command>
; (local-build.bat does this when RCOS_SIGN_THUMBPRINT or RCOS_SIGN_PFX is set).
#ifdef SignToolName
SignTool={#SignToolName}
SignedUninstaller=yes
#endif

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons:"; Flags: unchecked

[Files]
; Pull in the entire PyInstaller output folder (exe + ffmpeg.exe + libs).
Source: "dist\RadioCastOS\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "LICENSE"; DestDir: "{app}"; Flags: ignoreversion
Source: "THIRD-PARTY-NOTICES.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "docs\RadioCastOS-Quick-Start-and-User-Guide.pdf"; DestDir: "{app}"; Flags: ignoreversion
Source: "docs\INSTALL-GUIDE.txt"; DestDir: "{app}"; Flags: ignoreversion skipifsourcedoesntexist

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{#MyAppName} Quick Start and User Guide"; Filename: "{app}\RadioCastOS-Quick-Start-and-User-Guide.pdf"
Name: "{group}\{#MyAppName} Install Guide"; Filename: "{app}\INSTALL-GUIDE.txt"; Check: FileExists(ExpandConstant('{app}\INSTALL-GUIDE.txt'))
Name: "{group}\Uninstall {#MyAppName}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}"

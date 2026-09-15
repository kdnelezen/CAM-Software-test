; Inno Setup test installer for CAM Software Test.
; Expected packaged app artifacts: dist\CAMSoftware\cam-software.exe plus PyInstaller support files.
; Replace the placeholders below if/when release branding is finalized.

#define MyAppName "CAM Software Test"
#define MyAppVersion "0.1.0"
#define MyAppPublisher "kdnelezen"
#define MyAppExeName "cam-software.exe"
#define MyAppSourceDir "dist\\CAMSoftware"

[Setup]
AppId={{5B658B1B-A12A-4F4F-839A-2CB1A1374F15}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
UninstallDisplayIcon={app}\{#MyAppExeName}
Compression=lzma
SolidCompression=yes
OutputDir=build\windows\inno
OutputBaseFilename=CAMSoftwareSetup
ArchitecturesInstallIn64BitMode=x64compatible
WizardStyle=modern

[Files]
Source: "{#MyAppSourceDir}\\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; Flags: unchecked

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent

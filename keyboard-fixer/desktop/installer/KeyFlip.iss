; Inno Setup script for KeyFlip (https://jrsoftware.org/isinfo.php).
; Build: ISCC.exe /DSourceExe=C:\path\to\KeyFlip.exe /DAppVersion=0.1.0.15 KeyFlip.iss  ->  output\KeyFlip-Setup-x64.exe
#ifndef AppVersion
  #define AppVersion "0.1.0.0"
#endif
#ifndef SourceExe
  #error Define SourceExe: path to the published KeyFlip.exe
#endif

[Setup]
AppId={{72050D37-6501-472A-AA30-1341AE5E8D69}
AppName=KeyFlip
AppVersion={#AppVersion}
AppVerName=KeyFlip {#AppVersion}
AppPublisher=diamondrubinny
AppPublisherURL=https://github.com/diamondrubinny/diamondrubinny
AppSupportURL=https://github.com/diamondrubinny/diamondrubinny/issues
VersionInfoVersion={#AppVersion}
DefaultDirName={autopf}\KeyFlip
DisableProgramGroupPage=yes
DisableDirPage=auto
; Installs for the current user without admin rights; the user may choose "all users" in the dialog.
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
OutputDir=output
OutputBaseFilename=KeyFlip-Setup-x64
SetupIconFile=..\KeyFlip.App\Assets\keyflip.ico
UninstallDisplayIcon={app}\KeyFlip.exe
UninstallDisplayName=KeyFlip
LicenseFile=..\..\LICENSE
InfoBeforeFile=privacy-notice.txt
Compression=lzma2
SolidCompression=yes
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
WizardStyle=modern
CloseApplications=yes
RestartApplications=no

[Tasks]
Name: "autostart"; Description: "Start KeyFlip when I sign in to Windows"; Flags: unchecked

[Files]
Source: "{#SourceExe}"; DestDir: "{app}"; DestName: "KeyFlip.exe"; Flags: ignoreversion
Source: "..\..\LICENSE"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\..\NOTICE.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\KeyFlip"; Filename: "{app}\KeyFlip.exe"

[Registry]
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "KeyFlip"; ValueData: """{app}\KeyFlip.exe"""; Flags: uninsdeletevalue; Tasks: autostart

[Run]
Filename: "{app}\KeyFlip.exe"; Description: "Launch KeyFlip"; Flags: nowait postinstall skipifsilent

[UninstallRun]
Filename: "{sys}\taskkill.exe"; Parameters: "/F /IM KeyFlip.exe"; Flags: runhidden; RunOnceId: "StopKeyFlip"

[Code]
procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
  SettingsDir: String;
begin
  if CurUninstallStep <> usPostUninstall then Exit;
  // The tray menu can also create the startup entry; remove it whichever way it was created.
  RegDeleteValue(HKEY_CURRENT_USER, 'Software\Microsoft\Windows\CurrentVersion\Run', 'KeyFlip');
  SettingsDir := ExpandConstant('{userappdata}\KeyFlip');
  if DirExists(SettingsDir) and (not UninstallSilent) then
  begin
    if MsgBox('Also delete KeyFlip settings (' + SettingsDir + ')?', mbConfirmation, MB_YESNO or MB_DEFBUTTON2) = IDYES then
      DelTree(SettingsDir, True, True, True);
  end;
end;

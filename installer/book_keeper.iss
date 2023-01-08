; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "Book Keeper"
#define MyAppVersion "1.0"
#define MyAppExeName "book_keeper_window.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{EDE3DF98-38A6-40AF-94A8-E86C9F55737D}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
DefaultDirName={autopf}\BookKeeper
DisableProgramGroupPage=yes
; Remove the following line to run in administrative install mode (install for all users.)
;PrivilegesRequired=lowest
OutputBaseFilename=book_keeper_installer
SetupIconFile=.\icons8-install-58.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "..\dist\book_keeper_window\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\dist\book_keeper_window\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Dirs]
Name: "{%TEMP}\book_keeper"

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Registry]
Root: HKLM; Subkey: "SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_hu-HU_Szabolcs"; Flags: uninsdeletekeyifempty
Root: HKLM; Subkey: "SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_hu-HU_Szabolcs"; ValueType: string; ValueName: ""; ValueData: "Microsoft Szabolcs - Hungarian (Hungary)"; Flags: uninsdeletevalue
Root: HKLM; Subkey: "SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_hu-HU_Szabolcs"; ValueType: string; ValueName: "40E"; ValueData: "Microsoft Szabolcs - Hungarian (Hungary)"; Flags: uninsdeletevalue
Root: HKLM; Subkey: "SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_hu-HU_Szabolcs"; ValueType: string; ValueName: "CLSID"; ValueData: "{{179F3D56-1B0B-42B2-A962-59B7EF59FE1B}"; Flags: uninsdeletevalue
Root: HKLM; Subkey: "SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_hu-HU_Szabolcs"; ValueType: expandsz; ValueName: "LangDataPath"; ValueData: "%windir%\Speech_OneCore\Engines\TTS\hu-HU\MSTTSLocHuHU.dat"; Flags: uninsdeletevalue
Root: HKLM; Subkey: "SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_hu-HU_Szabolcs"; ValueType: expandsz; ValueName: "VoicePath"; ValueData: "%windir%\Speech_OneCore\Engines\TTS\hu-HU\M1038Szabolcs"; Flags: uninsdeletevalue
Root: HKLM; Subkey: "SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_hu-HU_Szabolcs\Attributes"; Flags: uninsdeletekeyifempty
Root: HKLM; Subkey: "SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_hu-HU_Szabolcs\Attributes"; ValueType: string; ValueName: "Age"; ValueData: "Adult"; Flags: uninsdeletevalue
Root: HKLM; Subkey: "SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_hu-HU_Szabolcs\Attributes"; ValueType: string; ValueName: "DataVersion"; ValueData: "11.0.2016.1016"; Flags: uninsdeletevalue
Root: HKLM; Subkey: "SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_hu-HU_Szabolcs\Attributes"; ValueType: string; ValueName: "Gender"; ValueData: "Male"; Flags: uninsdeletevalue
Root: HKLM; Subkey: "SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_hu-HU_Szabolcs\Attributes"; ValueType: string; ValueName: "Language"; ValueData: "40E"; Flags: uninsdeletevalue
Root: HKLM; Subkey: "SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_hu-HU_Szabolcs\Attributes"; ValueType: string; ValueName: "Name"; ValueData: "Microsoft Szabolcs"; Flags: uninsdeletevalue
Root: HKLM; Subkey: "SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_hu-HU_Szabolcs\Attributes"; ValueType: string; ValueName: "SayAsSupport"; ValueData: "spell=NativeSupported; alphanumeric=NativeSupported"; Flags: uninsdeletevalue
Root: HKLM; Subkey: "SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_hu-HU_Szabolcs\Attributes"; ValueType: string; ValueName: "SharedPronunciation"; ValueData: ""; Flags: uninsdeletevalue
Root: HKLM; Subkey: "SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_hu-HU_Szabolcs\Attributes"; ValueType: string; ValueName: "Vendor"; ValueData: "Microsoft"; Flags: uninsdeletevalue
Root: HKLM; Subkey: "SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_hu-HU_Szabolcs\Attributes"; ValueType: string; ValueName: "Version"; ValueData: "11.0"; Flags: uninsdeletevalue

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: files; Name: "{%TEMP}\book_keeper\preview.wav"
Type: files; Name: "{%TEMP}\book_keeper\speech_preview.wav"


; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{4020619C-F961-4B3A-82CE-CF378B2F2D51}}
AppName=RadPy
AppVersion=0.1
AppPublisher=RadPy
AppPublisherURL=http://www.radpy.org/
AppCopyright=Copyright (C) 2009-2011 Radpy contributors
DefaultDirName={pf}\RadPy
DefaultGroupName=RadPy
AllowNoIcons=yes
OutputBaseFilename=setup
Compression=lzma
SolidCompression=yes
VersionInfoVersion = 0.1
LicenseFile=license.txt

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\*"; DestDir: "{app}\dist"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "Scripts\*"; DestDir: "{app}\Scripts"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "license.txt"; DestDir: "{app}"; Flags: ignoreversion

[Dirs]
Name: "{app}\Data\"
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\RadPy"; Filename: "{app}\dist\RadPy.exe"; IconFilename: "{app}\dist\RadPy.ico"
Name: "{group}\{cm:UninstallProgram,RadPy}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\RadPy"; Filename: "{app}\dist\RadPy.exe"; Tasks: desktopicon; IconFilename: "{app}\dist\RadPy.ico"

;[Run]
;Filename: "{app}\dist\RadPy.exe"; Description: "{cm:LaunchProgram,RadPy}"; Flags: nowait postinstall skipifsilent

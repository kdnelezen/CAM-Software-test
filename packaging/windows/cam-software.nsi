; NSIS test installer for CAM Software Test.
; Expected packaged app artifacts: dist\CAMSoftware\cam-software.exe plus PyInstaller support files.

!define APP_NAME "CAM Software Test"
!define APP_VERSION "0.1.0"
!define APP_PUBLISHER "kdnelezen"
!define APP_EXE "cam-software.exe"
!define APP_DIR "dist\\CAMSoftware"
!define OUT_DIR "build\\windows\\nsis"

Name "${APP_NAME}"
OutFile "${OUT_DIR}\\CAMSoftwareSetup-NSIS.exe"
InstallDir "$PROGRAMFILES\\${APP_NAME}"
InstallDirRegKey HKCU "Software\\${APP_NAME}" "InstallDir"
RequestExecutionLevel admin
Unicode True

Page directory
Page instfiles
UninstPage uninstConfirm
UninstPage instfiles

Section "Install"
  SetOutPath "$INSTDIR"
  File /r "${APP_DIR}\\*"
  WriteRegStr HKCU "Software\\${APP_NAME}" "InstallDir" "$INSTDIR"
  WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APP_NAME}" "DisplayName" "${APP_NAME}"
  WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APP_NAME}" "Publisher" "${APP_PUBLISHER}"
  WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APP_NAME}" "DisplayVersion" "${APP_VERSION}"
  WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APP_NAME}" "UninstallString" '"$INSTDIR\\Uninstall.exe"'
  WriteUninstaller "$INSTDIR\\Uninstall.exe"
  CreateDirectory "$SMPROGRAMS\\${APP_NAME}"
  CreateShortcut "$SMPROGRAMS\\${APP_NAME}\\${APP_NAME}.lnk" "$INSTDIR\\${APP_EXE}"
  CreateShortcut "$DESKTOP\\${APP_NAME}.lnk" "$INSTDIR\\${APP_EXE}"
SectionEnd

Section "Uninstall"
  Delete "$DESKTOP\\${APP_NAME}.lnk"
  Delete "$SMPROGRAMS\\${APP_NAME}\\${APP_NAME}.lnk"
  RMDir "$SMPROGRAMS\\${APP_NAME}"
  Delete "$INSTDIR\\Uninstall.exe"
  RMDir /r "$INSTDIR"
  DeleteRegKey HKCU "Software\\${APP_NAME}"
  DeleteRegKey HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APP_NAME}"
SectionEnd

# Packaging CAM Software Test

These packaging assets are intended for **test installers only**. Code-signing, notarization, and store submission are explicitly out of scope for now.

## Prerequisites

### Common
- Python 3.12+
- Linux desktop packaging requires `python3-tk` (or the platform equivalent Tk bindings)
- `pip install -r requirements.txt pyinstaller`
- Run commands from the repository root

### Windows option A: Inno Setup
- Inno Setup 6 (`ISCC.exe`) available in `C:\Program Files (x86)\Inno Setup 6\`

### Windows option B: NSIS
- NSIS (`makensis.exe`) available in `C:\Program Files (x86)\NSIS\`

### Linux option A: Flatpak
- `flatpak` and `flatpak-builder`
- Freedesktop runtime/sdk `23.08`

### Linux option B: AppImage
- `appimagetool`
- `squashfs-tools`

## Local build commands

### 1. Build the packaged app with PyInstaller

```bash
python scripts/build_pyinstaller.py --clean
```

This produces a one-folder application in `dist/CAMSoftware/`.

### 2A. Windows test installer with Inno Setup

```powershell
python scripts/build_pyinstaller.py --clean
./scripts/build_inno.ps1
```

Artifact: `build/windows/inno/CAMSoftwareSetup.exe`

### 2B. Windows test installer with NSIS

```powershell
python scripts/build_pyinstaller.py --clean
./scripts/build_nsis.ps1
```

Artifact: `build/windows/nsis/CAMSoftwareSetup-NSIS.exe`

### 3A. Linux Flatpak bundle

```bash
python scripts/build_pyinstaller.py --clean
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
flatpak install -y flathub org.freedesktop.Platform//23.08 org.freedesktop.Sdk//23.08
bash scripts/build_flatpak.sh
```

Artifact: `build/CAMSoftware.flatpak`

Install/test locally:

```bash
flatpak install --user --bundle build/CAMSoftware.flatpak
flatpak run io.github.kdnelezen.CAMSoftware
```

### 3B. Linux AppImage

```bash
python scripts/build_pyinstaller.py --clean
APPIMAGETOOL=/path/to/appimagetool bash scripts/build_appimage.sh
```

Artifact: `build/CAMSoftware-x86_64.AppImage`

Run/test locally:

```bash
chmod +x build/CAMSoftware-x86_64.AppImage
./build/CAMSoftware-x86_64.AppImage
```

## Artifact layout

- `dist/CAMSoftware/` — PyInstaller output used by all installers
- `build/windows/inno/` — Inno Setup installer output
- `build/windows/nsis/` — NSIS installer output
- `build/CAMSoftware.flatpak` — Flatpak bundle
- `build/CAMSoftware-x86_64.AppImage` — AppImage bundle

## Troubleshooting

- If PyInstaller fails to import project modules, run from the repository root and ensure dependencies from `requirements.txt` are installed.
- If the desktop UI cannot start in a shell session, use `cam-cli` or launch the packaged app from a graphical desktop session.
- Flatpak builds require the Freedesktop runtime and SDK version declared in `packaging/flatpak/io.github.kdnelezen.CAMSoftware.yml`.
- AppImage creation requires `appimagetool`; set `APPIMAGETOOL` if it is not on `PATH`.
- Windows installer scripts expect the PyInstaller build to exist first and intentionally target `Program Files` for installation.

# CAM-Software-test

Testing CAM software development.

## CAM Software Build Test

Starter repository for a CAM software project that imports 3D CAD files, generates machining toolpaths, and outputs controller-ready G-code.

## Goal

Build a CAM application that can:
- Import 3D CAD geometry
- Define stock, tools, and machine setup
- Generate toolpaths for common milling operations
- Simulate operations before export
- Post-process into G-code for selected CNC controllers

## MVP Scope

The first version should support:
- Single 3D CAD input format
- 3-axis milling
- Basic operations:
  - facing
  - pocketing
  - profiling
  - drilling
  - simple finishing passes
- One G-code post-processor
- Basic toolpath preview or backplot

## Current Implementation

This repository includes a modular Python CAM pipeline under `src/cam` that supports:

- CAD parsing for STL (ASCII + binary) and OBJ
- Extensible parser registry for future formats (DXF/STEP/etc.)
- Geometry analysis and mesh validation
- Roughing, finishing, and adaptive toolpath generation
- Machine profiles:
  - 2-axis mill
  - 3-axis mill
  - 4-axis mill
  - 2-axis lathe
- G-code generation with tool change, spindle, feed, and export support
- API + CLI workflow for file selection, machine selection, and parameter configuration
- A minimal Tkinter desktop launcher for packaging and installer testing

## Quick start

### CLI

```bash
python -m src.cam.cli input.stl output.nc --machine 3_axis_mill --tool-number 2 --tool-diameter 8.0
```

### Desktop entrypoint

```bash
PYTHONPATH=src python -m cam
```

## Testing installers

These are **test installers only**. Code-signing, notarization, and store-ready distribution are intentionally out of scope for now.

### Shared app build

```bash
pip install -r requirements.txt pyinstaller
# Linux desktop packaging also needs python3-tk installed
python scripts/build_pyinstaller.py --clean
```

PyInstaller outputs a reproducible one-folder app in `dist/CAMSoftware/`.

### Option A

#### Windows: Inno Setup

```powershell
python scripts/build_pyinstaller.py --clean
./scripts/build_inno.ps1
```

Result: `build/windows/inno/CAMSoftwareSetup.exe`

#### Linux: Flatpak

```bash
python scripts/build_pyinstaller.py --clean
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
flatpak install -y flathub org.freedesktop.Platform//23.08 org.freedesktop.Sdk//23.08
bash scripts/build_flatpak.sh
```

Result: `build/CAMSoftware.flatpak`

### Option B

#### Windows: NSIS

```powershell
python scripts/build_pyinstaller.py --clean
./scripts/build_nsis.ps1
```

Result: `build/windows/nsis/CAMSoftwareSetup-NSIS.exe`

#### Linux: AppImage

```bash
python scripts/build_pyinstaller.py --clean
APPIMAGETOOL=/path/to/appimagetool bash scripts/build_appimage.sh
```

Result: `build/CAMSoftware-x86_64.AppImage`

### CI artifacts

GitHub Actions now includes a `Build test installers` workflow that runs on push and manual dispatch, builds:
- Windows PyInstaller output + Inno Setup installer + NSIS installer
- Linux PyInstaller output + Flatpak bundle + AppImage

and uploads the generated artifacts for installation testing.

See `docs/packaging.md` for prerequisites, troubleshooting, and local testing steps.

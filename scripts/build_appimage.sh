#!/usr/bin/env bash
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
APPDIR="$REPO_ROOT/AppDir"
DIST_DIR="$REPO_ROOT/dist/CAMSoftware"
APPIMAGETOOL_BIN="${APPIMAGETOOL:-appimagetool}"
if [[ ! -x "$DIST_DIR/cam-software" ]]; then
  echo "PyInstaller output not found at $DIST_DIR/cam-software. Run python scripts/build_pyinstaller.py first." >&2
  exit 1
fi
if ! command -v "$APPIMAGETOOL_BIN" >/dev/null 2>&1; then
  echo "appimagetool not found. Install it or set APPIMAGETOOL=/path/to/appimagetool." >&2
  exit 1
fi
rm -rf "$APPDIR"
mkdir -p "$APPDIR/usr/bin" "$APPDIR/usr/lib/cam-software"
cp -r "$DIST_DIR"/* "$APPDIR/usr/lib/cam-software/"
cp "$REPO_ROOT/packaging/appimage/AppRun" "$APPDIR/AppRun"
cat > "$APPDIR/usr/bin/cam-software" <<'WRAPPER'
#!/usr/bin/env sh
set -eu
APPDIR="$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)"
exec "$APPDIR/usr/lib/cam-software/cam-software" "$@"
WRAPPER
chmod +x "$APPDIR/usr/bin/cam-software" "$APPDIR/AppRun"
cp "$REPO_ROOT/packaging/linux/cam-software.desktop" "$APPDIR/cam-software.desktop"
cp "$REPO_ROOT/packaging/linux/icons/cam-software.svg" "$APPDIR/io.github.kdnelezen.CAMSoftware.svg"
"$APPIMAGETOOL_BIN" "$APPDIR" "$REPO_ROOT/build/CAMSoftware-x86_64.AppImage"

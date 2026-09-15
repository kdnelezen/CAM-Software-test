#!/usr/bin/env bash
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MANIFEST="$REPO_ROOT/packaging/flatpak/io.github.kdnelezen.CAMSoftware.yml"
ARTIFACT="$REPO_ROOT/dist/CAMSoftware/cam-software"
if [[ ! -x "$ARTIFACT" ]]; then
  echo "PyInstaller output not found at $ARTIFACT. Run python scripts/build_pyinstaller.py first." >&2
  exit 1
fi
flatpak-builder --force-clean --repo="$REPO_ROOT/build/flatpak-repo" "$REPO_ROOT/build/flatpak-workdir" "$MANIFEST"
flatpak build-bundle "$REPO_ROOT/build/flatpak-repo" "$REPO_ROOT/build/CAMSoftware.flatpak" io.github.kdnelezen.CAMSoftware stable

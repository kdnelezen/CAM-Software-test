from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the CAM Software desktop app with PyInstaller.")
    parser.add_argument("--clean", action="store_true", help="Remove previous build and dist directories before building.")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    if args.clean:
        for dirname in ("build", "dist"):
            target = repo_root / dirname
            if target.exists():
                shutil.rmtree(target)

    subprocess.run(
        [
            sys.executable,
            "-m",
            "PyInstaller",
            "--clean",
            "--noconfirm",
            str(repo_root / "packaging" / "pyinstaller" / "cam_software.spec"),
        ],
        check=True,
        cwd=repo_root,
    )


if __name__ == "__main__":
    main()

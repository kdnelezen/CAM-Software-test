$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
$installerScript = Join-Path $repoRoot 'packaging\windows\cam-software.iss'
$artifact = Join-Path $repoRoot 'dist\CAMSoftware\cam-software.exe'
if (-not (Test-Path $artifact)) {
    throw "PyInstaller output not found at $artifact. Run python scripts/build_pyinstaller.py first."
}
$compiler = Join-Path ${env:ProgramFiles(x86)} 'Inno Setup 6\ISCC.exe'
if (-not (Test-Path $compiler)) {
    throw 'Inno Setup compiler not found. Install Inno Setup 6 or run the GitHub Actions workflow.'
}
& $compiler $installerScript

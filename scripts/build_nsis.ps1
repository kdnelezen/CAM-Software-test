$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
$installerScript = Join-Path $repoRoot 'packaging\windows\cam-software.nsi'
$artifact = Join-Path $repoRoot 'dist\CAMSoftware\cam-software.exe'
if (-not (Test-Path $artifact)) {
    throw "PyInstaller output not found at $artifact. Run python scripts/build_pyinstaller.py first."
}
$compiler = Join-Path ${env:ProgramFiles(x86)} 'NSIS\makensis.exe'
if (-not (Test-Path $compiler)) {
    throw 'NSIS compiler not found. Install NSIS or run the GitHub Actions workflow.'
}
& $compiler $installerScript

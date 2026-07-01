param(
    [string]$PythonExe = "python",
    [switch]$OneFile
)

$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$MainScript = Join-Path $ProjectRoot "kymograph_force_distance_ui.py"
$IconPath = Join-Path $ProjectRoot "assets\otplot_icon.ico"
$VersionFile = Join-Path $ProjectRoot "version_info.txt"
$EnvRoot = Split-Path -Parent $PythonExe
$LibraryBin = Join-Path $EnvRoot "Library\bin"
$RuntimeDlls = @(
    "tcl86t.dll",
    "tk86t.dll",
    "libssl-3-x64.dll",
    "libcrypto-3-x64.dll",
    "sqlite3.dll",
    "ffi.dll",
    "liblzma.dll",
    "libbz2.dll"
)

if (-not (Test-Path $MainScript)) {
    throw "Main script not found: $MainScript"
}

if (-not (Test-Path $IconPath)) {
    throw "Icon file not found: $IconPath"
}

if (-not (Test-Path $VersionFile)) {
    throw "Version file not found: $VersionFile"
}

$distMode = if ($OneFile) { "--onefile" } else { "--onedir" }
$PyInstallerArgs = @(
    "-m", "PyInstaller",
    "--noconfirm",
    "--clean",
    "--windowed",
    $distMode,
    "--name", "OTPlotViewer",
    "--icon", $IconPath,
    "--version-file", $VersionFile,
    "--collect-submodules", "lumicks.pylake",
    "--collect-data", "lumicks.pylake",
    "--collect-submodules", "openpyxl",
    "--hidden-import", "openpyxl",
    "--hidden-import", "tkinter"
)

if (Test-Path $LibraryBin) {
    foreach ($dllName in $RuntimeDlls) {
        $dllPath = Join-Path $LibraryBin $dllName
        if (Test-Path $dllPath) {
            $PyInstallerArgs += "--add-binary"
            $PyInstallerArgs += "$dllPath;."
        } else {
            Write-Warning "Optional conda runtime DLL not found, skipping: $dllPath"
        }
    }
} else {
    Write-Host "Conda runtime directory not found, skipping explicit conda DLL additions: $LibraryBin"
}

$PyInstallerArgs += $MainScript

& $PythonExe -m pip install -r (Join-Path $ProjectRoot "requirements-packaging.txt")
& $PythonExe @PyInstallerArgs

Write-Host "Build finished. Output folder:" (Join-Path $ProjectRoot "dist")

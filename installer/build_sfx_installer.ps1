param(
    [string]$Version = "v1.0.2",
    [string]$OutputDir = "D:\chenlishuang_files\software_dp\OT_plot_backups\OT_plot_backup_20260428_215955\release"
)

$ErrorActionPreference = "Stop"

$SevenZipDir = "C:\Program Files\7-Zip"
$SevenZip = Join-Path $SevenZipDir "7z.exe"
$SevenZipDll = Join-Path $SevenZipDir "7z.dll"
$SfxModule = Join-Path $SevenZipDir "7z.sfx"

foreach ($path in @($SevenZip, $SevenZipDll, $SfxModule)) {
    if (-not (Test-Path -LiteralPath $path)) {
        throw "Required 7-Zip file not found: $path"
    }
}

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$InstallScript = Join-Path $ScriptDir "install_otplotviewer.ps1"
if (-not (Test-Path -LiteralPath $InstallScript)) {
    throw "Installer script not found: $InstallScript"
}

New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
$BuildDir = Join-Path $OutputDir "installer_sfx_build"
$PayloadDir = Join-Path $BuildDir "payload"
Remove-Item -LiteralPath $BuildDir -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path $PayloadDir -Force | Out-Null

Copy-Item -LiteralPath $InstallScript -Destination (Join-Path $PayloadDir "install.ps1") -Force
Copy-Item -LiteralPath $SevenZip -Destination (Join-Path $PayloadDir "7z.exe") -Force
Copy-Item -LiteralPath $SevenZipDll -Destination (Join-Path $PayloadDir "7z.dll") -Force

$PayloadArchive = Join-Path $BuildDir "payload.7z"
& $SevenZip a -t7z -mx=9 $PayloadArchive (Join-Path $PayloadDir "*") | Out-Host
if ($LASTEXITCODE -ne 0) {
    throw "7-Zip payload build failed with exit code $LASTEXITCODE."
}

$ConfigPath = Join-Path $BuildDir "sfx_config.txt"
@"
;!@Install@!UTF-8!
Title="OTPlotViewer Setup $Version"
BeginPrompt="Install OTPlotViewer $Version? The installer will download the application package from GitHub."
RunProgram="powershell.exe -NoProfile -ExecutionPolicy Bypass -File install.ps1"
;!@InstallEnd@!
"@ | Set-Content -LiteralPath $ConfigPath -Encoding UTF8

$VersionText = $Version.TrimStart("v")
$OutputExe = Join-Path $OutputDir "OTPlotViewer_Setup_$VersionText.exe"
if (Test-Path -LiteralPath $OutputExe) {
    Remove-Item -LiteralPath $OutputExe -Force
}

$outStream = [System.IO.File]::Create($OutputExe)
try {
    foreach ($part in @($SfxModule, $ConfigPath, $PayloadArchive)) {
        $bytes = [System.IO.File]::ReadAllBytes($part)
        $outStream.Write($bytes, 0, $bytes.Length)
    }
} finally {
    $outStream.Close()
}

Remove-Item -LiteralPath $BuildDir -Recurse -Force -ErrorAction SilentlyContinue
Get-Item -LiteralPath $OutputExe

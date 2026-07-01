param(
    [Parameter(Mandatory = $true)]
    [string]$Tag,

    [string]$ProjectRoot = (Split-Path -Parent $PSScriptRoot),
    [string]$OutputDir = (Join-Path (Split-Path -Parent $PSScriptRoot) "release")
)

$ErrorActionPreference = "Stop"

if ($Tag -notmatch '^v\d+\.\d+\.\d+$') {
    throw "Tag must look like v1.2.3. Got: $Tag"
}

$SevenZip = "C:\Program Files\7-Zip\7z.exe"
if (-not (Test-Path -LiteralPath $SevenZip)) {
    $SevenZip = "7z.exe"
}

$DistDir = Join-Path $ProjectRoot "dist"
$AppDir = Join-Path $DistDir "OTPlotViewer"
if (-not (Test-Path -LiteralPath (Join-Path $AppDir "OTPlotViewer.exe"))) {
    throw "Packaged application not found. Run build_windows.ps1 first: $AppDir"
}

New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null

$readme = @"
OTPlotViewer $($Tag.TrimStart("v")) for Windows

How to use:
1. Extract this archive first.
2. Open the OTPlotViewer folder.
3. Double-click OTPlotViewer.exe.

Important:
- Do not move OTPlotViewer.exe out of the OTPlotViewer folder.
- Keep the _internal folder next to OTPlotViewer.exe.
- This packaged version does not require Python, conda, or manual dependency installation.
"@
$ReadmePath = Join-Path $DistDir "README.txt"
Set-Content -LiteralPath $ReadmePath -Value $readme -Encoding UTF8

$zip = Join-Path $OutputDir ("OTPlotViewer_{0}_windows_folder.zip" -f $Tag)
$split = Join-Path $OutputDir ("OTPlotViewer_{0}_windows_folder_split.7z" -f $Tag)
Remove-Item -LiteralPath $zip -Force -ErrorAction SilentlyContinue
Remove-Item -LiteralPath "$split.*" -Force -ErrorAction SilentlyContinue

Push-Location $DistDir
try {
    & $SevenZip a -tzip -mx=5 $zip ".\README.txt" ".\OTPlotViewer"
    if ($LASTEXITCODE -ne 0) { throw "7-Zip zip build failed with exit code $LASTEXITCODE." }

    & $SevenZip a -t7z -mx=9 -v20m $split ".\OTPlotViewer"
    if ($LASTEXITCODE -ne 0) { throw "7-Zip split archive build failed with exit code $LASTEXITCODE." }
} finally {
    Pop-Location
}

Get-ChildItem -LiteralPath $OutputDir -Filter ("OTPlotViewer_{0}_windows_folder*" -f $Tag)

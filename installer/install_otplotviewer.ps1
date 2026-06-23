param(
    [string]$InstallDir = "",
    [switch]$NoLaunch
)

$ErrorActionPreference = "Stop"

$Version = "v1.0.1"
$Repo = "Dorlores199/OTPlotViewer"
$AssetPrefix = "OTPlotViewer_v1.0.1_windows_folder_split.7z"
$BaseUrl = "https://github.com/$Repo/releases/download/$Version"
$PartNames = @(
    "$AssetPrefix.001",
    "$AssetPrefix.002",
    "$AssetPrefix.003",
    "$AssetPrefix.004"
)

if (-not $InstallDir) {
    $InstallDir = Join-Path $env:LOCALAPPDATA "Programs\OTPlotViewer"
}

[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$SevenZip = Join-Path $ScriptRoot "7z.exe"
if (-not (Test-Path -LiteralPath $SevenZip)) {
    throw "Bundled 7z.exe was not found next to the installer script."
}

$WorkDir = Join-Path ([System.IO.Path]::GetTempPath()) ("OTPlotViewerInstall_" + [guid]::NewGuid().ToString("N"))
$DownloadDir = Join-Path $WorkDir "downloads"
$ExtractDir = Join-Path $WorkDir "extract"
New-Item -ItemType Directory -Path $DownloadDir, $ExtractDir -Force | Out-Null

function Download-File {
    param(
        [string]$Url,
        [string]$OutFile
    )
    $maxAttempts = 4
    for ($attempt = 1; $attempt -le $maxAttempts; $attempt++) {
        Write-Host "Downloading $Url (attempt $attempt/$maxAttempts)"
        Remove-Item -LiteralPath $OutFile -Force -ErrorAction SilentlyContinue

        try {
            Start-BitsTransfer -Source $Url -Destination $OutFile -ErrorAction Stop
            if (Test-Path -LiteralPath $OutFile) { return }
        } catch {
            Write-Host "BITS download failed: $($_.Exception.Message)"
        }

        try {
            Invoke-WebRequest -Uri $Url -OutFile $OutFile -UseBasicParsing -ErrorAction Stop
            if (Test-Path -LiteralPath $OutFile) { return }
        } catch {
            Write-Host "PowerShell download failed: $($_.Exception.Message)"
        }

        $curl = Get-Command curl.exe -ErrorAction SilentlyContinue
        if ($curl) {
            try {
                & $curl.Source -L --retry 5 --retry-delay 2 --fail --output $OutFile $Url
                if ($LASTEXITCODE -eq 0 -and (Test-Path -LiteralPath $OutFile)) { return }
                Write-Host "curl download failed with exit code $LASTEXITCODE"
            } catch {
                Write-Host "curl download failed: $($_.Exception.Message)"
            }
        }

        Start-Sleep -Seconds ([Math]::Min(3 * $attempt, 12))
    }
    throw "Failed to download $Url after $maxAttempts attempts."
}

try {
    foreach ($name in $PartNames) {
        Download-File -Url "$BaseUrl/$name" -OutFile (Join-Path $DownloadDir $name)
    }

    $firstPart = Join-Path $DownloadDir $PartNames[0]
    & $SevenZip x $firstPart "-o$ExtractDir" -y | Out-Host
    if ($LASTEXITCODE -ne 0) {
        throw "7-Zip extraction failed with exit code $LASTEXITCODE."
    }

    $ExtractedAppDir = Join-Path $ExtractDir "OTPlotViewer"
    if (-not (Test-Path -LiteralPath (Join-Path $ExtractedAppDir "OTPlotViewer.exe"))) {
        throw "Extracted application folder is incomplete."
    }

    if (Test-Path -LiteralPath $InstallDir) {
        Remove-Item -LiteralPath $InstallDir -Recurse -Force
    }
    New-Item -ItemType Directory -Path (Split-Path -Parent $InstallDir) -Force | Out-Null
    Copy-Item -LiteralPath $ExtractedAppDir -Destination $InstallDir -Recurse -Force

    $ExePath = Join-Path $InstallDir "OTPlotViewer.exe"
    $StartMenuDir = Join-Path $env:APPDATA "Microsoft\Windows\Start Menu\Programs\OTPlotViewer"
    New-Item -ItemType Directory -Path $StartMenuDir -Force | Out-Null

    $UninstallScript = Join-Path $InstallDir "uninstall_otplotviewer.ps1"
    @"
`$ErrorActionPreference = "SilentlyContinue"
Remove-Item -LiteralPath "$StartMenuDir" -Recurse -Force
Remove-Item -LiteralPath "$([Environment]::GetFolderPath("Desktop"))\OTPlotViewer.lnk" -Force
Remove-Item -LiteralPath "$InstallDir" -Recurse -Force
Write-Host "OTPlotViewer has been uninstalled."
"@ | Set-Content -LiteralPath $UninstallScript -Encoding UTF8

    $Shell = New-Object -ComObject WScript.Shell

    $DesktopShortcut = Join-Path ([Environment]::GetFolderPath("Desktop")) "OTPlotViewer.lnk"
    $Shortcut = $Shell.CreateShortcut($DesktopShortcut)
    $Shortcut.TargetPath = $ExePath
    $Shortcut.WorkingDirectory = $InstallDir
    $Shortcut.IconLocation = $ExePath
    $Shortcut.Save()

    $StartShortcut = Join-Path $StartMenuDir "OTPlotViewer.lnk"
    $Shortcut = $Shell.CreateShortcut($StartShortcut)
    $Shortcut.TargetPath = $ExePath
    $Shortcut.WorkingDirectory = $InstallDir
    $Shortcut.IconLocation = $ExePath
    $Shortcut.Save()

    $UninstallShortcut = Join-Path $StartMenuDir "Uninstall OTPlotViewer.lnk"
    $Shortcut = $Shell.CreateShortcut($UninstallShortcut)
    $Shortcut.TargetPath = "powershell.exe"
    $Shortcut.Arguments = "-NoProfile -ExecutionPolicy Bypass -File `"$UninstallScript`""
    $Shortcut.WorkingDirectory = $InstallDir
    $Shortcut.Save()

    Write-Host ""
    Write-Host "OTPlotViewer $Version was installed to:"
    Write-Host $InstallDir

    if (-not $NoLaunch) {
        Start-Process -FilePath $ExePath -WorkingDirectory $InstallDir
    }
} finally {
    Remove-Item -LiteralPath $WorkDir -Recurse -Force -ErrorAction SilentlyContinue
}

param(
    [Parameter(Mandatory = $true)]
    [string]$Tag
)

$ErrorActionPreference = "Stop"

if ($Tag -notmatch '^v\d+\.\d+\.\d+$') {
    throw "Release tag must look like v1.2.3. Got: $Tag"
}

$Version = $Tag.TrimStart("v")
$Root = Split-Path -Parent $PSScriptRoot
$Files = @{
    Readme = Join-Path $Root "README.md"
    Citation = Join-Path $Root "CITATION.cff"
    VersionInfo = Join-Path $Root "version_info.txt"
    ReleaseNotes = Join-Path $Root ("docs\release_{0}.md" -f $Tag)
}

foreach ($path in $Files.Values) {
    if (-not (Test-Path -LiteralPath $path)) {
        throw "Required release metadata file is missing: $path"
    }
}

$readme = Get-Content -LiteralPath $Files.Readme -Raw -Encoding UTF8
$citation = Get-Content -LiteralPath $Files.Citation -Raw -Encoding UTF8
$versionInfo = Get-Content -LiteralPath $Files.VersionInfo -Raw -Encoding UTF8
$releaseNotes = Get-Content -LiteralPath $Files.ReleaseNotes -Raw -Encoding UTF8

if ($readme -notmatch [regex]::Escape($Tag)) {
    throw "README.md does not mention $Tag. Update the download/citation links before tagging."
}

if ($citation -notmatch ('version:\s*"{0}"' -f [regex]::Escape($Version))) {
    throw "CITATION.cff version is not $Version."
}

$tuple = ($Version.Split(".") + @("0")) -join ", "
if ($versionInfo -notmatch [regex]::Escape($tuple)) {
    throw "version_info.txt does not contain file/product version tuple ($tuple)."
}

if ($releaseNotes.Trim().Length -lt 80) {
    throw "Release notes for $Tag look too short: $($Files.ReleaseNotes)"
}

Write-Host "Release metadata is consistent for $Tag."

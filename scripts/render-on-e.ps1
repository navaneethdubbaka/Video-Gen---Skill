#Requires -Version 5.1
<#
.SYNOPSIS
  Render a HyperFrames composition using ONLY the E: drive for TEMP (not C:).

.EXAMPLE
  .\scripts\render-on-e.ps1 `
    -ProjectDir "E:\Video Gen Skill\videos\llm-series-ep3\composition\hyperframes" `
    -Out "E:\Video Gen Skill\videos\llm-series-ep3\renders\draft\out.mp4"
#>
param(
  [Parameter(Mandatory = $true)]
  [string]$ProjectDir,

  [Parameter(Mandatory = $true)]
  [string]$Out,

  [int]$Workers = 1,

  [string]$WorkspaceRoot = "E:\Video Gen Skill"
)

$ErrorActionPreference = "Stop"

if (-not $Out.StartsWith("E:\", [StringComparison]::OrdinalIgnoreCase)) {
  throw "Output must be on E: drive. Got: $Out"
}
if (-not $ProjectDir.StartsWith("E:\", [StringComparison]::OrdinalIgnoreCase)) {
  throw "ProjectDir must be on E: drive. Got: $ProjectDir"
}

$tmpRoot = Join-Path $WorkspaceRoot ".tmp"
$hfTemp = Join-Path $tmpRoot "hf-render"
$framesCache = Join-Path $tmpRoot "hyperframes-extract-cache"
New-Item -ItemType Directory -Force -Path $hfTemp, $framesCache | Out-Null

# Keep HyperFrames / ffmpeg scratch OFF C:. Do NOT redirect npm cache (causes ECOMPROMISED locks).
$env:TEMP = $hfTemp
$env:TMP = $hfTemp
$env:TMPDIR = $hfTemp
$env:HYPERFRAMES_EXTRACT_CACHE_DIR = $framesCache

Write-Host "TEMP=$env:TEMP (E: only)"
Write-Host "HYPERFRAMES_EXTRACT_CACHE_DIR=$env:HYPERFRAMES_EXTRACT_CACHE_DIR"
Write-Host "ProjectDir=$ProjectDir"
Write-Host "Out=$Out"
Write-Host "Workers=$Workers"

Push-Location $ProjectDir
try {
  npx --yes hyperframes@0.8.160 render --workers $Workers --frames-cache-dir $framesCache -o $Out
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
finally {
  Pop-Location
}

Write-Host "DONE $Out"

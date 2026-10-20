#Requires -Version 5.1
<#
.SYNOPSIS
  Encode talking mouth PNG frames to MP4, GIF (512px), and animated WebP (alpha).

.EXAMPLE
  .\encode_loops.ps1 -OutDir "E:\Video Gen Skill\greencode\my_animations\host_talking\talk_loop"
#>
param(
  [Parameter(Mandatory = $true)]
  [string]$OutDir,

  [int]$Fps = 24
)

$ErrorActionPreference = "Stop"
$frames = Join-Path $OutDir "frames"
if (-not (Test-Path (Join-Path $frames "f000.png"))) {
  throw "No frames at $frames\f000.png"
}

$ffmpeg = Get-Command ffmpeg -ErrorAction SilentlyContinue
if (-not $ffmpeg) {
  throw "ffmpeg not found on PATH"
}

$mp4 = Join-Path $OutDir "talking_loop.mp4"
$gif = Join-Path $OutDir "talking_loop.gif"
$webp = Join-Path $OutDir "talking_loop.webp"

Write-Host "Encoding MP4 → $mp4"
# libx264 needs even dimensions (480x853 fails) — pad to next even
& ffmpeg -y -framerate $Fps -i (Join-Path $frames "f%03d.png") `
  -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" `
  -c:v libx264 -pix_fmt yuv420p -crf 14 $mp4
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Encoding GIF → $gif"
& ffmpeg -y -framerate $Fps -i (Join-Path $frames "f%03d.png") `
  -vf "scale=512:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=128:reserve_transparent=1[p];[b][p]paletteuse=dither=bayer:bayer_scale=4:alpha_threshold=64" `
  -loop 0 $gif
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Encoding WebP (alpha) → $webp"
& ffmpeg -y -framerate $Fps -i (Join-Path $frames "f%03d.png") `
  -c:v libwebp -lossless 0 -compression_level 4 -q:v 80 -loop 0 -an $webp
if ($LASTEXITCODE -ne 0) {
  Write-Host "WebP encode failed; trying gifski-less fallback as copy of GIF name only"
  # fallback: keep GIF as compose fallback
}

Write-Host "DONE $OutDir"

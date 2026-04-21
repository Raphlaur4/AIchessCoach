<#
.SYNOPSIS
    Downloads the Stockfish 17.1 binary (Windows x86-64 AVX2) into bin/stockfish/.

.DESCRIPTION
    The binary is not committed to the repo. This script fetches it from the
    official Stockfish GitHub releases and extracts it to bin/stockfish/.
    bin/ is gitignored. Re-running the script is safe (it overwrites).
#>

$ErrorActionPreference = "Stop"

$Version = "17.1"
$Asset   = "stockfish-windows-x86-64-avx2"
$Url     = "https://github.com/official-stockfish/Stockfish/releases/download/sf_$Version/$Asset.zip"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$BinDir   = Join-Path $RepoRoot "bin"
$ZipPath  = Join-Path $BinDir "stockfish.zip"

Write-Host "Installing Stockfish $Version ($Asset)..."

New-Item -ItemType Directory -Path $BinDir -Force | Out-Null

Write-Host "Downloading $Url"
Invoke-WebRequest -Uri $Url -OutFile $ZipPath

Write-Host "Extracting to $BinDir"
Expand-Archive -Path $ZipPath -DestinationPath $BinDir -Force
Remove-Item $ZipPath

$Exe = Join-Path (Join-Path $BinDir "stockfish") "$Asset.exe"
if (-not (Test-Path $Exe)) {
    throw "Expected binary not found at $Exe after extraction."
}

Write-Host "Installed: $Exe"

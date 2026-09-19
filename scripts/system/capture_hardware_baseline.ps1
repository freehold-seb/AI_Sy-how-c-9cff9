param(
    [string]$OutputDirectory = "$env:LOCALAPPDATA\Kepler\hardware-evidence"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$directory = [System.IO.Path]::GetFullPath($OutputDirectory)
New-Item -ItemType Directory -Path $directory -Force | Out-Null
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$output = Join-Path $directory "hardware-baseline-$timestamp.txt"
$script = Join-Path $PSScriptRoot "hardware_baseline.ps1"

& $script | Tee-Object -FilePath $output
Write-Host "Evidence captured: $output"

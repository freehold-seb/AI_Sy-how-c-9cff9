# === Project-Rutabaga: Strict Document Archiver ===
# Wrapper around central cleanup_and_sort.ps1 to guarantee safety and no-touch zone adherence.

[CmdletBinding()]
param(
    [switch]$DryRun
)

& (Join-Path $PSScriptRoot "cleanup_and_sort.ps1") -OnlyDocuments -DryRun:$DryRun


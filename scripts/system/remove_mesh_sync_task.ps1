[CmdletBinding()]
param([string]$TaskName = "Project-Rutabaga_MeshSync")

$ErrorActionPreference = "Stop"
$task = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if (-not $task) {
    Write-Host "[mesh-sync] Task not installed: $TaskName"
    exit 0
}
Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
Write-Host "[mesh-sync] Removed $TaskName. Status history was preserved."

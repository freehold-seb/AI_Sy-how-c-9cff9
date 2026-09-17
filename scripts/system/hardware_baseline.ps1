Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Write-Host "=== Computer ==="
Get-CimInstance Win32_ComputerSystem |
    Select-Object Manufacturer, Model, TotalPhysicalMemory |
    Format-List

Write-Host "=== Memory ==="
Get-CimInstance Win32_PhysicalMemory |
    Select-Object Manufacturer, PartNumber, Capacity, Speed, ConfiguredClockSpeed |
    Format-Table -AutoSize

Write-Host "=== CPU ==="
Get-CimInstance Win32_Processor |
    Select-Object Name, MaxClockSpeed, CurrentClockSpeed |
    Format-List

Write-Host "=== Motherboard ==="
Get-CimInstance Win32_BaseBoard |
    Select-Object Manufacturer, Product |
    Format-List

Write-Host "=== BIOS ==="
Get-CimInstance Win32_BIOS |
    Select-Object SMBIOSBIOSVersion, ReleaseDate |
    Format-List

Write-Host "=== Present non-OK devices ==="
Get-PnpDevice -PresentOnly |
    Where-Object Status -NE "OK" |
    Select-Object Class, FriendlyName, Status, Problem, InstanceId |
    Format-List

Write-Host "=== WHEA events from last 24 hours ==="
$wheaEvents = @(
    Get-WinEvent -FilterHashtable @{
        LogName = "System"
        ProviderName = "Microsoft-Windows-WHEA-Logger"
        StartTime = (Get-Date).AddDays(-1)
    } -ErrorAction SilentlyContinue |
        Select-Object TimeCreated, Id, LevelDisplayName, Message
)

if ($wheaEvents.Count -eq 0) {
    Write-Host "No WHEA events found in the last 24 hours."
}
else {
    $wheaEvents | Format-List
}

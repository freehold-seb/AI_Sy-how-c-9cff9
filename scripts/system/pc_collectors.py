"""Allowlisted, read-only PowerShell collectors for PC assessment metadata."""

from __future__ import annotations

import json
import subprocess
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from typing import Any


POWERSHELL_COMMANDS: Mapping[str, str] = {
    "system": (
        "$os=Get-CimInstance Win32_OperatingSystem; "
        "$computer=Get-CimInstance Win32_ComputerSystem; "
        "$battery=Get-CimInstance Win32_Battery -ErrorAction SilentlyContinue; "
        "[pscustomobject]@{OperatingSystem=$os | "
        "Select-Object Caption,Version,BuildNumber,LastBootUpTime; "
        "Computer=$computer | Select-Object Manufacturer,Model,TotalPhysicalMemory; "
        "Battery=$battery | Select-Object BatteryStatus,EstimatedChargeRemaining} | "
        "ConvertTo-Json -Depth 4 -Compress"
    ),
    "updates": (
        "$since=(Get-Date).AddDays(-7); "
        "$hotfixes=@(Get-HotFix -ErrorAction SilentlyContinue | "
        "Where-Object InstalledOn -GE $since | "
        "Select-Object HotFixID,Description,InstalledOn); "
        "$failures=@(Get-WinEvent -FilterHashtable "
        "@{LogName='System';ProviderName='Microsoft-Windows-WindowsUpdateClient';"
        "StartTime=$since;Level=2,3} -MaxEvents 50 -ErrorAction SilentlyContinue | "
        "Select-Object TimeCreated,Id,LevelDisplayName); "
        "[pscustomobject]@{HotFixes=$hotfixes;Failures=$failures} | "
        "ConvertTo-Json -Depth 4 -Compress"
    ),
    "security": (
        "$defender=Get-MpComputerStatus -ErrorAction SilentlyContinue; "
        "$firewall=@(Get-NetFirewallProfile -ErrorAction SilentlyContinue | "
        "Select-Object Name,Enabled,DefaultInboundAction,DefaultOutboundAction); "
        "[pscustomobject]@{Defender=$defender | "
        "Select-Object AntivirusEnabled,AntispywareEnabled,RealTimeProtectionEnabled,"
        "BehaviorMonitorEnabled,AntivirusSignatureLastUpdated,QuickScanAge,FullScanAge; "
        "FirewallProfiles=$firewall} | ConvertTo-Json -Depth 4 -Compress"
    ),
    "drivers": (
        "$signed=@(Get-CimInstance Win32_PnPSignedDriver | "
        "Select-Object DeviceName,DeviceClass,DriverVersion,DriverDate,Manufacturer,IsSigned); "
        "$problems=@(Get-PnpDevice -PresentOnly -ErrorAction SilentlyContinue | "
        "Where-Object Status -NE 'OK' | Select-Object Class,FriendlyName,Status,Problem); "
        "[pscustomobject]@{SignedDrivers=$signed;ProblemDevices=$problems} | "
        "ConvertTo-Json -Depth 4 -Compress"
    ),
    "storage": (
        "$disks=@(Get-PhysicalDisk -ErrorAction SilentlyContinue | "
        "Select-Object FriendlyName,MediaType,BusType,HealthStatus,OperationalStatus,Size); "
        "$volumes=@(Get-Volume -ErrorAction SilentlyContinue | "
        "Where-Object DriveLetter | Select-Object DriveLetter,FileSystemLabel,FileSystem,"
        "DriveType,HealthStatus,OperationalStatus,Size,SizeRemaining); "
        "[pscustomobject]@{PhysicalDisks=$disks;Volumes=$volumes} | "
        "ConvertTo-Json -Depth 4 -Compress"
    ),
    "network": (
        "$adapters=@(Get-NetAdapter -ErrorAction SilentlyContinue | "
        "Select-Object Name,InterfaceDescription,Status,LinkSpeed); "
        "$profiles=@(Get-NetConnectionProfile -ErrorAction SilentlyContinue | "
        "Select-Object InterfaceAlias,NetworkCategory,IPv4Connectivity,IPv6Connectivity); "
        "$dns=@(Get-DnsClientServerAddress -AddressFamily IPv4 -ErrorAction SilentlyContinue | "
        "Where-Object ServerAddresses | Select-Object InterfaceAlias,ServerAddresses); "
        "$routes=@(Get-NetRoute -DestinationPrefix '0.0.0.0/0' -ErrorAction SilentlyContinue | "
        "Select-Object InterfaceAlias,NextHop,RouteMetric); "
        "$listeners=@(Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue | "
        "Select-Object -First 100 LocalAddress,LocalPort,OwningProcess); "
        "$proxy=netsh winhttp show proxy; "
        "[pscustomobject]@{Adapters=$adapters;Profiles=$profiles;Dns=$dns;"
        "DefaultRoutes=$routes;Listeners=$listeners;WinHttpProxy=$proxy} | "
        "ConvertTo-Json -Depth 5 -Compress"
    ),
    "software": (
        "Get-ItemProperty "
        "HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*,"
        "HKLM:\\Software\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*,"
        "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* "
        "-ErrorAction SilentlyContinue | "
        "Where-Object DisplayName | "
        "Select-Object DisplayName,DisplayVersion,Publisher,InstallDate | "
        "ConvertTo-Json -Compress"
    ),
    "startup": (
        "Get-CimInstance Win32_StartupCommand | "
        "Select-Object Name,Location,User | ConvertTo-Json -Compress"
    ),
    "developer": (
        "$tools=@(Get-Command git,py,python,node,npm,dotnet,java,code,winget "
        "-All -ErrorAction SilentlyContinue | Select-Object Name,Source,Version); "
        "$paths=@($env:Path -split ';' | Where-Object { $_ }); "
        "[pscustomobject]@{Tools=$tools;PathEntries=$paths} | "
        "ConvertTo-Json -Depth 4 -Compress"
    ),
    "reliability": (
        "$since=(Get-Date).AddDays(-7); "
        "$events=@(Get-WinEvent -FilterHashtable "
        "@{LogName='System';StartTime=$since;Level=1,2,3} -MaxEvents 100 "
        "-ErrorAction SilentlyContinue | Group-Object ProviderName,Id | "
        "Sort-Object Count -Descending | Select-Object -First 25 Count,Name); "
        "[pscustomobject]@{SystemWarningAndErrorGroups=$events} | "
        "ConvertTo-Json -Depth 4 -Compress"
    ),
}


@dataclass(frozen=True)
class CollectionResult:
    category: str
    status: str
    data: Any = None
    error: str | None = None


Executor = Callable[..., subprocess.CompletedProcess[str]]


def run_category(
    category: str,
    *,
    executor: Executor = subprocess.run,
    timeout_seconds: int = 30,
) -> CollectionResult:
    """Run one exact allowlisted command and parse its structured output."""
    if category not in POWERSHELL_COMMANDS:
        raise ValueError(f"Unsupported assessment category: {category}")

    command: Sequence[str] = (
        "powershell.exe",
        "-NoLogo",
        "-NoProfile",
        "-NonInteractive",
        "-Command",
        POWERSHELL_COMMANDS[category],
    )

    try:
        completed = executor(
            command,
            capture_output=True,
            check=False,
            shell=False,
            text=True,
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired:
        return CollectionResult(category=category, status="failed", error="timeout")
    except OSError:
        return CollectionResult(category=category, status="unavailable", error="powershell")

    if completed.returncode != 0:
        status = "denied" if "access is denied" in completed.stderr.lower() else "failed"
        return CollectionResult(category=category, status=status, error="command")

    try:
        data = json.loads(completed.stdout)
    except json.JSONDecodeError:
        return CollectionResult(category=category, status="failed", error="invalid_json")

    return CollectionResult(category=category, status="collected", data=data)

"""Redact and render PC assessment results without retaining raw command output."""

from __future__ import annotations

import os
import re
import socket
from collections.abc import Mapping, Sequence
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

try:
    from .pc_collectors import CollectionResult
except ImportError:
    from pc_collectors import CollectionResult


IPV4_PATTERN = re.compile(r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])")
MAC_PATTERN = re.compile(r"(?i)(?<![0-9a-f])(?:[0-9a-f]{2}[:-]){5}[0-9a-f]{2}(?![0-9a-f])")
WINDOWS_PATH_PATTERN = re.compile(r"(?i)\b[A-Z]:\\[^\r\n\t,;|]+")
SENSITIVE_FIELDS = {
    "account",
    "hostname",
    "macaddress",
    "serialnumber",
    "user",
    "username",
}


def redact_text(value: str) -> str:
    redacted = value
    replacements = {
        str(Path.home()): "<HOME>",
        Path.home().name: "<USER>",
        socket.gethostname(): "<HOST>",
    }
    for original, replacement in replacements.items():
        if original:
            redacted = re.sub(re.escape(original), replacement, redacted, flags=re.IGNORECASE)
    redacted = IPV4_PATTERN.sub("<IP_ADDRESS>", redacted)
    redacted = MAC_PATTERN.sub("<MAC_ADDRESS>", redacted)
    return WINDOWS_PATH_PATTERN.sub("<PATH>", redacted)


def redact(value: Any) -> Any:
    if isinstance(value, str):
        return redact_text(value)
    if isinstance(value, Mapping):
        return {
            str(key): "<REDACTED>" if str(key).lower() in SENSITIVE_FIELDS else redact(item)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [redact(item) for item in value]
    return value


def report_directory(environ: Mapping[str, str] | None = None) -> Path:
    values = os.environ if environ is None else environ
    base = values.get("LOCALAPPDATA")
    return Path(base) / "Kepler" / "pc-assessment" if base else Path.home() / "AppData" / "Local" / "Kepler" / "pc-assessment"


def _items(value: Any) -> list[Mapping[str, Any]]:
    if isinstance(value, Mapping):
        return [value]
    if isinstance(value, list):
        return [item for item in value if isinstance(item, Mapping)]
    return []


def _category_data(results: Sequence[CollectionResult], category: str) -> Mapping[str, Any]:
    for result in results:
        if result.category == category and result.status == "collected" and isinstance(result.data, Mapping):
            return result.data
    return {}


def _findings(results: Sequence[CollectionResult]) -> list[tuple[int, str]]:
    findings: list[tuple[int, str]] = []
    for result in results:
        if result.status != "collected":
            findings.append(
                (1, f"{result.category}: evidence {result.status}; health cannot be confirmed from this source")
            )

    security = _category_data(results, "security")
    defender = security.get("Defender")
    if isinstance(defender, Mapping):
        disabled = [
            name
            for name in ("AntivirusEnabled", "AntispywareEnabled", "RealTimeProtectionEnabled")
            if defender.get(name) is False
        ]
        if disabled:
            findings.append((0, f"security: disabled protections reported: {', '.join(disabled)}"))
    disabled_firewalls = [
        str(profile.get("Name", "unknown"))
        for profile in _items(security.get("FirewallProfiles"))
        if profile.get("Enabled") is False
    ]
    if disabled_firewalls:
        findings.append((0, f"security: disabled firewall profiles: {', '.join(disabled_firewalls)}"))

    drivers = _category_data(results, "drivers")
    problem_devices = _items(drivers.get("ProblemDevices"))
    if problem_devices:
        findings.append((0, f"drivers: {len(problem_devices)} present device(s) reported a non-OK state"))
    unsigned = [item for item in _items(drivers.get("SignedDrivers")) if item.get("IsSigned") is False]
    if unsigned:
        findings.append((1, f"drivers: {len(unsigned)} installed driver record(s) reported unsigned"))

    hardware = _category_data(results, "hardware")
    hardware_problem_devices = _items(hardware.get("ProblemDevices"))
    if hardware_problem_devices and not problem_devices:
        findings.append((0, f"hardware: {len(hardware_problem_devices)} present device(s) reported a non-OK state"))
    whea_events = _items(hardware.get("WHEA"))
    if whea_events:
        findings.append((0, f"hardware: {len(whea_events)} WHEA hardware event(s) reported in the seven-day window"))

    storage = _category_data(results, "storage")
    for volume in _items(storage.get("Volumes")):
        size = volume.get("Size")
        remaining = volume.get("SizeRemaining")
        if isinstance(size, (int, float)) and size > 0 and isinstance(remaining, (int, float)):
            free_percent = remaining / size * 100
            if free_percent < 15:
                label = volume.get("DriveLetter") or volume.get("FileSystemLabel") or "mounted volume"
                findings.append((0 if free_percent < 10 else 1, f"storage: {label} has {free_percent:.1f}% free space"))

    updates = _category_data(results, "updates")
    update_failures = _items(updates.get("Failures"))
    if update_failures:
        findings.append((1, f"updates: {len(update_failures)} warning/error event(s) in the seven-day window"))

    reliability = _category_data(results, "reliability")
    event_groups = _items(reliability.get("SystemWarningAndErrorGroups"))
    if event_groups:
        event_count = sum(item.get("Count", 0) for item in event_groups if isinstance(item.get("Count"), int))
        findings.append((1, f"reliability: {event_count} warning/error event(s) across {len(event_groups)} top group(s)"))

    developer = _category_data(results, "developer")
    path_entries = [item for item in developer.get("PathEntries", []) if isinstance(item, str)]
    duplicate_paths = len(path_entries) - len({item.casefold() for item in path_entries})
    if duplicate_paths:
        findings.append((2, f"developer: {duplicate_paths} duplicate PATH entry or entries detected"))

    if not findings:
        findings.append((3, "no material warning was detected in the available metadata"))
    return sorted(findings, key=lambda item: (item[0], item[1]))


def _inventory_summary(results: Sequence[CollectionResult]) -> list[str]:
    lines: list[str] = []
    system = _category_data(results, "system")
    operating_system = system.get("OperatingSystem", system)
    if isinstance(operating_system, Mapping):
        caption = operating_system.get("Caption")
        build = operating_system.get("BuildNumber")
        if caption:
            lines.append(f"- Operating system: {redact_text(str(caption))} (build {build or 'unknown'})")

    storage = _category_data(results, "storage")
    for volume in _items(storage.get("Volumes")):
        size = volume.get("Size")
        remaining = volume.get("SizeRemaining")
        label = volume.get("DriveLetter") or volume.get("FileSystemLabel") or "mounted volume"
        if isinstance(size, (int, float)) and isinstance(remaining, (int, float)):
            lines.append(f"- Storage {label}: {remaining / 2**30:.1f} GiB free of {size / 2**30:.1f} GiB")

    software_result = next((item for item in results if item.category == "software"), None)
    software = _items(software_result.data) if software_result and software_result.status == "collected" else []
    lines.append(f"- Installed software records: {len(software)}")

    startup_result = next((item for item in results if item.category == "startup"), None)
    startup = _items(startup_result.data) if startup_result and startup_result.status == "collected" else []
    lines.append(f"- Startup records: {len(startup)}")

    drivers = _category_data(results, "drivers")
    lines.append(f"- Signed driver records: {len(_items(drivers.get('SignedDrivers')))}")

    developer = _category_data(results, "developer")
    tool_names = sorted(
        {str(item.get("Name")) for item in _items(developer.get("Tools")) if item.get("Name")}
    )
    lines.append(f"- Developer commands found: {', '.join(tool_names) if tool_names else 'none reported'}")
    return lines


def render_report(results: Sequence[CollectionResult], *, generated_at: datetime | None = None) -> str:
    generated = generated_at or datetime.now().astimezone()
    window_start = generated - timedelta(days=7)
    findings = _findings(results)
    collected_count = sum(result.status == "collected" for result in results)
    gap_count = len(results) - collected_count
    lines = [
        "# Windows PC assessment",
        "",
        "## Window and scope",
        "",
        f"- Window: {window_start.isoformat(timespec='seconds')} to {generated.isoformat(timespec='seconds')}",
        "- Sources: approved Windows system, update, security, driver, hardware, storage, network, software, startup, developer, and reliability metadata.",
        "- Content paths: none approved or inspected.",
        "- Exclusions: file contents, OneDrive, Google Drive traversal, browser/credential data, communications, packet capture, and all machine changes.",
        "- Baseline: first run; observations are not week-over-week deltas.",
        "",
        "## Executive assessment",
        "",
        f"Collected {collected_count} of {len(results)} approved metadata categories with {gap_count} evidence gap(s).",
        "This report is observational and authorizes no remediation.",
        "",
        "## Collection status",
        "",
    ]
    status_priority = {"denied": 0, "failed": 1, "unavailable": 2, "collected": 3}
    for result in sorted(results, key=lambda item: (status_priority.get(item.status, 0), item.category)):
        lines.append(f"- {result.category}: {result.status}")

    lines.extend(
        [
        "",
        "## Prioritized findings",
        "",
        ]
    )
    impact_names = {0: "high", 1: "medium", 2: "low", 3: "low"}
    for priority, finding in findings:
        lines.append(f"- {finding} (impact: {impact_names[priority]}; confidence: high)")

    lines.extend(
        [
            "",
            "## Inventory summary",
            "",
            *_inventory_summary(results),
            "",
            "## Predictions",
            "",
            "- Over the next one to two weeks, unresolved high-impact findings are expected to remain observable unless their underlying configuration changes (confidence: medium).",
            "- If no remediation is performed, inventory counts should remain broadly stable; software or Windows updates would invalidate this prediction (confidence: low).",
            "",
            "## Suggested actions",
            "",
            "1. Review high-impact findings and evidence gaps before considering cleanup.",
            "2. Review installed software and startup entries with user context; do not infer removability from names or age alone.",
            "3. Use Windows Update or exact manufacturer sources for any separately approved driver action.",
            "",
            "## Data and uncertainty",
            "",
            "- The assessment is a first-run snapshot and cannot prove what changed without an approved prior baseline.",
            "- Non-admin collection may leave some Windows security or event sources unavailable.",
            "- Driver inventory identifies reported state but does not query vendor catalogs for latest versions.",
            "",
            "No update, uninstall, network change, firmware action, or file move is authorized by this report.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_report(
    results: Sequence[CollectionResult],
    *,
    destination: Path | None = None,
    generated_at: datetime | None = None,
) -> Path:
    generated = generated_at or datetime.now().astimezone()
    output_directory = destination or report_directory()
    output_directory.mkdir(parents=True, exist_ok=True)
    output = output_directory / f"pc-assessment-{generated:%Y%m%d-%H%M%S}.md"
    output.write_text(render_report(results, generated_at=generated), encoding="utf-8")
    return output

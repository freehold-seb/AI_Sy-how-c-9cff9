# One-time Windows PC assessment

## Current status

The assessment workflow is read-only and fail-closed. Its collectors are tested
with synthetic JSON before any live collection is considered. Preview is the
default mode and executes no PowerShell commands.

Live collection is not a cleanup authorization. Updates, firmware actions,
uninstalls, network changes, and file moves remain separate actions requiring
individual approval and rollback checks.

## Collection boundary

The allowlist in `scripts/system/pc_collectors.py` contains the only PowerShell
commands the workflow can execute. Commands run as argument arrays with
`shell=False`, without profiles or interactive prompts, under the current user,
and with a 30-second timeout. The workflow never self-elevates.

The available categories are:

- `system`: Windows version, build, and boot metadata.
- `updates`: recent Windows hotfixes and bounded update warning/error events.
- `security`: Defender protection state and Windows Firewall profiles.
- `drivers`: signed Plug and Play driver metadata.
- `storage`: physical-disk health plus mounted volume type, capacity, and free
  space.
- `network`: adapter/profile status, DNS, default routes, WinHTTP proxy, and up
  to 100 listening TCP endpoints; no packets or payloads.
- `software`: machine-wide installed application names, versions, publishers,
  and install dates from machine-wide and current-user uninstall metadata.
- `startup`: startup entry names, locations, and owning users.
- `developer`: command and PATH metadata for common development tools.
- `reliability`: aggregate counts for up to 25 recent system warning/error
  groups; event messages are not retained.

The collector does not invoke uninstall strings, installers, package upgrades,
driver updates, firmware tools, file enumerators, or network reset commands.

## Exclusions

- No file contents or directory traversal.
- No OneDrive inspection.
- No Google Drive traversal or file hydration. Detecting or inspecting a Google
  Drive mount requires a later, exact-path approval after the file organizer's
  four fixture gates pass.
- No browser profiles, credentials, communications, or sensitive documents.
- No packet capture or payload inspection.
- No persistent raw PowerShell output.

## Usage

Run the safe preview from the repository root:

```powershell
python scripts/system/pc_assessment.py --preview
```

The preview prints the exact seven-day window, report destination, commands,
privilege posture, and exclusions. It does not create a report.

A future live read-only invocation must explicitly select every category and
include the exact phrase printed by the CLI. Approval is scoped to that single
invocation and is not stored. Review the preview immediately before running it.

Reports are redacted and written outside Git beneath
`%LOCALAPPDATA%\Kepler\pc-assessment\`. Usernames, hostnames, paths, IP
addresses, and MAC addresses are removed. Failed, denied, and unavailable
sources remain visible as evidence gaps rather than being treated as healthy.

## Hardware baseline fallback

If the Copilot agent sandbox denies Windows CIM/WMI access, run the read-only
hardware snapshot from a normal PowerShell session outside the sandbox:

```powershell
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\system\hardware_baseline.ps1
```

The script prints computer, memory, CPU, motherboard, BIOS, present non-OK
device, and last-24-hour WHEA event metadata. It does not change firmware,
drivers, devices, clocks, voltages, files, or Windows settings.

## Verification

```powershell
python -m pytest tests/test_pc_assessment.py -q
python scripts/system/pc_assessment.py --preview
python -m pytest tests/test_repo_smoke.py -q
python -m pytest -q
python -m compileall -q agent_core core runner services verifier workflows scripts
git diff --check
```

## Remediation policy

Use Windows Update or the exact hardware manufacturer's official source for
routine drivers. Never use a third-party driver updater. BIOS, UEFI, and device
firmware remain report-only until separately approved with model, power,
BitLocker recovery, backup, and rollback checks.

Review software usefulness with the user; names and age are not sufficient
evidence for removal. Apply at most one approved uninstall or network change at
a time and rerun its focused health check before proceeding.

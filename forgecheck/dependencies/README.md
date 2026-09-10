# ForgeCheck Dependencies (First Pass)

This folder is the first-pass dependency/driver reference catalog used by ForgeCheck planning.

## Purpose

When hardware is detected, ForgeCheck maps the system class (for example `amd_amd` or `intel_nvidia`) to recommended package families so you know what to review/install first.

## Policy

- OEM-first source strategy
- Vendor fallback
- Windows Update as last fallback
- No automatic installation in Phase 1.x

## File

- `catalog.yaml` — system-class dependency mapping used by planner metadata and per-action hints.

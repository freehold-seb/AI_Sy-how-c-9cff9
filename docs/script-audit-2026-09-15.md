# Script audit

Generated: 2026-09-15
Scope: current recovery workspace only; header-only inventory and disposition of scripts.

## Baseline decision

The active baseline is exactly these three items:

1. `ochre_bridge.py`
2. `scripts/daily_briefing.py`
3. `.vscode/tasks.json`

Everything else below is outside the active baseline unless it is separately reviewed and promoted.

## Active

- `ochre_bridge.py` — active voice-to-clipboard bridge; prior `Copied:` output is documented
- `scripts/daily_briefing.py` — active read-only briefing generator; one successful run is documented
- `.vscode/tasks.json` — active task wiring for the current workflow

## Deferred

These files are retained but are not part of the active baseline:

- `scripts/prepare_prompt.py` — deferred clipboard prompt helper
- `scripts/workspace_inventory.py` — deferred metadata inventory helper
- `agent.py` — deferred compatibility launcher
- `control_panel.py` — deferred compatibility launcher
- `workflows/run_verifier_pipeline.py` — deferred workflow entrypoint
- `runner/` — deferred restored local runner boundary
- `verifier/` — deferred restored local verifier boundary
- `tests/test_repo_smoke.py` — deferred test coverage; it does not itself activate runtime behavior

## Review before run

These files must not be run as part of the active workflow without a separate review:

- `scripts/files/archive_old_files.ps1` — references missing `cleanup_and_sort.ps1`; archive behavior is not approved
- `scripts/system/remove_mesh_sync_task.ps1` — system-level task removal; not approved for execution

## Header inventory

### `scripts/`

- `scripts/daily_briefing.py` — ACTIVE
- `scripts/prepare_prompt.py` — DEFERRED
- `scripts/workspace_inventory.py` — DEFERRED
- `scripts/files/archive_old_files.ps1` — REVIEW-BEFORE-RUN
- `scripts/system/remove_mesh_sync_task.ps1` — REVIEW-BEFORE-RUN

### Root-level Python files

- `ochre_bridge.py` — ACTIVE
- `agent.py` — DEFERRED
- `control_panel.py` — DEFERRED

## Live safety state observed during audit

- `config/agent_config.json`: `dry_run` is `true`
- `config/agent_config.json`: `orchestrator_enabled` is `false`
- No script was run during this audit
- No file was deleted, archived, renamed, or moved

## Final disposition

This is an audit decision only. The current repo remains fail-closed and single-node. No script promotion, deletion, archival, or system change is authorized by this document.

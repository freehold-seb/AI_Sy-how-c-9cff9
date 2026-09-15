# Script audit

Generated: 2026-09-15
Scope: current recovery workspace only; decision record for active baseline vs non-baseline repo scripts.

## Baseline decision

The active baseline is exactly these three items:

1. `ochre_bridge.py`
2. `scripts/daily_briefing.py`
3. `handoff.md` and its supporting docs under `docs/`

Everything else in the repo is not part of the active baseline unless it is explicitly restored, used, and validated later.

## Active baseline

- `ochre_bridge.py` — active
- `scripts/daily_briefing.py` — active
- `handoff.md` — active
- `docs/` — active support docs for the project record and operating model

## Deferred

These files are not part of the active baseline and are valid to keep only as deferred, non-runtime helpers until they are re-proven:

- `scripts/prepare_prompt.py` — deferred; prompt helper, not part of the proven runtime path
- `scripts/workspace_inventory.py` — deferred; repo inventory utility, not part of the active baseline
- `tests/test_repo_smoke.py` — deferred; smoke coverage exists, but it does not prove the active runtime boundary
- `workflows/run_verifier_pipeline.py` — deferred; reaches the restored boundary but is not part of the active baseline until separately validated
- `scripts/files/archive_old_files.ps1` — deferred; cleanup script needs explicit review before any use
- `scripts/system/remove_mesh_sync_task.ps1` — deferred; operational script, not part of the active baseline
- `agent.py` — deferred; not part of the proven execution path
- `control_panel.py` — deferred; not part of the proven execution path

## Remove after review

These are legacy or speculative structures that are not part of the active baseline and should be reviewed for archival or cleanup once the minimal proof path is stable:

- `agent_core/` — remove after review; not proven to be an active runtime system
- `core/` — remove after review; legacy layer with no active execution path in the current baseline
- `services/` — remove after review; not part of the active baseline and appears to be stale scaffolding
- `modules/` — remove after review; not part of the active baseline
- `runner/` — deferred; restored bounded runner boundary, but not part of the active baseline
- `verifier/` — deferred; restored deterministic verifier boundary, but not part of the active baseline
- `forgecheck/` — remove after review; speculative tooling not connected to the active baseline

## Final audit disposition

The current repo is not to be treated as a full runtime. It is a minimal proof surface with a clear baseline and a clear audit boundary.

- Keep active: `ochre_bridge.py`, `scripts/daily_briefing.py`, `handoff.md`, and the docs that support the handoff
- Keep deferred: non-runtime helper scripts and partially recovered tooling
- Remove after review: orphaned or speculative directories that are not the active baseline

No deletions are performed as part of this audit. This file is the decision record only.

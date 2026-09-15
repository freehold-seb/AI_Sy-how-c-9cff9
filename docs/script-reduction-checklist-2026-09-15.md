# Script reduction checklist

Generated: 2026-09-15
Scope: current recovery workspace only; direct reduction plan for the active working surface.

## Working baseline

These are the only items that should remain in normal use until a missing runtime boundary is restored and validated:

- `scripts/daily_briefing.py`
- `scripts/prepare_prompt.py`
- `ochre_bridge.py`
- `tests/test_repo_smoke.py`
- `handoff.md`
- `.vscode/tasks.json`

## Keep but do not expand beyond

These may remain available as reference or support files, but they are not part of the active runtime path unless independently proven:

- `scripts/workspace_inventory.py`
- `README.md`
- `docs/*.md`
- `config/agent_config.json`
- `config/runtime_mode.json`

## Quarantine or defer

These should be treated as deferred or speculative until proven active:

- `workflows/run_verifier_pipeline.py`
- `runner/`
- `verifier/`
- `scripts/files/archive_old_files.ps1`
- `agent_core/`
- any duplicate or unreviewed scripts outside the proven working path

## Action today

1. Keep the active baseline in the normal workflow.
2. Do not run speculative scripts or archive scripts.
3. Do not broaden validation until the missing runner/verifier boundary is restored.
4. Record any friction in the handoff and keep the project fail-closed.
5. Use only the proven baseline for the next real task.

## Rule

The correct state for today is: minimal working surface, no speculative automation, no broad validation, and one narrow next proof step at a time.

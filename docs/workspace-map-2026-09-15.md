# Workspace map

Updated: 2026-09-15

## Scope

This is a first-pass map of the Kepler workspace and the current recovery repository. It is based on repository metadata, filenames, and selected project configuration. No personal documents, browser data, credentials, or broad user folders were inspected.

## Topology

- Active recovery worktree: `AI_Sy-do-th-126fe`
- Sibling worktrees: 7 additional worktrees are present under `C:\Users\SEB\kepler\worktrees`
- Separate repository: `C:\Users\SEB\kepler\repositories\freehold-web`
- Canonical workspace: `AI_Sy-do-th-126fe`
- Current runtime posture: single-node recovery mode
- Second node, mesh sync, and SSH are documented as future or disabled work

## What is currently real

- `ochre_bridge.py`: local speech-to-clipboard tool; verified to produce `Copied:` transcripts
- `docs/service-tool-usage.md`: operating instructions for turning raw speech into usable service output
- `docs/service-tool-framing.md`: service-tool boundary
- `docs/real-vs-aspirational-2026-09-15.md`: proven versus deferred work
- `docs/minimum-viable-workflow-2026-09-15.md`: staged operating plan
- `core/agent.py`, `core/control_panel.py`, and `services/queue_worker.py`: minimal bootstrap stubs that keep compatibility imports alive
- `runner/` and `verifier/`: the runner/verifier boundary described as absent below has since been restored (see the update note under "What is currently skeletal or unproven") and is covered by `tests/test_repo_smoke.py`

## What is support infrastructure

- `config/`: runtime and autonomy settings
- `docs/`: operating rules, handoffs, and roadmaps
- `tests/test_repo_smoke.py`: import-level smoke coverage
- `forgecheck/`: partial safety/reporting scaffold
- `.github/agents/` and `.github/skills/`: workflow guidance and local operating instructions
- `scripts/`: potentially destructive or incomplete maintenance scripts; review before use

## What is currently skeletal or unproven

> Update: the bullets below on `runner/` and `verifier/` describe this
> repository's 2026-09-15 recovery snapshot and are now stale. Both
> packages have since been implemented with concrete submodules
> (`verifier/domain_rules.py`, `verifier/metrics.py`, `verifier/models.py`,
> `verifier/qc_learning.py`, `verifier/schemas.py`,
> `runner/orchestrator_adapter.py`, `runner/run_verifier_pipeline.py`) and
> are exercised by `tests/test_repo_smoke.py`. `workflows/run_verifier_pipeline.py`
> forwards to the now-present `runner` module. The historical text is kept
> below for the audit trail.

- `modules/freehold/`: package shells without substantive implementation in this snapshot
- `skills/*`: multiple manifests describe capabilities, but most corresponding runtime implementations are not present here
- `agent_core/`: only a self-modification placeholder is present
- `runner/`: package shell only
- `verifier/`: the real verifier submodules referenced by the original exports are absent
- `workflows/run_verifier_pipeline.py`: forwards to a runner module that is not present in this snapshot

## Immediate hazards and drift

- `scripts/files/archive_old_files.ps1` calls `cleanup_and_sort.ps1`, but that file is not present in the visible script tree. Do not run the wrapper until its target is recovered and reviewed.
- `config/agent_config.json` enables orchestration and sets `dry_run` to false, while the active code is largely skeletal. Treat this as configuration drift until the runtime owner is confirmed.
- There are many declared capabilities without matching implementations or tests. Treat manifests as intentions, not available features.
- The current repo is a partial recovery snapshot, so absence of a file does not prove it never existed.

## Safe operating categories

### Keep active

- `ochre_bridge.py`
- the service-tool documentation
- the minimum smoke test
- single-node configuration

### Review next

- compatibility stubs and import paths
- `workflows/run_verifier_pipeline.py`
- `config/agent_config.json`
- the `skills/` manifests against actual implementation files
- the separate `freehold-web` repository boundary

### Do not touch without explicit review

- deletion or archiving scripts
- mesh/SSH task scripts
- credentials, `.env` files, browser data, personal documents, or payment data
- anything under the sibling worktrees until the canonical worktree is chosen

## Recommended cleanup order

1. Produce a metadata-only inventory of sibling worktrees and the separate repository.
2. Verify the import and smoke-test baseline.
3. Mark each module as active, support, placeholder, or deferred.
4. Quarantine or archive only after a review list exists.
5. Run a separate Windows security/system audit with explicit read-only scope.

## Naming rule

Keep the current paths stable. Use short, descriptive names such as `daily_briefing.py`, `service-tool-usage.md`, and `workspace-map-2026-09-15.md`. Do not introduce codenames, abbreviations, or nested wrappers unless they solve a demonstrated problem.

## Current conclusion

The biggest problem is organization and ownership, not a lack of files. The repo contains several overlapping intentions, but only a small working core. The next useful action is to establish the canonical workspace and inventory the surrounding worktrees before deleting anything.

# Operating decision

Generated: 2026-09-15
Scope: current recovery workspace only; active decision for the project owner and AI lead.

## Final decision

The project is not yet autonomous because the active runtime boundary is incomplete and the repo is still a partial recovery snapshot. The correct operating posture is fail-closed, single-node, and proof-first.

## What is proven

- Voice bridge works in the current workspace and produces observable transcript output
- Daily briefing task executes and generates a dated report under `reports/`
- Manual `TRANSLATE:` / `SAUCE:` refinement works on real inputs
- The canonical project record is `handoff.md`
- The repo is configured to remain fail-closed until missing runtime components are restored and validated

## What remains deferred

- full multi-node runtime
- orchestrator implementation
- runner/verifier boundary restoration
- broader validation pass against missing modules
- any automation beyond a reversible, bounded handoff

## Project rule

The project must operate under this rule:

- one canonical handoff
- one lead AI per task
- no competing AI rewrites of the same state
- one narrow next action at a time
- no broad validation until the missing boundary is restored and proven
- any automation must be reversible, observable, and paused before irreversible actions

## Immediate next action

Use the proven working path only:

1. run the bridge on one real problem
2. paste the transcript with `TRANSLATE:` or `SAUCE:`
3. record the friction in the handoff
4. do not start a second feature or second improvement
5. keep the repo in the fail-closed baseline until a missing boundary is restored and validated

This is the shortest route to real progress without reintroducing drift or false validation.

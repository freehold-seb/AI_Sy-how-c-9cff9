# Today autonomy plan

Generated: 2026-09-15
Scope: current recovery workspace only; executable project plan for today.

> Update: the runner/verifier boundary referenced as "missing" throughout
> this plan has since been restored and is covered by
> `tests/test_repo_smoke.py`. Kept for the historical record.

## Goal

Create a safe, single-threaded operating baseline that reduces churn, keeps the project in a fail-closed state, and produces real progress without pretending the full autonomous system is already running.

## Non-negotiable rules

1. One canonical handoff: `handoff.md`
2. One lead AI per task
3. One specialist only for a defined gap
4. No parallel AI edits to the same state
5. No broader validation until the missing runner/verifier boundary is restored and validated in isolation
6. Every task must answer: what proof did this produce?
7. Every task must be reversible unless it is a documented, reviewed validation step

## Today’s working baseline

Keep these items active and proven:

- `scripts/daily_briefing.py`
- `scripts/prepare_prompt.py`
- `ochre_bridge.py`
- `tests/test_repo_smoke.py`
- `handoff.md`
- `.vscode/tasks.json`

These items are not yet proven as autonomous runtime and remain deferred or speculative until independently restored and validated:

- `workflows/run_verifier_pipeline.py`
- `runner/`
- `verifier/`
- `scripts/files/archive_old_files.ps1`
- `agent_core/`
- any unreviewed or duplicate scripts outside the proven working path

## Execution sequence for today

### Step 1: freeze the baseline

- Confirm the current recovery-hand-off baseline is the canonical source of truth
- Keep orchestration fail-closed and do not broaden automation
- Do not run archive or deletion scripts without review

### Step 2: reduce the repo surface

- Make a short list of all scripts and identify each as active, dormant, or speculative
- Keep only the proven active path in normal use
- Quarantine any speculative or duplicate scripts that are not currently part of the working workflow

### Step 3: define the one-way AI chain

Use this chain:

```text
User -> lead AI -> canonical handoff -> specialist (only if needed) -> canonical handoff -> next action
```

Do not allow multiple AI systems to rewrite the same state in parallel.

### Step 4: force a standard response format

Every AI must answer these questions before an edit or plan is accepted:

- CONTRIBUTION
- CURRENT STATE
- GOAL
- KNOWN GAPS
- NEXT HANDOFF
- RISK OF CONFUSION

### Step 5: define the first bounded automation candidate

Only after three real manual runs are recorded should any automation be introduced. The automation candidate must be:

- reversible
- observable
- paused before irreversible actions
- documented in the handoff

### Step 6: restore one missing boundary at a time

Target the missing runner/verifier boundary first. Restore only that boundary, validate it in isolation, and then decide whether a broader pass is appropriate.

### Step 7: record one proof outcome

After each step, write one sentence that answers: what did we prove today?

## Today’s target outcome

By the end of the day, the project should have:

- one canonical handoff
- one clear single-threaded AI model
- one verified working baseline
- one reduced script surface
- one explicit deferred gap list
- one defined next automation boundary

This is the path to real progress without pretending the missing runtime is already restored.

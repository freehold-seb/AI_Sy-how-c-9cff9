# Kepler / AI_Sy-do-th-126fe — Handoff

**Date:** 2026-09-16
**Time:** 09:34 EDT
**Branch:** do-the-next-5-most
**Status:** LOCKED — baseline proven by live output

---

## Proven baseline (do not assume, do not skip)

| Check | Command | Observed result |
| --- | --- | --- |
| Working tree | `git status --short` | Clean — 0 modified, 0 untracked |
| Branch sync | `rev-list --left-right HEAD...origin/do-the-next-5-most` | `0 0` |
| Smoke tests | `pytest -q tests/test_repo_smoke.py` | `5 passed in 0.03s` |
| agent.py | `python core\agent.py` | `AI workspace runtime ready at …\AI_Sy-do-th-126fe` |
| control_panel.py | `python core\control_panel.py` | `Control panel ready at …\AI_Sy-do-th-126fe` |
| queue_worker.py | `python services\queue_worker.py` | Clean exit, no error |

---

## Reusable preflight (run at the start of every session)

```powershell
$wt = "C:\Users\SEB\kepler\worktrees\AI_Sy-do-th-126fe"
Write-Host '--- git ---'
git -C $wt status --short --branch
git -C $wt rev-list --left-right --count HEAD...origin/do-the-next-5-most
Write-Host '--- pytest ---'
python -m pytest -q $wt\tests\test_repo_smoke.py
Write-Host '--- entrypoints ---'
python $wt\core\agent.py
python $wt\core\control_panel.py
python $wt\services\queue_worker.py
```

Pass criteria — all four must be true:

1. `git status` → no modified or untracked files
2. `rev-list` → `0 0`
3. `pytest` → N passed, zero failures
4. All three entrypoints → expected ready message or clean exit

If any single line deviates: stop, fix that one thing, re-run. Do not continue past a failure.

---

## Scope boundary

**Proven:** repo is importable, bootstrap paths are operational, branch is in sync.

**Not proven:** orchestration, external integrations, feature completeness.

---

## Session rules

- Run preflight before touching anything
- One label per bridge pass (`TRANSLATE` or `SAUCE`, not both)
- One friction point per pass — note it, stop
- No new repo work until the current pass is closed and recorded
- Documents and plans are not proof — only runtime output counts

---

## Next action

Run one bridge pass. One label. One transcript. Evaluate the output. Record one friction point. Stop.

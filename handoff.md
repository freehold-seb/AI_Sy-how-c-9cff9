# Kepler Recovery System - Handoff

**Date:** 2026-09-18
**Branch:** `recovery/kepler-baseline-and-safety`
**Remote:** `git@github.com:freehold-seb/AI_Sy-how-c-9cff9.git`
**Status:** Hardware-baseline fallback script is committed at `9d018bb`; Gate 2/3/4 organizer and hardware-diagnostics changes are uncommitted

## Naming

This worktree is the **Kepler Recovery System**. The active local branch is
`recovery/kepler-baseline-and-safety`. The old remote branch
`origin/do-the-next-5-most` and the locked sibling worktree branches were left
unchanged; rename or deletion of those requires a separate repository review.

## Current session queue

The next priorities are hardware evidence and stability, reversible tuning
records, fixture-only file-organizer safety gates, daily briefing delivery, and
independent repository coordination. This recovery worktree must not modify
`freehold-web`; its status must be checked from its canonical checkout instead.

The current uncommitted hardware-diagnostics slice adds a read-only assessment
category for CPU clocks, memory configuration, GPU and BIOS metadata, present
non-OK devices, and bounded WHEA events. Its focused tests and full suite have
passed in this session; the changes remain uncommitted.

File-organizer Gate 2 is complete in the current uncommitted slice:
conflicts are detected during fixture planning, routed to `unsorted/`, and
labelled in dry-run output without filesystem mutation. Focused organizer tests
passed (`14 passed`), and the normal fixture dry-run output remains unchanged.

File-organizer Gate 3 is complete as well: fixture-only `--execute` moves
planned files, writes `move_log.txt`, and validates that every source was moved
to its planned destination.

File-organizer Gate 4 is complete in the same uncommitted slice: fixture-only
`--execute` exits 2 unless the exact confirmation phrase is supplied, and no
default/classification/dry-run path moves files. Focused organizer tests passed
(`17 passed`), the full suite passed (`115 passed`), and the committed fixture
dry-run remained unchanged.

The next active task is backlog item 10: connect speech input to a dry-run-only
file organization command. The Gate 2/3/4 slice is not committed; the current
working-tree changes are intentional and must remain distinguishable from the
committed hardware-baseline fallback.

## Verified repository state

- HEAD: `9d018bb` - `Add hardware baseline fallback for sandboxed CIM access`
- The local branch was renamed from `do-the-next-5-most`; its previous remote
  tracking branch is `origin/do-the-next-5-most`.
- The branch is ahead of `origin/do-the-next-5-most` by four local commits
  (`b7b8675`, `49abbd5`, `40653b5`, `9d018bb`), confirmed via
  `git rev-list --count origin/do-the-next-5-most..HEAD` = 4; working tree has
  the intentional uncommitted Gate 2/3/4 and hardware-diagnostics changes listed
  above.
- Full test suite (2026-09-18): `115 passed`; file-organizer focused tests:
  `17 passed`; PC-assessment focused tests: `18 passed`.
- The sandbox's default pytest temp path
  (`AppData\Local\Packages\sandbox.*\AC\Temp`) is still denied; use
  `--basetemp <repo>\.tmp\pytest` (create the parent directory first) until
  that default is allowed.
- Python compilation (2026-09-18): passed
- JSON parsing: 31 files parsed with UTF-8 BOM tolerance
- `git diff --check` (2026-09-18): passed
- Workspace diagnostics: no errors in touched files

## Baseline and tags

- Golden baseline tag: `golden-baseline-hardened-pipeline`
- Tag target: `5fdb9e4` - `Harden pipeline with schema validation and dry-run isolation`
- Baseline documentation: [BASELINE.md](BASELINE.md)

## Delivered slices

1. Config schema validation and strict boolean parsing.
2. Verifier decision logging and finite-score validation.
3. TaskSpec schema enforcement.
4. Dry-run isolation at the pipeline boundary.
5. Read-only pipeline introspection collector.
6. Additive static routing expansion with preserved status/reason semantics.
7. Explicit-registry `CandidateHookRunner` with ordering, failure recovery,
   dry-run suppression, score bounds, and introspection events.
8. Fixture-only extension classification for document, image, audio, and
   unknown files, with CLI output and no filesystem mutations.
9. `scripts/file_organizer_schema.json` folder schema mapping every known
   category (document, image, audio, unknown) to a target folder name, with a
   validating `load_schema()` loader (rejects missing/unknown categories and
   blank folder names). Closes `tasks.md` backlog item 3.
10. Fixture-only dry-run planning for file organization. `plan_moves()` maps
   classified fixture files through the schema to source/destination records,
   and `--dry-run` prints planned moves without creating folders, writing logs,
   or moving files. Closes Gate 1 and `tasks.md` backlog item 4.
11. Read-only `scripts/system/hardware_baseline.ps1` fallback for running
   hardware checks from a normal PowerShell session when the Copilot sandbox
   denies CIM/WMI provider access. It prints computer, memory, CPU,
   motherboard, BIOS, present non-OK device, and last-24-hour WHEA metadata and
   does not change system state.
12. Fixture-tested Windows PC assessment foundation with exact PowerShell
  allowlisting, bounded execution, preview-by-default behavior, per-invocation
  confirmation, structured failure states, redaction, and Local AppData report
  generation. Coverage includes system, update, security, driver, storage,
  network, software, startup, developer-tool, and reliability metadata.

## Current boundaries

- Candidate hooks are implemented and tested, but not integrated into
  `run_pipeline`.
- Routing remains descriptive: static routes exist, but there is no conditional
  routing or route selection.
- Introspection is standalone and not wired into pipeline return values.
- File organizer backlog Gate 1 (dry-run), Gate 2 (conflict handling), Gate 3
  (fixture-only execution, logging, and post-move validation), and Gate 4
  (explicit confirmation before execution) are closed by runtime proof:
  `python scripts\file_organizer.py tests\fixtures\file_organizer_scan --dry-run`
  printed planned moves for documents, images, audio, and unknown files without
  moving anything; focused organizer tests passed with 17 tests and the full
  suite passed with 115 tests. Only backlog item 10 remains pending in this
  sequence.
- PC assessment preview was verified for the seven-day local-time window.
  The workflow remains read-only and does not authorize elevation, updates,
  uninstalls, network changes, firmware actions, cloud traversal, or file
  moves.
- A live read-only assessment and a firmware memory-profile change were
  discussed on 2026-09-17. The user reports 48 GB of memory and that the
  firmware settings are now applied. This session did not change firmware.
- Current live hardware verification is still blocked by the VS Code sandbox:
  Windows CIM/WMI queries (`Get-CimInstance`) return access-denied errors even
  after the 2026-09-17 policy update that fixed pytest's temp-directory
  access. No supported memory or CPU stability-test executable was found on
  `PATH`. Do not treat memory speed, temperatures, WHEA state, or the two
  previously reported non-OK devices as independently verified by this
  session; a further sandbox policy change permitting `Get-CimInstance` is
  required before that verification can run.
- Workaround for the same blocker: run
  `powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\system\hardware_baseline.ps1`
  from a normal PowerShell terminal outside the sandbox, then paste the output
  back into the session for interpretation.
- Assessment fixture tests: `18 passed`; repository smoke tests: `5 passed`;
  file-organizer tests: `17 passed`.
- All 11 allowlisted PowerShell command strings passed parser-only validation
  without executing their system queries.
- The hardware-baseline fallback is committed at `9d018bb`; no tag has been
  created for it.

## Local-only setup

- Serena is installed as `Serena 1.7.0`.
- Serena MCP setup is preserved in local stash `Serena setup kept separate from
  hardened baseline` and is intentionally not part of the repository commits.
- Generated `.serena/` metadata is locally ignored.

## Next repository: freehold-web

This worktree is not `freehold-web`. Do not merge PR #10 or change web-repo
files from here. The canonical local folder is:

`C:\Users\SEB\kepler\repositories\freehold-web`

Its remote is `https://github.com/freehold-seb/freehold-web.git`. Its current
state was preflighted on 2026-09-16: clean working tree, branch `main`, four
commits behind `origin/main`, with several locked worktrees all at the same
older commit. Open that folder separately, then inspect the remote PR state
before acting on PR #10. The supplied PR summary says it is docs-only and
likely safe, but that summary has not been independently verified here.

## Resume commands

```powershell
git status --short --branch
git log -2 --oneline --decorate
python -m pytest -q
```

For the next repo, use its own folder and run:

```powershell
git status --short --branch
git remote -v
git log -3 --oneline --decorate
```

# Task Backlog — Kepler Recovery System

## Hard constraint — fixtures only

All scanning, classification, move, and validation tasks must run against
disposable test fixtures in `tests/fixtures/` only.

Real user directories are off-limits until ALL four gates are independently
proven by runtime output:

1. Dry-run mode works and produces accurate output
2. Conflict handling works — no silent overwrites, unknowns routed to `unsorted/`
3. Post-move validation passes against expected schema state
4. Explicit confirmation step is required before any real move executes

No task below may skip ahead of this sequence.

---

## Next priorities — 2026-09-17

These are the next cross-repository work priorities. Work one slice at a time,
with runtime proof before moving on.

1. **Hardware evidence and stability**
        Identify the two non-OK devices, capture CPU/RAM/GPU/BIOS/WHEA evidence, and
        run an approved memory stability check before changing CPU/PBO or voltage.
        Done when the device states and stability result are recorded.
2. **Reversible tuning records**
        Record before/after hardware settings and a rollback path for every tuning
        change. Done when a failed profile can be reverted without guesswork.
3. **File-organizer safety gates**
        Complete fixture-only conflict handling, execution logging, post-move
        validation, and explicit confirmation in order. Done when each gate has
        independent runtime output.
4. **Daily briefing reliability**
        Decide whether the briefing should remain manually triggered or be scheduled,
        then verify one complete delivery path. Done when its trigger and output
        timestamp are unambiguous.
5. **Repository coordination**
        Keep this recovery repository's handoff current and inspect `freehold-web`
        only from its own canonical checkout. Done when each repository has an
        independently verified status; no cross-worktree edits or assumptions.

---

## Week-close queue - 2026-09-19

### Complete today

- [x] **1. High - Write the weekly recap.** Acceptance: accomplishments, gaps,
        failures, decisions, and Monday's starting point are recorded in
        `reports/weekly-recap-2026-09-19.md`.
- [x] **2. High - Fetch the tracked remote.** Acceptance: remote references are
        refreshed without merging or modifying local work.
- [x] **3. High - Inspect repository divergence.** Acceptance: branch, tracking
        state, staged files, and untracked files are known before synchronization.
- [x] **4. High - Run the repository smoke test.** Acceptance:
        `tests/test_repo_smoke.py` passes.
- [x] **5. High - Validate the workflow slice.** Acceptance:
        `tests/test_daily_workflows.py` passes using a repository-local temp path.
- [x] **6. Medium - Correct briefing file counts.** Acceptance: generated,
        cached, report, and vendored dependency files are excluded by a test.
- [x] **7. High - Record the service direction.** Acceptance: a tracked document
        defines the privacy-first, supervised file-organization service.
- [x] **8. High - Identify service privacy risks.** Acceptance: the service
        document covers disclosure, inspection, classification, deletion, scope,
        retention, access, consent, legal exposure, and claims.
- [x] **9. High - Define the fixture-only proof of concept.** Acceptance: scope,
        inspection levels, review routing, audit output, and success criteria are
        explicit and use synthetic fixtures only.
- [x] **10. High - Run the complete test suite.** Acceptance: all repository tests
        pass with a repository-local pytest temp directory.
- [x] **11. High - Compile supported Python packages.** Acceptance: `compileall`
        completes without errors for the supported package directories.
- [x] **12. Medium - Validate patch formatting.** Acceptance: `git diff --check`
        reports no whitespace errors.
- [x] **13. High - Update the handoff.** Acceptance: the handoff records current
        HEAD, validation evidence, remaining risks, and Monday's first action.
- [ ] **14. High - Commit the coherent closeout slice.** Acceptance: tracked and
        intentional new files are committed together with a descriptive message.
- [ ] **15. High - Push and verify synchronization.** Acceptance: the branch is
        pushed and reports no divergence from its tracked remote.

### Resume Monday

- [ ] **16. High - Investigate both non-OK devices.** Acceptance: each device has
        an identified cause, impact assessment, and reversible next action.
- [ ] **17. High - Run an approved stability check.** Acceptance: bounded memory
        and CPU test results are captured without changing tuning settings.
- [ ] **18. Medium - Verify Monday's manual briefing.** Acceptance: one briefing
        is generated manually with credible source-file counts and timestamp.
- [ ] **19. Medium - Draft the customer intake model.** Acceptance: a structured
        draft covers allowed roots, forbidden roots, inspection depth, sensitive
        classes, allowed actions, review, retention, deletion, and consent.

### Longer-term backlog

- [ ] **20. High - Produce the service threat model and data lifecycle.**
        Acceptance: every collected artifact has a purpose, storage location,
        access rule, retention period, deletion proof, and incident owner before
        any real customer-data trial.

---

## Backlog

Tasks are ordered by dependency. Pull from the top. One task per session.
Nothing moves to done without runtime output as proof.

- [x] 1. Scan a fixture directory and return a file list
        FIXTURE ONLY — script prints file names and extensions, no moves
- [x] 2. Classify scanned files by extension into named buckets
        FIXTURE ONLY — output maps each file to a category (image, doc, audio, etc.)
- [x] 3. Define and write the folder schema
        Produce `schema.json` — maps each category to a target folder name
- [x] 4. Dry-run mode — show planned moves without executing them
        FIXTURE ONLY — output lists what would move; nothing on disk changes
        GATE 1 closes here
- [x] 5. Handle conflicts and unknown types
        FIXTURE ONLY — existing or duplicate destinations are marked as
        conflicts and routed to `unsorted/`; unknowns already route there.
        Runtime proof: `tests/test_file_organizer.py` passed with 14 tests,
        including conflict routing and conflict-labelled dry-run output.
        GATE 2 closes here
- [x] 6. Execute moves based on schema
        FIXTURE ONLY — `--execute` moves planned files into schema folders and
        validates the resulting layout.
- [x] 7. Log every move and every skip
        `move_log.txt` is written after each execution and tested for complete
        move records.
- [x] 8. Validate result — post-move scan matches expected schema state
        FIXTURE ONLY — post-move validation rejects missing destinations or
        sources that were not moved. Runtime proof: organizer tests passed with
        17 tests and the full suite passed with 115 tests.
        GATE 3 closes here
- [x] 9. Add explicit confirmation step before any real move executes
        No spoken or typed input alone triggers a real move without this gate.
        Fixture-only `--execute` exits 2 unless the exact confirmation phrase
        is supplied; no default/classification/dry-run path moves files.
        Runtime proof: organizer tests passed with 17 tests, including blocked
        execution without confirmation and successful execution with the exact
        phrase.
        GATE 4 closes here — real directories may now be considered
- [x] 10. Connect speech input to a file organization command
        Spoken phrase is read from the bridge clipboard; an explicit organize
        command triggers dry-run only and cannot authorize execution.

---

## Not in scope yet

- Undo / rollback
- Cloud sync
- Any UI layer
- Real user directories (blocked until all four gates above are proven)

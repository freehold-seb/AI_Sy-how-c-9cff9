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
        Spoken/transcript input triggers fixture-only dry-run previews through
        `scripts/speech_file_organizer.py`; transcript execution requests and
        spoken confirmation phrases are blocked and cannot call the real move
        path. Runtime proof: organizer + speech tests passed with 22 tests, and
        repository smoke tests passed with 5 tests.

---

## Not in scope yet

- Undo / rollback
- Cloud sync
- Any UI layer
- Real user directories (blocked until all four gates above are proven)

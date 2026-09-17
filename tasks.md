# Task Backlog — Kepler / AI_Sy-do-th-126fe

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

## Backlog

Tasks are ordered by dependency. Pull from the top. One task per session.
Nothing moves to done without runtime output as proof.

- [x] 1. Scan a fixture directory and return a file list
        FIXTURE ONLY — script prints file names and extensions, no moves
- [x] 2. Classify scanned files by extension into named buckets
        FIXTURE ONLY — output maps each file to a category (image, doc, audio, etc.)
- [ ] 3. Define and write the folder schema
        Produce `schema.json` — maps each category to a target folder name
- [ ] 4. Dry-run mode — show planned moves without executing them
        FIXTURE ONLY — output lists what would move; nothing on disk changes
        GATE 1 closes here
- [ ] 5. Handle conflicts and unknown types
        FIXTURE ONLY — no silent overwrites; unknowns land in `unsorted/`
        GATE 2 closes here
- [ ] 6. Execute moves based on schema
        FIXTURE ONLY — files land in correct folders, confirmed by directory listing
- [ ] 7. Log every move and every skip
        `move_log.txt` written after each run, checked for completeness
- [ ] 8. Validate result — post-move scan matches expected schema state
        FIXTURE ONLY
        GATE 3 closes here
- [ ] 9. Add explicit confirmation step before any real move executes
        No spoken or typed input alone triggers a real move without this gate
        GATE 4 closes here — real directories may now be considered
- [ ] 10. Connect speech input to a file organization command
        Spoken phrase triggers dry-run only; transcript confirms intent before execution

---

## Not in scope yet

- Undo / rollback
- Cloud sync
- Any UI layer
- Real user directories (blocked until all four gates above are proven)

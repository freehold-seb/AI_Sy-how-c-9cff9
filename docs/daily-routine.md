# Daily routine

## Morning start

1. Open the canonical Kepler workspace in VS Code.
2. Run `Tasks: Run Task` -> `Daily Project Briefing`.
3. Open the generated report under `reports/`.
4. Start the bridge with `Tasks: Run Task` -> `OCHRE Bridge`.
5. Speak one real thought, problem, or decision.
6. Paste it into this chat with `TRANSLATE:` or `SAUCE:`.
7. Choose one actionable focus for the day.

Use [ai-tool-routing.md](ai-tool-routing.md) to decide whether a specialist tool is actually needed. Start with one lead tool and add one specialist only for a defined gap.

## Review format

The daily briefing answers:

- Where are we?
- What is working?
- What needs attention?
- What is the single biggest friction point?
- What is the smallest reversible improvement?
- What stays deferred?

## Boundaries

- The bridge transcribes; it does not add personality.
- Refinement happens in chat through `POLISH:`, `SAUCE:`, `ELABORATE:`, or `TRANSLATE:`.
- The briefing only reads workspace metadata; it writes exactly one dated
  report file per run under `reports/` and does not modify existing files.
  Set `DAILY_BRIEFING_DRY_RUN=1` to print the report instead of writing it.
- Generated reports are local working artifacts and are ignored by Git.
- One improvement per day is enough.
- Do not turn the daily briefing into an autonomous change loop.

## Recovery rule

If a new change makes the workflow worse, stop, record what changed, and return to the last known working workflow. Do not stack more changes on top of an unverified failure.

# AI operations baseline

Generated: 2026-09-15
Scope: current recovery workspace only; project baseline for all AI agents and contributors.

> Update: the "missing runner/verifier boundary" referenced below has since
> been restored (`runner/`, `verifier/`) and is covered by
> `tests/test_repo_smoke.py`. Kept for the historical record.

## Purpose

This file exists to reduce repeated handoff copy-paste, conflicting assumptions, and multi-AI drift. It is not a runtime feature. It is the operating baseline for every AI that joins the project.

## Canonical project rule

- One canonical handoff exists: `handoff.md`
- One designated owner manages the final canonical state
- Other AI systems may read, summarize, or propose edits, but they do not rewrite the project memory directly
- The project runs on a proof-first model: runtime behavior outranks planning or aspirational documentation
- Broad validation is deferred until the missing runner/verifier boundary is restored and validated in isolation
- The current working state is a fail-closed single-node recovery workspace

## Required AI operating model

### Single-threaded chain

```text
User -> lead AI -> canonical handoff -> specialist (only if needed) -> canonical handoff -> next action
```

The chain must remain one-way. No second AI should rewrite the same project state without returning to the canonical handoff.

### Required roles

- Microsoft Copilot: operational lead, repo synthesis, daily briefing, final handoff stewardship
- Gemini: historical context and cross-check against the canonical baseline only
- Perplexity: source-backed research only when a specific question needs external evidence
- ChatGPT: challenge and alternative phrasing only after the lead has defined the issue
- Local model: private or local runtime context only; not the live project source of truth

## Required response format for all AI agents

Before editing a file or recommending a plan, every AI must answer exactly this template:

```text
CONTRIBUTION:
- What did you do on this project, and which files or artifacts did you contribute?

CURRENT STATE:
- What is actually true right now without assuming missing components exist?

GOAL:
- What is the current project goal in plain language?

KNOWN GAPS:
- What is missing, deferred, or intentionally unimplemented?

NEXT HANDOFF:
- What is the single best next step or handoff to pass to the next agent?

RISK OF CONFUSION:
- What should not be assumed, and what could be mistaken if the wrong baseline is used?
```

## VS Code operating baseline

The repos and prompts should be configured to reduce friction, not to add more parallel complexity.

- Keep the canonical handoff in the repo root and use it as the default project starting point
- Keep the daily briefing task easy to run and obvious in the task list
- Keep prompting templates minimal and consistent
- Use a single lead AI per task and avoid parallel agent rewrites of the same files
- Do not add random settings that produce no proving behavior
- Prefer one clear workflow over multiple competing automation paths

## Safe automation rule

Only automate after verified behavior exists. Do not broaden validation before the missing runner/verifier boundary is restored and validated in isolation.

## Daily proof rule

Every day must answer these three questions explicitly:

1. What did we prove today?
2. What gap remains real?
3. What is the smallest reversible next step?

## Implementation target

The immediate goal is to keep the project in a fail-closed, single-node, proven workflow and reduce speculative work until a real runtime boundary is restored.

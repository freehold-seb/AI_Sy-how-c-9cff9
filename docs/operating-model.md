# Operating Model

## Source Of Truth

Git is the source of truth for shared, durable project state: code, configuration intended for the repository, decisions, handoffs, and validation evidence.

Do not commit secrets, machine-local configuration, caches, model weights, runtime logs, or ephemeral scratch files. Keep those outside the repository and document only the portable setup requirements.

## Cross-Machine Continuity

Move work between machines with:

- `repo-manifest.json`
- `handoff.md` when switching machines, pausing multi-step work, making risky changes, or transferring responsibility
- Git commits

Handoffs are concise status records, not chat transcripts. Before continuing handed-off work, read the manifest and handoff, fetch the expected repository state, check for uncommitted changes, and confirm that the next action is clear.

## Model Boundary

Models are interchangeable. Reliable behavior comes from small workflows, explicit contracts, handoffs, and validation rather than a particular model or a large permanent agent roster.

## Durable Roles

The steady-state roles are:

- Builder
- Debugger
- Security Reviewer
- Verification and Release

Recovery is a runbook or skill for recovery work, not a durable role. Use orchestration only when work spans multiple roles or machines.

## Current Boundaries

- No shared foundation repository until two repositories have used these artifacts successfully.
- No MCP profiles beyond the empty manifest allowlist until a server is introduced and reviewed.
- No automatic end-of-session handoffs. Create handoffs only when the continuity conditions above apply.
- Validation never authorizes destructive actions. Any future authorization must be explicit, scoped, and time-bound.

## Non-Goals

Do not introduce mega-agents, custom versioning systems, schemas, validators, registries, compatibility matrices, retry subsystems, or sync automation unless repeated real usage demonstrates a specific need.

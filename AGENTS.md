# AI_Sy-do-th-126fe Agent Guide

## Working agreement

- Treat Git as the source of truth for shared project state.
- Before changing code, read [README.md](README.md), [tasks.md](tasks.md), and [handoff.md](handoff.md) when they are relevant. Check the worktree with `git status --short --branch`.
- Make one focused change at a time. Preserve public contracts and prefer existing helpers over new abstractions.
- Do not edit unrelated user changes. Do not commit, push, tag, reset, or delete history unless explicitly requested.
- Keep secrets, credentials, private keys, payment details, model weights, generated logs, caches, and virtual environments out of Git.

## Safety boundaries

- This is a one-node recovery workspace. Do not assume the upstairs node, mesh sync, SSH, or cloud services are available or required.
- All file scanning, classification, move, and validation work must target disposable fixtures under `tests/fixtures/` only until every gate in [tasks.md](tasks.md) has independent runtime proof.
- Dry-run behavior, conflict handling, post-move validation, and explicit confirmation are separate gates. Validation never authorizes a destructive action.
- Do not work on the separate `freehold-web` repository from this worktree. See [handoff.md](handoff.md) for its location and current status.

## Project shape

- `verifier/` owns deterministic candidate and task validation.
- `runner/` owns pipeline orchestration and verifier integration.
- `agent_core/` owns configuration, introspection, and candidate hooks.
- `core/` and `services/` provide entrypoints and workers; `workflows/` delegates pipeline runs.
- `tests/` is the executable contract. Follow its fixture and naming patterns.

The project favors small workflows, explicit contracts, handoffs, and validation over model-specific behavior or large permanent registries. See [docs/operating-model.md](docs/operating-model.md).

## Validation

Run the narrowest relevant check first, then broaden when the change warrants it:

```powershell
python -m pytest tests/test_repo_smoke.py -q
python -m pytest -q
python -m compileall -q agent_core core runner services verifier workflows
git diff --check
```

Run commands from the workspace root. Record meaningful runtime proof in [handoff.md](handoff.md) when the task changes the handoff state; otherwise leave handoff content alone.

## Specialist routing

Use the existing custom agents for focused work:

- [Principal Builder](.github/agents/principal-builder.agent.md): implement a scoped Python or PowerShell change.
- [Debugger](.github/agents/debugger.agent.md): reproduce and isolate a failure.
- [Security Reviewer](.github/agents/security-reviewer.agent.md): inspect secrets, injection, permissions, or unsafe behavior.
- [Verification and Release](.github/agents/verification-release.agent.md): run acceptance checks and assess release readiness.
- [Recovery and Local Ops](.github/agents/recovery-ops.agent.md): recover local artifacts or maintain the one-node runtime.
- [Chief Orchestrator](.github/agents/chief-orchestrator.agent.md): coordinate work that genuinely spans roles or machines.

Use the existing [daily review skill](.github/skills/daily-review/SKILL.md) and [weekly PC assessment skill](.github/skills/weekly-pc-assessment/SKILL.md) for those workflows. Use [safe audit](.github/prompts/safe_audit.prompt.md) for a safety audit.

## Documentation sources

- [BASELINE.md](BASELINE.md): hardened baseline and invariants.
- [repo-manifest.json](repo-manifest.json): repository and recovery metadata.
- [docs/daily-routine.md](docs/daily-routine.md): normal local operating routine.
- [docs/ai-tool-routing.md](docs/ai-tool-routing.md): choosing tools and roles.

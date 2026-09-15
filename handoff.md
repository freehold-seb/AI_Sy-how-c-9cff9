# Handoff

Updated: 2026-09-15

## Purpose

This handoff is the shared source of truth for continuing work across Copilot, VS Code, and any other AI assistants. It records what is proven, what is incomplete, and what must happen next. Do not treat plans or documentation as proof of runtime behavior.

## Naming and organization rule

Keep names plain, stable, and easy to search. Do not rename or reorganize files just to make the structure look cleaner. Preserve an existing path unless its current name blocks understanding or use. New names should say what the file does in ordinary language. One clear file is better than several clever layers.

## Canonical operating rule

This project must operate on a proof-first, single-threaded model.

- One canonical handoff file exists for the project: `handoff.md`.
- One designated owner updates the final project memory; other AI systems may read, summarize, or propose edits but do not rewrite the canonical record.
- All incoming AI responses are folded into the master handoff, not treated as separate competing truths.
- Verified runtime behavior outranks documents, plans, or aspirational assumptions.
- The current recovery workspace is a partial snapshot; broader validation remains deferred until the restored runner/verifier boundary is validated in isolation.
- Fail-closed defaults remain in place until proven components exist and are validated in isolation.
- Each task must answer: what proof does this produce, what risk remains, and what is the next smallest reversible step?

## AI operating model

This project is intentionally single-threaded. One lead AI owns the decision for a task; one specialist can be added only for a defined gap. A second AI should not be allowed to edit the same file or re-interpret the same decision without returning to the canonical handoff.

### Lead tool and handoff chain

```text
User -> lead AI -> canonical handoff -> specialist (only if needed) -> canonical handoff -> next action
```

The chain must stay one-way. Do not allow multiple AI systems to write competing versions of the same project state at the same time.

### Required roles

- Microsoft Copilot: operational lead, repo synthesis, daily briefing, final handoff stewardship.
- Gemini: historical context and cross-check against the canonical baseline only.
- Perplexity: research with source-backed citations when needed.
- ChatGPT: challenge and alternative phrasing only after the lead has defined the issue.
- Local model: private or local runtime context only; it should not be treated as the live project source of truth.

### Required response format for all AI agents

Before any AI edits files or proposes a plan, it must answer:

- CONTRIBUTION: what work did you do, and which files or artifacts did you contribute?
- CURRENT STATE: what is true right now without assuming missing components exist?
- GOAL: what is the project goal in plain language?
- KNOWN GAPS: what is missing, deferred, or intentionally unimplemented?
- NEXT HANDOFF: what is the next single step or handoff to pass to the next agent?
- RISK OF CONFUSION: what should not be assumed, and what can be mistaken if the wrong baseline is used?

### Today’s execution rule

Today’s safe autonomous move is to validate the restored runner/verifier boundary while keeping orchestration disabled. No external action or broader automation is allowed until that focused validation passes.

## Executive status

The project is a personal service-tool workflow, not a consumer product. The working tool is a voice-to-text and refinement workflow. The larger multi-AI chain is a design direction, not an implemented autonomous system.

The project is currently in a partial recovery repository with structural drift. The voice bridge is useful and has produced real transcripts, but the bridge has a gap between transcription and refinement: the transcript must still be manually pasted into this chat with a mode label. That gap is intentional for now, but it is the next useful integration boundary.

## What is proven

### Voice bridge

[ochre_bridge.py](ochre_bridge.py) has been run on the current Windows machine. It has printed `Copied:` with spoken transcripts, proving:

```text
speech -> Whisper transcription -> clipboard
```

The bridge is intentionally neutral. It should capture speech faithfully and should not try to add personality, interpret intent, or choose another AI tool.

The bridge has also produced occasional `Nothing detected` results and repeated hallucinated phrases when silence filtering was disabled. Pre-roll, tail buffering, VAD, and release debouncing were added. The bridge is usable but not yet a perfect capture device.

### Refinement workflow

The working manual refinement path is:

```text
hold Right Ctrl -> speak -> release -> clipboard -> paste here with a mode -> assistant refines -> copy result -> use it
```

The current modes are:

- `TRANSLATE:` find what the speaker is trying to say and express it clearly
- `SAUCE:` make it sharp, intelligent, direct, and professionally confident without cruelty
- `POLISH:` clean grammar and filler while preserving meaning and voice
- `ELABORATE:` add structure, context, and useful detail

The bridge does not perform the refinement. The chat does.

### Repository hygiene

The workspace currently reports no editor diagnostics for the inspected files. This is not equivalent to a passing runtime test.

The repo now contains operating documents for the workflow, service boundary, daily routine, AI routing, and workspace map. These documents improve continuity but are not runtime features.

## What is not proven

- No autonomous multi-AI chain is running.
- No automatic handoff exists between Copilot, ChatGPT, Gemini, Perplexity, and the local model.
- No automatic morning startup is configured.
- The OCHRE Hub app is not a working foundation; its `AppSDK.ai.chat()` path previously returned 404 and must not be rebuilt casually.
- The current repo is not verified as a complete clone of the lost or previous system.
- The Windows network, firewall, Defender, installed software, startup programs, and system health have not yet been assessed under an approved read-only scope.

## The current bridge hole

The intended future chain is:

```text
voice capture
    -> intent translation
    -> task classification
    -> specialist work
    -> challenge and verification
    -> final synthesis
    -> human approval
    -> use or execute
```

What currently exists is only:

```text
voice capture -> clipboard -> manually paste into Copilot -> refinement
```

The missing middle is routing and handoff. Before automating it, prove the manual version on three real tasks and record where the handoff creates repeated friction.

## AI tool roles

- Microsoft Copilot: operational lead, daily briefing, Windows/Microsoft context, and final synthesis
- VS Code/GitHub Copilot: repository inspection, implementation, and validation
- Perplexity: current external research and citations
- ChatGPT: second-opinion challenge, blind spots, and alternative phrasing
- Gemini: Google-specific context or independent reasoning when relevant
- Local model: private material that should remain on the machine

Use one lead tool and add one specialist only for a defined gap. Do not ask every service the same question by default. Model agreement is not proof; tests, sources, and observed behavior outrank model preference.

## Repository topology

- Active recovery worktree: `AI_Sy-do-th-126fe`
- Seven additional sibling worktrees exist under the Kepler worktrees directory.
- A separate local repository exists at `C:\Users\SEB\kepler\repositories\freehold-web`.
- This repo is configured for single-node operation.
- The second node, mesh synchronization, and SSH are future or disabled work.

### Canonical workspace decision

`AI_Sy-do-th-126fe` is the canonical source of truth for this service-tool work.

All future edits, handoffs, proofs, and decisions should be anchored here unless a later handoff explicitly changes the decision. The other worktrees are unreviewed siblings or historical branches and must not be treated as active sources of truth. `freehold-web` remains a separate repository until its relationship to this service tool is explicitly decided.

## Current repo findings

- [workflows/run_verifier_pipeline.py](workflows/run_verifier_pipeline.py) now reaches a restored, bounded runner/verifier boundary: task specs load through `runner/run_verifier_pipeline.py`, candidates are checked by `verifier/`, and `runner/orchestrator_adapter.py` refuses routing while orchestration is disabled.
- [config/agent_config.json](config/agent_config.json) keeps orchestration disabled and `dry_run` set to true. The local runner/verifier boundary is restored, but external orchestration remains fail-closed until focused validation is confirmed.
- [verifier/__init__.py](verifier/__init__.py) is a compatibility layer because the original verifier submodules are absent from this snapshot.
- [core/agent.py](core/agent.py), [core/control_panel.py](core/control_panel.py), and [services/queue_worker.py](services/queue_worker.py) are minimal bootstrap stubs.
- [scripts/files/archive_old_files.ps1](scripts/files/archive_old_files.ps1) calls a missing `cleanup_and_sort.ps1`. Do not run it until its target is recovered and reviewed.
- Skill manifests describe several capabilities whose implementations and tests are not visible in this snapshot. Treat manifests as intentions, not available features.
- No files have been deleted or archived during this recovery work.

## Files added or updated for continuity

- [docs/service-tool-usage.md](docs/service-tool-usage.md)
- [docs/service-tool-framing.md](docs/service-tool-framing.md)
- [docs/project-roadmap-2026-09-15.md](docs/project-roadmap-2026-09-15.md)
- [docs/minimum-viable-workflow-2026-09-15.md](docs/minimum-viable-workflow-2026-09-15.md)
- [docs/real-vs-aspirational-2026-09-15.md](docs/real-vs-aspirational-2026-09-15.md)
- [docs/ochre-handoff-2026-09-15.md](docs/ochre-handoff-2026-09-15.md)
- [docs/workspace-map-2026-09-15.md](docs/workspace-map-2026-09-15.md)
- [docs/daily-routine.md](docs/daily-routine.md)
- [docs/ai-tool-routing.md](docs/ai-tool-routing.md)
- [docs/ai-service-flow.md](docs/ai-service-flow.md)
- [docs/proof-of-value-2026-09-15.md](docs/proof-of-value-2026-09-15.md)
- [scripts/daily_briefing.py](scripts/daily_briefing.py)
- [.vscode/tasks.json](.vscode/tasks.json)
- [runner/orchestrator_adapter.py](runner/orchestrator_adapter.py)
- [runner/run_verifier_pipeline.py](runner/run_verifier_pipeline.py)
- [verifier/verifier.py](verifier/verifier.py)
- [tests/test_repo_smoke.py](tests/test_repo_smoke.py)

## Daily routine

1. Open the canonical workspace in VS Code.
2. Run _Daily Project Briefing_ from `Tasks: Run Task`.
3. Read the generated local report under `reports/`.
4. Run _OCHRE Bridge_ from `Tasks: Run Task`.
5. Speak one real thought, problem, or decision.
6. Paste the transcript here with `TRANSLATE:` or `SAUCE:`.
7. Choose one actionable focus.
8. Record one friction point; do not start several improvements at once.

The daily briefing generator is read-only and scoped to the current workspace. Its first execution completed successfully and produced the dated report cited below.

## Next proof sequence

### Proof 1: daily briefing

Completed on 2026-09-15. Running `scripts/daily_briefing.py` created `reports/daily-briefing-2026-09-15.md` with the expected single-node posture and working-surface checks. The report recorded 92 total files, 27 Python files, and 26 Markdown files. This proves the briefing task executes and produces its local report; it does not prove the broader runtime is complete.

### Proof 2: restored runner/verifier boundary

The local boundary is implemented and editor diagnostics report no errors. `Run Verifier Tests` is available as a VS Code task and targets `tests/test_repo_smoke.py`. The pytest result is not recorded in this handoff until its output is available.

### Proof 3: one real service task

Use the bridge for a real thought or problem and submit it as:

```text
TRANSLATE: [raw transcript]
```

Confirm that the result identifies the actual point and produces a usable next action.

### Proof 4: one specialist

For a task that genuinely needs it, send a compact packet to one specialist, then bring the result back for synthesis:

```text
INTENT: What is the user trying to accomplish?
CONTEXT: What facts matter?
CONSTRAINTS: What must not happen?
QUESTION: What should the specialist answer?
```

### Proof 5: one bounded automation

Only after three manual runs work should we automate one repeated handoff. The automation must be reversible, observable, and paused before external sending, deletion, system changes, or other irreversible actions.

## Stop conditions

- Do not rebuild the Hub around the known 404 path.
- Do not run deletion, archiving, mesh, or SSH scripts without review.
- Do not enable autonomous external actions.
- Do not treat a document, plan, or model answer as runtime proof.
- If debugging exceeds 30 minutes, use the manual fallback and preserve the last known good workflow.
- If tools disagree, surface the disagreement rather than averaging it away.

## Open decisions

- Is `freehold-web` part of this service tool or a separate project?
- Which one repeated manual handoff is worth automating first?
- What Windows/system audit scope should be approved beyond the repository?

## Closed decisions

- Verified behavior only: no broader validation pass until the restored runner/verifier boundary is validated in isolation.
- The canonical working scope is the current recovery workspace, not the historical full-system state.
- The project is intentionally fail-closed: local routing and verification may be tested, but external orchestration remains disabled.

## AI onboarding protocol

Any AI joining the project should answer these six questions before editing files or proposing a plan:

- CONTRIBUTION: What did you do on this project, and which files or artifacts did you contribute?
- CURRENT STATE: What is the actual project state right now, without assuming missing components exist?
- GOAL: What is the current project goal in plain language?
- KNOWN GAPS: What is missing, unverified, or intentionally deferred?
- NEXT HANDOFF: What is the single best next step or handoff to pass to the next agent?
- RISK OF CONFUSION: What should not be assumed, and what could be mistaken if the wrong baseline is used?

This protocol prevents multi-agent drift and keeps the conversation anchored to the canonical handoff.

## Request for Microsoft Copilot

Use this handoff as the current source of truth. Do not assume that planned files, documented workflows, or declared capabilities are implemented. Separate every response into facts, inferences, open questions, and recommended actions.

Please answer these questions:

1. Does the current daily briefing task run successfully and create a dated report under `reports/`?
2. Is the current manual service loop useful enough for three real tasks, and what friction appears in each run?
3. What is the smallest safe change that would close one part of the gap between clipboard transcription and AI refinement?
4. Which AI tool should lead that next step, and which specialist, if any, should be added?
5. Does `freehold-web` belong to this service tool, or should it remain a separate project?
6. Should orchestration stay disabled until the missing runner/verifier implementation is restored?
7. What evidence supports each answer, and what remains unverified?

Return the response in this format:

```text
FACTS:
- ...

INFERENCES:
- ...

OPEN_QUESTIONS:
- ...

RECOMMENDED_ACTIONS:
1. ...

VALIDATION:
- What was actually run or observed
- What was not run or observed
```

Do not delete, archive, rename, or move files. Do not enable autonomous external actions. Do not rebuild the Hub around `AppSDK.ai.chat()`. Any proposed code change must include a focused validation command and an observable acceptance criterion.

## Current Copilot assessment

### Facts

- `ochre_bridge.py` has produced real `Copied:` transcripts; speech-to-clipboard is proven.
- `scripts/daily_briefing.py` has been reported as run successfully once; the dated report exists in `reports/`.
- Two real `TRANSLATE:`/`SAUCE:` refinement runs are recorded in this conversation.
- `AI_Sy-do-th-126fe` is the canonical worktree.
- Live `config/agent_config.json` confirms `dry_run: true` and `orchestrator_enabled: false`.
- `scripts/files/archive_old_files.ps1` references missing `cleanup_and_sort.ps1` and is unsafe to run.
- The local runner/verifier boundary exists but remains deferred and focused pytest output is not recorded here.

### Inferences

- The main recurring friction is context fragmentation across AI sessions, not bridge proof or mode labeling.
- The smallest safe transcript-to-refinement improvement remains a reversible clipboard helper, but it is deferred until the current baseline is stable.
- `freehold-web` should remain separate until a read-only inspection establishes a relationship.

### Open questions

- Has any Windows scheduled task for `daily_briefing.py` been registered?
- What does `freehold-web` contain?
- Which deferred tools, if any, should be promoted after focused validation?

### Recommended actions

1. Keep the active baseline limited to `ochre_bridge.py`, `scripts/daily_briefing.py`, and `.vscode/tasks.json`.
2. Keep orchestration disabled and do not run archive, mesh, SSH, or other system-changing scripts.
3. Run `Run Verifier Tests` and record its actual pytest output before promoting the runner/verifier boundary.
4. Read `freehold-web` read-only before deciding whether it belongs to this service tool.

### Validation

- Observed: `Copied:` bridge output, two refinement runs, the dated daily briefing report, and live fail-closed config values.
- Not observed: scheduled-task registration output, focused pytest output, `freehold-web` contents, or a clean post-patch bridge recording.

## Friction log

1. Bridge proof was requested repeatedly after it was already documented. Root cause: absence of a new terminal paste was incorrectly treated as absence of proof. Fix: treat the canonical handoff as authoritative for already-closed evidence.
2. Config values were previously cited from handoff text rather than the live file. Fix: verify config directly before asserting runtime state.
3. Context fragmentation caused repeated re-establishment of decisions. Fix: begin each new AI session by reading `handoff.md`.

## Next-agent script reduction packet

```text
INTENT: Identify which scripts are part of the active baseline versus deferred or unsafe.
CONTEXT: Active baseline is exactly ochre_bridge.py, scripts/daily_briefing.py, and .vscode/tasks.json.
CONSTRAINTS: Do not delete, archive, move, or run any file. Read directory listings and file headers only.
QUESTION: List every file in scripts/ and every root-level .py file. Classify each as ACTIVE, DEFERRED, or REVIEW-BEFORE-RUN. Write the decision to docs/script-audit-2026-09-15.md.
```

## Historical Microsoft Copilot response

The following response is a historical snapshot from before the local runner/verifier boundary and daily briefing proof were completed. Its observations are retained for traceability but do not override the current sections above.

Date: 2026-09-15

### Confirmed facts

- The bridge has produced real `Copied:` transcripts.
- The bridge patch has not yet been confirmed by a clean post-patch recording.
- `scripts/daily_briefing.py` and `.vscode/tasks.json` exist, but the daily briefing task has not yet been run and no report has been observed under `reports/`.
- `AI_Sy-do-th-126fe` is the canonical worktree.
- The manual bridge-to-chat loop has not yet been completed for three real tasks.

### Assessment

- The daily briefing is low risk to try because it is intended to be read-only and workspace-scoped, but that remains an inference until it runs successfully.
- The most likely repeated manual friction is typing the mode label before pasting the transcript.
- `freehold-web` should remain separate until a read-only inspection proves a relationship.
- Orchestration should remain disabled until `runner.run_verifier_pipeline` exists and is validated.

### Actions taken from that response

- Set `orchestrator_enabled` to `false`.
- Set `dry_run` to `true` in [config/agent_config.json](config/agent_config.json).
- Added [scripts/prepare_prompt.py](scripts/prepare_prompt.py) and four VS Code tasks to prepare `TRANSLATE:`, `SAUCE:`, `POLISH:`, or `ELABORATE:` prompts from the clipboard without sending or modifying external systems.
- Added [scripts/workspace_inventory.py](scripts/workspace_inventory.py) and the _Inventory Related Workspaces_ task. It reports metadata for the canonical worktree, sibling worktrees, and `freehold-web` without modifying them.
- Focused validation passed: `python -m py_compile ...` completed successfully and `python -m pytest -q tests\\test_repo_smoke.py` reported `2 passed`.

This is a fail-closed configuration change. It does not restore the missing runner; it prevents incomplete orchestration from being treated as active.

### Still required

1. Run the _Daily Project Briefing_ task and confirm a dated report exists.
2. Run one clean recording with the patched bridge.
3. Complete three real manual `TRANSLATE:` or `SAUCE:` runs and record friction.
4. Inspect `freehold-web` read-only before deciding its relationship to this repo.
5. Run `python scripts\\workspace_inventory.py` and review `reports/workspace-inventory.md` before any synchronization decision.

## Safety and privacy boundary

Do not inspect or transmit browser profiles, saved sessions, passwords, private keys, tokens, `.env` files, personal communications, medical/legal/financial documents, or payment data as part of routine project work. Keep sensitive material local unless the user explicitly approves a specific service and purpose.

## Bottom line

The useful thing currently exists, but it is smaller than the imagined system: voice capture plus manual AI refinement. The next honest milestone is not a larger architecture. It is three observable service runs, one specialist handoff, and one measured improvement to the bridge between them.

## Final visible-test summary

The manual bridge loop has now been demonstrated and understood:

```text
hold Right Ctrl -> speak -> release -> bridge transcribes -> clipboard receives text -> type TRANSLATE: -> paste transcript into this chat -> assistant clarifies it -> user reviews and uses the result
```

Observed evidence:

- The bridge loaded the Whisper model and reached `Model ready.`
- The bridge printed multiple real `Copied:` transcripts from spoken input.
- The clipboard-to-chat step was demonstrated with a `TRANSLATE:` prompt.
- The assistant converted the raw spoken explanation into a clear description of the workflow.
- The daily briefing script ran successfully and created `reports/daily-briefing-2026-09-15.md`.
- The briefing reported the expected working surface: bridge, service guide, smoke test, and handoff.
- The workspace remains in single-node mode.

Observed limitations:

- The bridge has intermittently printed `Nothing detected` and has produced repeated hallucinated phrases when VAD was disabled.
- The pre-roll, tail buffer, VAD, and release-debounce changes are present, but a clean post-patch recording is still the remaining bridge validation.
- The manual mode-label paste remains the middle gap. No automatic routing or refinement handoff exists.
- No autonomous multi-AI chain has been implemented or validated.

This is enough to prove the service-tool concept at its current level. It does not prove the future autonomous chain.

## Safe autonomous candidate

The first autonomous task should be a read-only daily workspace briefing:

```text
inspect current workspace metadata -> write dated local report -> stop
```

Implementation: [scripts/daily_briefing.py](scripts/daily_briefing.py), launched by the _Daily Project Briefing_ VS Code task.

Allowed behavior:

- read selected workspace files and metadata
- report runtime posture and working-surface presence
- count files and list recent workspace changes
- write a dated report under `reports/`

Forbidden behavior:

- edit source or configuration
- delete, rename, move, or archive files
- send messages or upload data
- inspect credentials, browser data, or personal documents
- enable orchestration or invoke external AI services

The task is safe to leave running only after its execution behavior is independently confirmed. At present it has been run once successfully, but no Windows schedule has been configured. Scheduling it would be a separate explicit decision.

## Away-mode acceptance criteria

Before allowing any background task to run while the user is away:

1. It performs no mutation beyond its own local report output.
2. It uses no network or external AI service.
3. It records a timestamp and clear scope.
4. It fails without blocking or modifying the working system.
5. It can be disabled through one obvious task or command.

The daily briefing meets the intended design on paper and has passed one manual run. It is the only current candidate suitable for further bounded automation.

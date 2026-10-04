# Recovered memory subsystem

This report was first committed on 2026-10-01. It describes a recovered source snapshot, but the original inspection date, source repository/remote, and immutable source commit were not preserved. The original workspace's Git metadata was reported unreadable, so the source and branch claims below are historical, unpinned observations that cannot be independently reproduced. They do not establish functionality available or validated in this checkout.

One reported detail is that the root `memory_service.py` was a compatibility launcher, while the implementation lived in `services/memory_service.py`.

## What the recovered source appeared to do

The described subsystem was the repo’s long-term memory for the assistant. It appeared to do three jobs:

1. **Collected outside context**: files dropped into `imports/` were treated as incoming memory material.
2. **Stored durable memory**: the useful pieces were deduplicated and written into a local SQLite database.
3. **Injected memory back into prompts**: when the orchestrator or behavior engine built a model prompt, it asked the memory system for a short “relevant memory” pack and inserted that text into the context.

In plain language: it was intended as a local notebook with a filter. It watched for new context, trimmed it into short facts/preferences/summaries, stored it, and then fed matching pieces back into later AI calls.

## How the recovered source described its wiring

The described flow was:

1. `setup_AI_System.ps1` creates `memory_service.py` and registers a scheduled task named `Project-Rutabaga_MemoryService`.
2. `services/service_watchdog.py` knows about the memory service and supervises it like the other background services.
3. `services/memory_service.py` starts a `MemoryBridge` and loops forever, calling `sync_imports()`.
4. `MemoryBridge` scans `imports/`, parses supported files, optionally moves processed files into `imports/processed/`, and hands parsed records to `MemoryManager`.
5. `MemoryManager` writes the durable records to SQLite and updates `config/learned_preferences.json` when repeated preferences become strong enough to promote.
6. `core/orchestrator.py` and `modules/behavior_engine.py` ask `MemoryManager` for memory-pack output and splice relevant memory into prompts. `modules/capture_bridge.py` exposes a `routing_pack()` context lookup for capture-related callers, but does not itself inject text into a model prompt.

There is also a one-off import path from `scripts/system/pull_downstairs_context.ps1`, which writes a snapshot into `imports/` and then calls `MemoryBridge().sync_imports()`.

## Storage described in the recovered source

The recovered source described live and legacy storage across these paths:

| Path | Purpose | Reported status in recovered snapshot |
|---|---|---|
| `data/system.db` | Main SQLite database for `facts`, `notes`, `preferences`, and `summaries` | Described as active |
| `config/learned_preferences.json` | Promoted rules and promotion history | Described as active |
| `config/memory_bridge.json` | Bridge settings like watched extensions, archive behavior, and file-size limit | Described as active |
| `commands/memory_bridge_state.json` | Seen-file tracking for import de-duplication | Described as active state |
| `imports/` | Incoming memory files waiting to be parsed | Described as active |
| `imports/processed/` | Archive for files already imported | Described as active if archiving is enabled |
| `exports/` | Exported memory bundles | Described as active |
| `config/dispatch_preferences.json` | Success/failure counters for dispatch method ordering | Described as active, but separate from memory content |
| `logs/agent_dispatch.log` / `logs/memory_service.log` | Operational logs | Described as active |
| `commands/memory.json.bak` | Old JSON-format memory dump | Legacy backup, not part of the active flow |

The report described `commands/memory.json.bak` as a legacy format rather than the live source of truth; that behavior is not verified in this checkout.

## Features reported in recovered source vs. paths described as dead or brittle

The items below were reported in the recovered source and configuration. The implementations and supporting scripts are not present in this checkout, so none of these features is available or validated here.

**Reported as implemented in the recovered source**

- The SQLite-backed `MemoryManager`.
- Importing `.txt`, `.md`, `.log`, `.json`, and `.csv` files through `MemoryBridge`.
- Deduplication and summary creation.
- Preference promotion when the same preference repeats often enough.
- Prompt enrichment through `routing_pack()` / `context_pack()`.
- The handoff mirror sync tooling in `scripts/system/sync_handoffs.py`.

**Described as dead, brittle, or machine-specific**

- Many scripts and docs hardcode `C:\AI_System`, `C:\Users\<username>`, and `G:\...`.
- The current machine has no `D:` or `G:` drive, so those paths will fail here unless rewritten.
- The personal-branch files also assume paths like `C:\Users\<username>\Downloads\...` and `C:\Users\<username>\.copilot\repos\ai_system`.
- `show-memory-report.py` is just a RAM/process report; it is unrelated to the memory subsystem despite the name.
- `memory_service.py` at repo root is only a shim now; if someone expects the implementation there, they will look in the wrong place.

## What might be worth reviving

If rebuilding a memory feature for the current project, these are the pieces I would consider:

1. **`MemoryManager.routing_pack()` + the prompt injection hooks**  
   This was described as the part that could turn past facts and preferences into context for future AI calls.

2. **`MemoryBridge.sync_imports()`**  
   This was described as the ingestion bridge for external exports, notes, and snapshots.

3. **`learn()` / `compact()` / `promote_preferences()`**  
   These were described as the “memory quality” layer for deduplicating repeated statements, summarizing them, and promoting repeated preferences.

What I would *not* revive as-is: the hardcoded paths, the legacy `.bak` memory dump, and the old machine-specific backup choreography. Those should be retooled around the SQLite store and config-driven paths, not copied back verbatim.

## Personal branches

The recovered snapshot reportedly had `mom-personal` and `sebastian-personal` at the same tip commit, making them effectively the same snapshot. Both were described as closer to a personal workstation image than to `master`.

At a high level, they add or carry:

- Personal workflow agents and instructions under `.github/`.
- Backup, training, maintenance, and desktop/file-management scripts.
- Large model and training artifacts.
- Workspace-specific cleanup and automation docs.
- A lot of absolute path assumptions for the original machine.

Sensitive path patterns found there include:

- `C:\AI_System`
- `C:\Users\<username>`
- `C:\Users\<username>\Downloads\...`
- `C:\Users\<username>\.copilot\repos\ai_system`
- `G:\...`

## Quick fix/perf branch census

The statuses below are historical ancestry claims from the recovered snapshot, not a live status check. “Not merged” does not imply that a branch was abandoned.

| Branch | What it fixed / changed | Status |
|---|---|---|
| `fix/backend-venv-detection` | Selected the interpreter that actually had `uvicorn` installed | Not merged |
| `fix/continuous-mesh-sync` | Added fail-closed continuous mesh sync | Merged |
| `fix/emergency-sync-conflict-markers` | Removed accidental merge-conflict markers left by emergency sync | Not merged |
| `fix/mesh-self-target-verification` | Recorded daemon-level SSH restrictions for self-target verification | Merged |
| `fix/mesh-verifier-configured-key` | Made the mesh verifier use the configured key | Merged |
| `fix/node2-safe-launch-bom` | Handled BOM-prefixed Python files in upstairs preflight | Merged |
| `fix/repo-audit-remediation` | Landed the final mesh handoff / audit remediation summary | Merged |
| `perf/json-load-cache` | Saved local testing state; not really a runtime performance change | Merged |
| `perf/native-clipboard` | Switched clipboard management to native Win32 ctypes for speed | Merged |
| `perf/non-blocking-cpu-percent` | Made CPU measurement non-blocking | Merged |
| `perf/optimize-memory-duplicate-detection` | Tightened duplicate-detection memory logic and fixed missing imports | Not merged |
| `perf/replace-bucket-executemany` | Bulk-inserted memory bucket replacements with `executemany` | Merged |

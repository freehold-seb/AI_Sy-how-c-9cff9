# Recovered memory subsystem

I traced the live memory/context path in `recovered/master`. One important correction: the root `memory_service.py` is only a compatibility launcher; the real service implementation lives in `services/memory_service.py`.

## What it actually did

This subsystem was the repo’s long-term memory for the assistant. It did three jobs:

1. **Collected outside context**: files dropped into `imports/` were treated as incoming memory material.
2. **Stored durable memory**: the useful pieces were deduplicated and written into a local SQLite database.
3. **Injected memory back into prompts**: when the orchestrator or behavior engine built a model prompt, it asked the memory system for a short “relevant memory” pack and inserted that text into the context.

In plain language: it was a local notebook with a filter. It watched for new context, trimmed it into short facts/preferences/summaries, stored it, and then fed the best matching pieces back into later AI calls.

## How it was wired up

The active flow was:

1. `setup_AI_System.ps1` creates `memory_service.py` and registers a scheduled task named `Project-Rutabaga_MemoryService`.
2. `services/service_watchdog.py` knows about the memory service and supervises it like the other background services.
3. `services/memory_service.py` starts a `MemoryBridge` and loops forever, calling `sync_imports()`.
4. `MemoryBridge` scans `imports/`, parses supported files, optionally moves processed files into `imports/processed/`, and hands parsed records to `MemoryManager`.
5. `MemoryManager` writes the durable records to SQLite and updates `config/learned_preferences.json` when repeated preferences become strong enough to promote.
6. `core/orchestrator.py` and `modules/behavior_engine.py` ask `MemoryManager` for memory-pack output and splice relevant memory into prompts. `modules/capture_bridge.py` exposes a `routing_pack()` context lookup for capture-related callers, but does not itself inject text into a model prompt.

There is also a one-off import path from `scripts/system/pull_downstairs_context.ps1`, which writes a snapshot into `imports/` and then calls `MemoryBridge().sync_imports()`.

## What storage it used

The live and legacy storage is split across a few places:

| Path | Purpose | Status |
|---|---|---|
| `data/system.db` | Main SQLite database for `facts`, `notes`, `preferences`, and `summaries` | Active |
| `config/learned_preferences.json` | Promoted rules and promotion history | Active |
| `config/memory_bridge.json` | Bridge settings like watched extensions, archive behavior, and file-size limit | Active |
| `commands/memory_bridge_state.json` | Seen-file tracking for import de-duplication | Active state file |
| `imports/` | Incoming memory files waiting to be parsed | Active |
| `imports/processed/` | Archive for files already imported | Active if archiving is enabled |
| `exports/` | Exported memory bundles | Active |
| `config/dispatch_preferences.json` | Success/failure counters for dispatch method ordering | Active, but separate from memory content |
| `logs/agent_dispatch.log` / `logs/memory_service.log` | Operational logs | Active |
| `commands/memory.json.bak` | Old JSON-format memory dump | Legacy backup, not part of the active flow |

The old JSON memory format is still visible in `commands/memory.json.bak`, but the live system no longer reads that file as its source of truth.

## What remains implemented vs. what is dead

The items below are present in the recovered source and configuration; the repository handoff says that source presence alone is not proof of current runtime health.

**Implemented in the recovered source**

- The SQLite-backed `MemoryManager`.
- Importing `.txt`, `.md`, `.log`, `.json`, and `.csv` files through `MemoryBridge`.
- Deduplication and summary creation.
- Preference promotion when the same preference repeats often enough.
- Prompt enrichment through `routing_pack()` / `context_pack()`.
- The handoff mirror sync tooling in `scripts/system/sync_handoffs.py`.

**Dead, brittle, or machine-specific**

- Many scripts and docs hardcode `C:\AI_System`, `C:\Users\smcca`, and `G:\...`.
- The current machine has no `D:` or `G:` drive, so those paths will fail here unless rewritten.
- The personal-branch files also assume paths like `C:\Users\smcca\Downloads\...` and `C:\Users\smcca\.copilot\repos\ai_system`.
- `show-memory-report.py` is just a RAM/process report; it is unrelated to the memory subsystem despite the name.
- `memory_service.py` at repo root is only a shim now; if someone expects the implementation there, they will look in the wrong place.

## What is worth reviving

If the goal is to make the current AI tooling better right now, these are the pieces I would keep:

1. **`MemoryManager.routing_pack()` + the prompt injection hooks**  
   This is the highest-value part. It turns past facts and preferences into live context for future AI calls.

2. **`MemoryBridge.sync_imports()`**  
   This is the ingestion bridge. It lets the system absorb external exports, notes, and snapshots instead of starting from zero every session.

3. **`learn()` / `compact()` / `promote_preferences()`**  
   This is the real “memory quality” layer. It deduplicates repeated statements, summarizes them, and turns repeated preferences into durable rules.

What I would *not* revive as-is: the hardcoded paths, the legacy `.bak` memory dump, and the old machine-specific backup choreography. Those should be retooled around the SQLite store and config-driven paths, not copied back verbatim.

## Personal branches

`mom-personal` and `sebastian-personal` point to the same tip commit, so they are effectively the same snapshot. Both are much closer to a personal workstation image than to `master`.

At a high level, they add or carry:

- Personal workflow agents and instructions under `.github/`.
- Backup, training, maintenance, and desktop/file-management scripts.
- Large model and training artifacts.
- Workspace-specific cleanup and automation docs.
- A lot of absolute path assumptions for the original machine.

Sensitive path patterns found there include:

- `C:\AI_System`
- `C:\Users\smcca`
- `C:\Users\smcca\Downloads\...`
- `C:\Users\smcca\.copilot\repos\ai_system`
- `G:\...`

## Quick fix/perf branch census

Merged status is based on ancestry in `master` at the recovered remote tip.

| Branch | What it fixed / changed | Status |
|---|---|---|
| `fix/backend-venv-detection` | Selected the interpreter that actually had `uvicorn` installed | Abandoned / not merged |
| `fix/continuous-mesh-sync` | Added fail-closed continuous mesh sync | Merged |
| `fix/emergency-sync-conflict-markers` | Removed accidental merge-conflict markers left by emergency sync | Abandoned / not merged |
| `fix/mesh-self-target-verification` | Recorded daemon-level SSH restrictions for self-target verification | Merged |
| `fix/mesh-verifier-configured-key` | Made the mesh verifier use the configured key | Merged |
| `fix/node2-safe-launch-bom` | Handled BOM-prefixed Python files in upstairs preflight | Merged |
| `fix/repo-audit-remediation` | Landed the final mesh handoff / audit remediation summary | Merged |
| `perf/json-load-cache` | Saved local testing state; not really a runtime performance change | Merged |
| `perf/native-clipboard` | Switched clipboard management to native Win32 ctypes for speed | Merged |
| `perf/non-blocking-cpu-percent` | Made CPU measurement non-blocking | Merged |
| `perf/optimize-memory-duplicate-detection` | Tightened duplicate-detection memory logic and fixed missing imports | Abandoned / not merged |
| `perf/replace-bucket-executemany` | Bulk-inserted memory bucket replacements with `executemany` | Merged |

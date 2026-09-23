# AI System

This is a fresh Git repository created from the files that were readable from
the previous workspace on 2026-09-10.

The original workspace remains preserved separately for recovery. Its Git
metadata and some files currently fail with a Windows device I/O error, so
this checkout is a partial snapshot rather than a verified full clone.

## Current deployment topology

This is currently a one-node system. The upstairs node has not been
reassembled yet and must not be treated as reachable or required for local
operation. Mesh synchronization and second-node SSH setup remain future work.

## Setup

This project targets Python 3.12.

1. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

2. Install dependencies for the task at hand:

   - Running or reviewing the smoke tests / CI only:

     ```powershell
     pip install -r requirements-dev.txt
     ```

   - Working on the full runtime (voice bridge, service, etc.), which also
     needs the test dependencies above:

     ```powershell
     pip install -r requirements.txt -r requirements-dev.txt
     ```

## Smoke test

The smoke suite (`tests/test_repo_smoke.py`) checks that the core entrypoints
import cleanly and that the runner/verifier boundary behaves as documented.
It only needs the standard library plus `requirements-dev.txt`:

```powershell
pytest tests/test_repo_smoke.py -q
```

This same command runs in CI via [`.github/workflows/smoke.yml`](.github/workflows/smoke.yml)
on every push and pull request.

## Recovery notes

- Do not copy credentials, `.env` files, private keys, or payment details into
  this repository.
- Keep generated logs, model weights, virtual environments, and local runtime
  state outside Git.
- Add the intended new GitHub remote only after confirming the correct account
  and repository.

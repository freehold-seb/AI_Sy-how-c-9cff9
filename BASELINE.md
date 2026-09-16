# Hardened Pipeline Baseline - September 16, 2026

## Validation Summary

- Full test suite: 47 passed
- Config schema validation: active
- Verifier decision logging: active
- TaskSpec schema enforcement: active
- Dry-run isolation: active
- Python `compileall`: passed
- JSON parsing: 24 files parsed successfully
- Workspace diagnostics: no errors in touched files

## Included Hardening

1. **Config schema validation**
   - Enforces the real nine-key configuration contract.
   - Rejects missing keys, unknown keys, and incorrect types.

2. **Verifier decision logging**
   - Emits structured events for acceptance, rejection, non-finite scores,
     selection, and empty fallback.
   - Preserves verifier return values and selection behavior.

3. **TaskSpec schema enforcement**
   - Requires a non-empty `task_id` or legacy `id` and a non-empty `objective`.
   - Allows optional `input` with its existing flexible type.
   - Rejects unknown fields and ambiguous dual IDs.

4. **Dry-run isolation**
   - Emits an explicit dry-run block event.
   - Skips candidate selection while dry-run is enabled.
   - Preserves normal-mode behavior.

## Baseline Notes

This documents the fully hardened pipeline state before the baseline commit and
tag. Serena setup files are intentionally kept separate from this baseline.

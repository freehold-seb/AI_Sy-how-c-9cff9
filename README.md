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

## Recovery notes

- Do not copy credentials, `.env` files, private keys, or payment details into
  this repository.
- Keep generated logs, model weights, virtual environments, and local runtime
  state outside Git.
- Add the intended new GitHub remote only after confirming the correct account
  and repository.

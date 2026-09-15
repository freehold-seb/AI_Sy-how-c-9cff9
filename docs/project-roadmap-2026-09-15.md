# Minimum viable project roadmap

## Goal

Keep the ambition, but make the system prove itself in layers.

## Phase 1: repo stability

Target outcome: the workspace loads without missing-module churn and the active runtime path is clear.

Required actions:

- keep the compatibility layer in [verifier/__init__.py](../verifier/__init__.py)
- treat this repo as a recovery workspace, not a full production clone
- decide the active repo boundary before adding new features
- do not add new orchestration or build layers until imports are stable

Definition of done:

- `import agent` works
- `import control_panel` works
- `import core.queue_worker` works
- `import services.queue_worker` works
- `import verifier` works

## Phase 2: voice workflow proof

Target outcome: the system reliably converts speech into refined output using the simplest working loop.

Required actions:

- use Voice Access for dictation
- paste text into Copilot with a mode label
- use one of these labels:
  - POLISH:
  - ELABORATE:
  - SAUCE:
  - TRANSLATE:
- copy the refined output and drop it into the target destination

Definition of done:

- one real dictation flow is repeatable
- one mode is consistently useful
- output quality is enough to trust the flow daily

## Phase 3: optional expansion

Only after Phase 1 and Phase 2 are stable should we revisit:

- the Hub
- OCHRE bridge
- deeper pipeline automation
- more advanced orchestration

Definition of done:

- the expansion fills a real gap
- the current phase remains stable while the new layer is added

## Hard rule

No new system layer without proof that the previous layer works.

## Daily rule

Every work session must answer two questions:

1. What is the smallest working proof we are validating today?
2. What is the next smallest step after that?

---
name: daily-review
description: "Use when: the user requests a daily review, recap, summary, planning review, project status, or an honest assessment of what is going well and what needs work."
argument-hint: "Conversation notes or topics to review"
---

# Daily Review

Produce an honest, structured review of the information the user supplied in the current conversation. This is an on-demand planning skill, not an always-on policy or a canonical baseline.

## Scope

1. Use only text the user provided in the conversation unless they explicitly authorize another source.
2. Do not assume access to voice calls, transcripts, files, cloud storage, automation, or other repositories.
3. Do not inspect files or run commands merely because this skill was invoked.
4. Do not assume multi-repository adoption, a completed validation trial, or a canonical baseline beyond the current repository.
5. Reference the operating model, repository manifest, or handoff only when they are relevant to alignment, consistency, gaps, or next actions.

## Reasoning Rules

Separate every conclusion into one of these categories:

- **Facts:** explicitly stated or confirmed by the user.
- **Inferences:** reasonable interpretations; state the basis and avoid presenting them as facts.
- **Open questions:** missing information that materially affects a decision.
- **Recommended actions:** concrete next steps derived from the facts and stated constraints.

Ask a clarifying question only when ambiguity affects a destructive operation, security-sensitive decision, irreversible change, or baseline integrity. For small, safe ambiguities, make the most reasonable interpretation and label it as an inference.

Do not invent accomplishments, risks, dependencies, decisions, or validation results. Do not use praise as filler.

## Review Workflow

1. Extract the stated goals, decisions, concerns, constraints, and unresolved items.
2. Compare them with applicable existing artifacts only when their content was supplied or is already available in the active conversation.
3. Identify genuine progress, functional but incomplete work, required corrections, and work that should be avoided or removed.
4. Turn the material items into a short prioritized task list. Each task needs a priority, one action, and observable acceptance criteria.
5. Flag uncertainty and ask only the necessary follow-up questions.

## Output Format

Use these sections, omitting any section that has no grounded content:

1. **What’s Going Well**
2. **What’s Okay but Needs Attention**
3. **What Needs to Change**
4. **What Must Go**
5. **Task List**

For each task, use:

- **Priority:** High, Medium, or Low
- **Action:** one concrete next step
- **Acceptance criteria:** what observable result completes it

Keep the review concise enough to act on. Recommendations must not introduce premature automation, multi-agent expansion, governance artifacts, or irreversible operations beyond the user's explicit direction.

## Completion Checks

Before responding, verify that:

- Every substantive statement is a fact, labeled inference, open question, or recommendation.
- No private source or unprovided content was assumed.
- Any destructive or security-sensitive ambiguity is surfaced as a question.
- Each listed task has priority and acceptance criteria.
- The review does not claim that a canonical baseline, multi-repository adoption, or automation exists unless explicitly established.

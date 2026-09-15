# AI tool routing

## Principle

Use the tools as a small service team, not as four copies of the same assistant.

One tool owns the task. Other tools are invited only for a specific reason. The final answer is synthesized once, with conflicts made visible.

## Roles

### Microsoft Copilot - operational lead

Use for:

- the daily briefing
- current task context
- Windows and Microsoft workflow questions
- turning the day's raw thoughts into an actionable plan
- final synthesis when the task is connected to this workspace

### VS Code and GitHub Copilot - implementation lead

Use for:

- inspecting and editing this repository
- running focused validation
- tracing code paths
- making small reversible changes

Do not use it as the general research panel when no code is involved.

### Perplexity - cited external research

Use for:

- current documentation
- product comparisons
- current software or hardware information
- claims that need links and source checking

Do not send private project details unless they are necessary and safe to disclose.

### ChatGPT - second-opinion challenger

Use for:

- challenging a plan
- finding blind spots
- comparing approaches
- editorial transformation or alternative phrasing

Ask for disagreement and failure modes, not another generic summary.

### Gemini - Google-context specialist

Use when:

- the task depends on Google Workspace or Google services
- a second independent reasoning pass is useful
- its particular context or integration is relevant

Do not invoke it by default.

### Local model - private-data specialist

Use for:

- sensitive material that should remain on the machine
- drafts that do not need current web research
- local classification or transformation

Keep its capabilities and outputs bounded until the local runtime is proven.

## Default routing

### Everyday thought or problem

```text
Voice bridge -> Copilot TRANSLATE -> Copilot action plan
```

### Sharp message or difficult conversation

```text
Voice bridge -> Copilot TRANSLATE -> ChatGPT challenge or SAUCE -> Copilot final wording
```

### Current factual question

```text
Voice bridge -> Perplexity research -> Copilot synthesis
```

### Code or repo change

```text
Voice bridge -> Copilot clarification -> VS Code/Copilot implementation -> focused validation
```

### Sensitive private material

```text
Voice bridge -> local model or Copilot only when appropriate
```

Do not distribute sensitive material across every service.

## Multi-tool packet

When a second opinion is justified, give each tool the same compact packet:

```text
CONTEXT: What is happening?
GOAL: What outcome is wanted?
CONSTRAINTS: What must not happen?
QUESTION: What decision or output is needed?
```

Ask each tool for one of:

- a recommendation
- the strongest objection
- missing information
- a confidence level

Then give the responses to the lead tool for synthesis. Do not average incompatible answers silently.

## Stop conditions

- Do not ask every tool the same question by habit.
- Do not use external tools for private data without a reason.
- Do not treat the number of agreeing models as proof.
- Do not add a second tool if the first already produced a clear, testable answer.
- If tools disagree, identify the factual or value assumption causing the disagreement.
- For code, the repository's tests and runtime behavior outrank model preference.

## Daily use

The daily briefing starts in Copilot. Add one specialist only when the briefing identifies a question that specialist is suited to answer.

The goal is not maximum model activity. The goal is better decisions with less drift, cost, and repeated work.

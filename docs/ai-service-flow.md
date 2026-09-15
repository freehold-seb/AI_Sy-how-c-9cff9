# AI service flow

## Core idea

The tools should work as a coordinated flow, not as isolated chat windows.

Each stage has one job, a clear output, and a handoff packet for the next stage. A later stage may improve or challenge an earlier result, but it must not silently erase the source meaning.

## Flow

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

## Stage contracts

### 1. Voice capture

Owner: OCHRE Bridge

Input: spoken thought
Output: raw transcript in the clipboard

Rules:

- preserve the words as captured
- do not add personality or interpretation
- an empty capture is a retry, not a decision

### 2. Intent translation

Owner: Copilot with `TRANSLATE:`

Input: raw transcript
Output: concise statement of what the speaker appears to mean, including uncertainty

Rules:

- separate the main point from noise
- preserve emotional or practical urgency
- ask one clarifying question only when ambiguity changes the action

### 3. Task classification

Owner: lead AI

Input: translated intent
Output: one route such as:

- communicate
- research
- decide
- plan
- implement
- troubleshoot
- review

Rules:

- choose the smallest route that can answer the need
- do not invoke every tool by default

### 4. Specialist work

Owner: the tool best suited to the route

Input: a compact context packet
Output: recommendation, draft, research result, code change, or diagnostic

Rules:

- give the specialist one question
- preserve sources and assumptions
- keep private material local or limited to approved services

### 5. Challenge and verification

Owner: a second tool only when risk or uncertainty justifies it

Input: proposed result and context packet
Output: strongest objection, missing evidence, contradiction, or confidence assessment

Rules:

- challenge the answer, not the person
- do not treat agreement between models as proof
- for code, executable validation outranks model opinion

### 6. Final synthesis

Owner: Copilot or the selected lead

Input: original intent, specialist result, challenge result
Output: one clear answer or next action, with unresolved uncertainty stated

Rules:

- keep the user's meaning and voice
- show important disagreement
- produce an output that can be used immediately

### 7. Human approval

Owner: Sebastian

Required before:

- sending an external message
- making a financial, legal, medical, or security-sensitive decision
- deleting, moving, or archiving files
- changing system configuration
- running destructive commands
- enabling new autonomous behavior

## Handoff packet

Every stage should pass this compact structure:

```text
INTENT: What is the user trying to accomplish?
CONTEXT: What facts matter?
CONSTRAINTS: What must not happen?
CURRENT_RESULT: What has been produced so far?
OPEN_QUESTIONS: What remains uncertain?
NEXT_ACTION: What should the next stage do?
```

## Autonomy levels

### Level 0: manual

The user chooses each tool and pastes each handoff.

### Level 1: guided

The lead tool recommends the next stage and prepares the handoff packet. The user starts it.

### Level 2: bounded automation

The system routes low-risk work automatically, records the route, and pauses at human approval gates.

### Level 3: not enabled

No autonomous external sending, deletion, system changes, or financial actions.

Start at Level 0, move to Level 1 after repeated successful daily use, and consider Level 2 only for a narrow proven workflow.

## Failure behavior

- If a specialist is unavailable, use the lead tool or the documented manual fallback.
- If tools disagree, surface the disagreement instead of averaging it away.
- If the output is unclear, return to `TRANSLATE:` rather than adding more tools.
- If a chain step fails twice, stop the chain and preserve the last known good result.
- Every automated step must be reversible or leave a clear record of what it did.

## First implementation target

Do not build a full multi-agent platform yet. Prove this small chain manually:

```text
OCHRE Bridge -> Copilot TRANSLATE -> one specialist -> Copilot synthesis
```

Use it for three real tasks. Record where the handoff is useful and where it creates friction. Automate only the repeated friction point.

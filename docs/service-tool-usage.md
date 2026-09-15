# Service-tool usage

## Purpose

Use the voice bridge to get raw thoughts and problems into this chat, then use a mode label to turn them into something useful.

The bridge does one job:

```text
speak -> transcribe -> clipboard
```

This chat does the next job:

```text
raw thought -> clarify -> structure -> usable output
```

## Standard run

1. Start the bridge from the repo root:

   ```powershell
   cd C:\Users\SEB\kepler\worktrees\AI_Sy-do-th-126fe
   python .\ochre_bridge.py
   ```

2. Hold Right Ctrl, speak naturally, and release.
3. Return to this chat.
4. Begin the pasted text with one mode label.
5. Paste the clipboard contents and send.

## Mode labels

### `POLISH:`

Clean up grammar and filler while preserving the meaning and voice.

### `SAUCE:`

Rewrite it with sharp, confident, professional directness: Simon Cowell's blunt clarity without cruelty. Keep the speaker's actual meaning and personality, remove filler and transcription noise, identify the real point, and make the result sound intelligent and usable. Do not invent facts or soften a valid criticism.

### `ELABORATE:`

Expand the thought with useful context, structure, and detail.

### `TRANSLATE:`

Work out what the speaker is trying to communicate, then express it clearly.

## Useful prompt formats

```text
TRANSLATE: [raw thought]
```

```text
SAUCE: [raw problem or message]
```

For this mode, the assistant should return only the finished version unless a brief clarification is necessary.

```text
POLISH: [raw draft]
```

```text
ELABORATE: [rough idea that needs structure]
```

## What counts as a successful run

- The bridge prints `Copied:` with a transcript.
- The transcript is pasted into chat.
- A mode label tells the assistant what kind of help is wanted.
- The result is specific enough to use, send, decide from, or act on.

An occasional empty capture is not a reason to rebuild the system. Ignore it, retry once, and use Voice Access plus manual copy if the bridge becomes unreliable.

## Service boundary

The bridge does not refine thoughts. The chat does not control the microphone. Keeping those jobs separate makes the workflow understandable and replaceable.

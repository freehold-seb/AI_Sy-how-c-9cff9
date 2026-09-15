# The minimum viable workflow

## Defend this above everything

```text
Speak → clipboard → paste into Copilot with [MODE]: → copy output → done
```

Nothing gets added until this runs frictionlessly every day.

## 7-day execution plan

### Phase 1 — Stability (Days 1–3)

#### Day 1 — Bridge proof

- [x] `python ochre_bridge.py`
- [x] Hold Right Ctrl → speak → release → check clipboard
- [x] Confirm text is in the clipboard
- [ ] Paste into Copilot with a mode label such as `SAUCE:`
- [ ] Confirm output is refined and usable
- [x] ✅ Bridge works → transcription and clipboard path proven
- [ ] ❌ Bridge broken → max 20 minutes debug. If still broken, skip it and continue with Voice Access + manual copy.
- [ ] Stop here. Do not add anything.

#### Day 2 — 5 real runs

- [ ] Use the workflow 5 times with real content
- [ ] Track what felt smooth and what created friction
- [ ] If one step breaks consistently, fix only that step and nothing else

#### Day 3 — Lock it

- [ ] If Days 1–2 worked → Phase 1 complete
- [ ] Write down the exact working steps
- [ ] If not working → find the one broken link, fix only that, repeat Day 2
- [ ] Do not touch the Hub
- [ ] Do not rebuild anything

### Phase 2 — Consistency (Days 4–5)

#### Day 4 — Real daily use

- [ ] Complete 3+ real tasks through the workflow
- [ ] Log exactly one friction point
- [ ] Do not fix anything yet

#### Day 5 — Fix one thing only

- [ ] Address the Day 4 friction point
- [ ] Stop condition: if the fix takes > 30 minutes, defer it, use a workaround, and keep moving

### Phase 3 — Optional expansion (Days 6–7)

#### Day 6 — Hub decision point

- [ ] If paste-into-chat is good enough permanently, stop here and do not build a Hub
- [ ] If the Hub is still wanted, confirm the AI connection issue is solved before writing code
- [ ] Do not rebuild the Hub with `AppSDK.ai.chat()`; that path is closed

#### Day 7 — Review and reset

- [ ] What is stable?
- [ ] What is the next proof step?
- [ ] Update the handoff notes with actual results

## Stop conditions — absolute rules, no exceptions

- Any debug session > 30 minutes → stop, use manual fallback, keep the loop going
- Hub broken → use the chat workflow; do not rebuild
- New idea arrives → write it down; implement nothing until Phase 2 is proven
- Machine acting up → fix the machine first with:
  - `powercfg /h off`
  - `shutdown /r /t 0 /f`
- Bridge broken on Day 1 → skip it, use Voice Access + manual paste, and prove the loop anyway

## Restart plan

Restart the machine. Then begin Day 1.

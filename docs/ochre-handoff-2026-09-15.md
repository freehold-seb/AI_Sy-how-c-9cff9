# OCHRE / FREEHOLD HANDOFF

Updated: 2026-09-15

## Project direction

This is a personal AI workflow system focused on voice, transcription, and text refinement.

The valid current working pattern is:

- Voice Access for dictation
- paste text into Copilot chat with a mode label
- refine with a specific mode
- copy the result to the destination

The broad Hub rebuild is not the current target. The target is a small validated workflow first.

## Operational principles

- Keep ambition.
- Reduce initial scope.
- Prove each step works.
- Expand only after the current layer is stable.
- Treat the Hub as a later layer, not the foundation.

## What is working right now

TEXT REFINEMENT via Copilot chat:

- POLISH
- ELABORATE
- SAUCE
- TRANSLATE

These modes are the current working interface.

## What failed earlier

- AppSDK.ai.chat() returning 404 on the Hub path
- repeated rebuilds without a root-cause pivot
- losing the simpler working alternative while chasing the bigger app

This is not a code bug in the chat workflow. It is a backend/platform limitation in the Hub path.

## OCHRE BRIDGE status

The bridge is verified on the current machine. It has produced `Copied:` transcripts from spoken input.

The bridge can still produce an occasional empty capture. Treat that as a retryable capture glitch, not as a reason to rebuild the workflow.

Keep the target pipeline simple:

- Speak
- capture to clipboard
- paste into Copilot with a mode label
- refine
- copy output

Detailed operating instructions are in [service-tool-usage.md](service-tool-usage.md).

## PC / system maintenance

### Shutdown / restart issue

This is likely caused by Fast Startup / hybrid shutdown behaviour in Windows.

Run in an Administrator PowerShell window:

```powershell
powercfg /h off
```

Then:

```powershell
shutdown /r /t 0 /f
```

This forces a proper restart instead of hybrid hibernate.

### Windows Update

```powershell
Start-Process "ms-settings:windowsupdate"
```

Install everything, then restart again if required.

## RGB + fan control

### Recommended free options

- OpenRGB: openrgb.org
- Fan Control by Rem0o: github.com/Rem0o/FanControl.Releases

These are the free replacements for the expensive RGB/fan-control stack.

If the system is all one brand, native tools may be cleaner:

- ASUS -> Armoury Crate
- MSI -> MSI Center
- Corsair -> iCUE
- Gigabyte -> Gigabyte Control Center

## Immediate next step

After the restart and cleanup:

1. install OpenRGB
2. install Fan Control
3. review startup apps
4. use the OCHRE bridge for real thoughts and problems
5. test the paste-into-chat pipeline

## Minimal proof-of-life workflow

1. Use Voice Access to dictate a sentence.
2. Paste into Copilot chat with a label such as SAUCE: or POLISH:
3. Copy the refined result.
4. Put the output into the desired target.

This is the working baseline.

## Keep in mind

Voice Access is a real primary input method. The project should be built around that, not around a full platform app that hasn't proven itself yet.

## Final principle

Do not add complexity before the loop is stable.

The system should be daily-use, not theoretical.

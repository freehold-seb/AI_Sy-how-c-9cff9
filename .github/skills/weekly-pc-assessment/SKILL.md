---
name: weekly-pc-assessment
description: "Use when: assessing what changed on this Windows PC in the past week, reviewing recent system or local-data changes, producing evidence-based operational suggestions, or making short-term predictions from a local PC assessment."
argument-hint: "Optional focus areas, approved folders, and exclusions"
---

# Weekly PC Assessment

Assess meaningful changes on the current Windows PC during the previous seven calendar days. Produce a concise, evidence-based assessment with practical suggestions and clearly labeled predictions.

## Safety And Consent

1. State the intended collection categories and ask for confirmation before inspecting broad user folders, application data, browser data, email, messaging, cloud-sync data, documents, or file contents.
2. Treat the following as sensitive. Do not read, print, retain, or include their contents unless the user explicitly names the exact file and purpose:
   - Passwords, private keys, tokens, credentials, SSH material, and `.env` files.
   - Browser profiles, saved sessions, authentication databases, and password-manager data.
   - Personal communications, medical, financial, legal, and identity documents.
3. Default to metadata only for broadly scoped paths: file names, extensions, sizes, timestamps, hashes when justified, and aggregate counts. Do not enumerate every personal filename in the report.
4. Do not modify the PC. Do not install software, change configuration, stop services, or remove files while assessing. Offer changes as suggestions and obtain separate approval before acting.
5. Keep raw evidence in the chat/session only. A redacted baseline may be saved only after the user approves its exact local path. Redact usernames, account identifiers, hostnames, and paths in the final summary when they are unnecessary.
6. Baselines may contain only aggregate counts, dates, software/update identifiers, health indicators, and redacted finding summaries. Exclude personal filenames, file contents, secrets, account data, and raw event-log records. Do not add a baseline to version control automatically.

## Inputs

Establish these inputs before collection:

- **Window:** the prior seven days ending now, using local time. State the exact start and end timestamps.
- **Focus:** system health, security, software, storage, project activity, network indicators, or a user-specified concern.
- **Approved content paths:** exact folders whose file contents may be examined. With no paths, use metadata only outside the workspace.
- **Exclusions:** folders, applications, accounts, or data types to omit.
- **Baseline path:** an optional, user-approved local path for a redacted week-over-week comparison file.

If the user has not provided focus, use a balanced system-and-workspace assessment. If broad local review was requested but no approved content paths are named, collect broad metadata only and ask whether any folders should be approved for content review.

## Collection Workflow

### 1. Establish A Baseline

1. Record the assessment window and the current Windows version/build, uptime, available disk space, and active power state when available.
2. Identify whether comparable prior snapshots, reports, or local baselines exist. Use them only if they do not contain sensitive content.
3. If no baseline exists, explicitly label the result as a first-run assessment; distinguish observations from detected deltas.
4. After reporting, offer to save a redacted baseline at the approved path. Do not create or overwrite it without explicit confirmation.

### 2. Collect System And Security Changes

Gather minimally sufficient, read-only evidence for:

- Windows Update history, recent update failures, restarts, and relevant Event Viewer summaries.
- Newly installed, removed, or updated applications, drivers, Windows features, and scheduled tasks.
- Changes to startup applications, services, firewall/Defender status, and security-related warnings.
- Recent reliability, crash, disk, memory, battery, thermal, and network-adapter indicators.

Prefer Windows-native commands and structured sources such as PowerShell cmdlets, WMI/CIM, Reliability Monitor data, Windows Update history, and filtered event logs. Filter by the assessment window and limit noisy results to relevant categories and counts.

### 3. Collect Workspace And Approved Data Changes

1. Inspect the current workspace first: version-control status, recent commits, dependency/lockfile changes, recently modified source/configuration files, test or build outputs, and error logs relevant to the focus.
2. For each approved external folder, summarize modification patterns by directory, extension, volume, and day. Read file contents only when the user approved that path and the content is necessary to explain a meaningful signal.
3. Identify unusual patterns: sudden file-count or storage growth, repeated failures, unexpected executable/script changes, synchronization conflicts, or persistent crash artifacts.
4. Do not infer intent from file names alone. Report observations and request context where alternative explanations are equally plausible.

### 4. Correlate And Triage

Correlate events by time:

- A system update followed by boot, driver, service, application, or reliability changes.
- An application update followed by errors, resource spikes, storage growth, or altered network behavior.
- Workspace dependency/configuration changes followed by failed builds, tests, or task failures.

For every finding, capture:

- The observation and time range.
- The source category and the smallest necessary supporting evidence.
- The likely impact: low, medium, or high.
- Confidence: low, medium, or high.
- Alternative explanations when confidence is not high.

Do not claim causation from temporal order alone. Mark it as a correlation unless corroborating evidence supports a causal link.

## Analysis And Predictions

1. Rank findings by likely user impact, not by raw event count.
2. Separate facts, correlations, hypotheses, and recommendations.
3. Make only short-horizon predictions, normally one to two weeks. Each prediction must include:
   - A measurable expected outcome.
   - The evidence pattern it relies on.
   - Confidence level and conditions that would invalidate it.
4. Prefer concrete, reversible suggestions: free or reclaim space, review a specific update, rerun a failing workflow, update a named dependency, inspect a service, or capture a new baseline.
5. Do not make health, employment, financial, behavioral, or identity predictions. Do not profile users from personal files or application usage.

## Report Format

Return the report in this order:

1. **Window and scope** - exact time range, inspected sources, approved content paths, and exclusions.
2. **Executive assessment** - two to five sentences describing overall system state and the most material change.
3. **Prioritized findings** - include impact, confidence, evidence summary, and interpretation.
4. **Predictions** - up to three short-horizon, falsifiable predictions with conditions.
5. **Suggested actions** - ranked, concrete, and reversible; distinguish urgent actions from monitoring.
6. **Data and uncertainty** - gaps, inaccessible sources, baseline limitations, and excluded data.

Never disclose sensitive contents in the report. Replace exact sensitive names and paths with neutral categories unless the user explicitly asks for them.

## Completion Checks

Before finishing, verify that:

- The entire assessment window was used and the timezone is stated.
- No unapproved sensitive content was accessed or reported.
- Every material claim has an evidence summary and confidence level.
- Predictions are short-term, measurable, and falsifiable.
- Recommendations follow from findings, are non-destructive, and identify any approval required.
- The report distinguishes first-run observations from changes against a known baseline.

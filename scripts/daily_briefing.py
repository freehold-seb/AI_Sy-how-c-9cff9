"""Generate a daily project briefing for the current workspace.

This only reads workspace metadata and selected config. It creates or replaces
the current day's Markdown report under `reports/`. Set
`DAILY_BRIEFING_DRY_RUN=1` to print the report to stdout instead of writing it.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"


def read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def count_files(suffix: str | None = None) -> int:
    files = (path for path in ROOT.rglob("*") if path.is_file())
    if suffix is None:
        return sum(1 for _ in files)
    return sum(1 for path in files if path.suffix.lower() == suffix)


def recent_files() -> list[Path]:
    cutoff = datetime.now().astimezone() - timedelta(hours=24)
    return sorted(
        (
            path
            for path in ROOT.rglob("*")
            if path.is_file()
            and ".git" not in path.parts
            and path.stat().st_mtime >= cutoff.timestamp()
        ),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )[:10]


def main() -> int:
    now = datetime.now().astimezone()
    runtime = read_json(ROOT / "config" / "runtime_mode.json")
    required_paths = {
        "Voice bridge": ROOT / "ochre_bridge.py",
        "Service usage guide": ROOT / "docs" / "service-tool-usage.md",
        "Smoke test": ROOT / "tests" / "test_repo_smoke.py",
        "Handoff": ROOT / "handoff.md",
    }

    lines = [
        "# Daily project briefing",
        "",
        f"Generated: {now.isoformat(timespec='seconds')}",
        "Scope: current recovery workspace only; read-only metadata and selected config.",
        "",
        "## Current posture",
        "",
        f"- Runtime mode: {runtime.get('mode', 'unknown')}",
        f"- Second node expected: {runtime.get('node2_online_expected', 'unknown')}",
        f"- Total files: {count_files()}",
        f"- Python files: {count_files('.py')}",
        f"- Markdown files: {count_files('.md')}",
        "",
        "## Working surface",
        "",
    ]

    for label, path in required_paths.items():
        status = "present" if path.exists() else "missing"
        lines.append(f"- {label}: {status}")

    lines.extend(
        [
            "",
            "## Recent workspace changes",
            "",
        ]
    )
    recent = recent_files()
    if recent:
        lines.extend(f"- {path.relative_to(ROOT)}" for path in recent)
    else:
        lines.append("- No files modified in the last 24 hours.")

    lines.extend(
        [
            "",
            "## Today's review questions",
            "",
            "- What is working well enough to keep?",
            "- What is the single biggest friction point?",
            "- What is the smallest reversible improvement?",
            "- What should remain deferred?",
            "",
            "## Recommended focus",
            "",
            "1. Use the voice bridge for one real thought or problem.",
            "2. Paste it here with `TRANSLATE:` or `SAUCE:`.",
            "3. Record one friction point; do not start a second improvement today.",
        ]
    )

    report = "\n".join(lines) + "\n"

    if os.environ.get("DAILY_BRIEFING_DRY_RUN") == "1":
        print(report)
        return 0

    REPORTS.mkdir(exist_ok=True)
    output = REPORTS / f"daily-briefing-{now.date().isoformat()}.md"
    output.write_text(report, encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

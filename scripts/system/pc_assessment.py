"""Preview and run explicitly approved, read-only PC metadata collection."""

from __future__ import annotations

import argparse
import os
from collections.abc import Callable, Sequence
from datetime import datetime, timedelta
from pathlib import Path

try:
    from .pc_collectors import POWERSHELL_COMMANDS, CollectionResult, run_category
    from .pc_report import write_report
except ImportError:
    from pc_collectors import POWERSHELL_COMMANDS, CollectionResult, run_category
    from pc_report import write_report


CONFIRMATION_PHRASE = "I APPROVE READ-ONLY COLLECTION"
EXCLUSIONS = (
    "file contents and directory traversal",
    "OneDrive",
    "Google Drive traversal or hydration",
    "browser, credential, communication, and sensitive document data",
    "packet capture and payload inspection",
    "all system changes, installs, uninstalls, updates, and file moves",
)

Collector = Callable[[str], CollectionResult]
ReportWriter = Callable[[Sequence[CollectionResult]], Path]


def report_directory(environ: dict[str, str] | None = None) -> Path:
    values = os.environ if environ is None else environ
    local_app_data = values.get("LOCALAPPDATA")
    if not local_app_data:
        return Path.home() / "AppData" / "Local" / "Kepler" / "pc-assessment"
    return Path(local_app_data) / "Kepler" / "pc-assessment"


def assessment_window(now: datetime | None = None) -> tuple[datetime, datetime]:
    end = now or datetime.now().astimezone()
    return end - timedelta(days=7), end


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preview", action="store_true", help="Show collection scope only")
    parser.add_argument("--collect", action="store_true", help="Run approved read-only categories")
    parser.add_argument(
        "--category",
        action="append",
        choices=tuple(POWERSHELL_COMMANDS),
        default=[],
        help="Category to collect; repeat for multiple categories",
    )
    parser.add_argument("--confirm", help="Exact one-time confirmation phrase")
    return parser


def print_preview(now: datetime | None = None) -> None:
    start, end = assessment_window(now)
    print("PC assessment preview (no commands executed)")
    print(f"Window: {start.isoformat(timespec='seconds')} to {end.isoformat(timespec='seconds')}")
    print(f"Report destination: {report_directory()}")
    print("Privileges: current user; no elevation or self-elevation")
    print("Categories and exact PowerShell commands:")
    for category, command in POWERSHELL_COMMANDS.items():
        print(f"- {category}: {command}")
    print("Exclusions:")
    for exclusion in EXCLUSIONS:
        print(f"- {exclusion}")


def main(
    argv: Sequence[str] | None = None,
    *,
    collector: Collector = run_category,
    report_writer: ReportWriter = write_report,
) -> int:
    args = build_parser().parse_args(argv)
    if not args.collect:
        print_preview()
        return 0

    if not args.category:
        print("Collection blocked: select at least one --category.")
        return 2
    if args.confirm != CONFIRMATION_PHRASE:
        print(f'Collection blocked: pass --confirm "{CONFIRMATION_PHRASE}".')
        return 2

    results = [collector(category) for category in dict.fromkeys(args.category)]
    for result in results:
        print(f"{result.category}: {result.status}")
    output = report_writer(results)
    print(f"Redacted report: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Create a read-only metadata inventory of related Kepler workspaces."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

CURRENT_ROOT = Path(__file__).resolve().parents[1]
KEPLER_ROOT = CURRENT_ROOT.parent.parent
WORKTREES_ROOT = KEPLER_ROOT / "worktrees"
REPOSITORIES_ROOT = KEPLER_ROOT / "repositories"


def git_metadata(path: Path) -> str:
    git_path = path / ".git"
    if git_path.is_dir():
        return "git directory"
    if git_path.is_file():
        return "git worktree"
    return "no git metadata"


def workspace_summary(path: Path) -> dict[str, str | int]:
    files = []
    try:
        files = [item for item in path.rglob("*") if item.is_file() and ".git" not in item.parts]
    except OSError as exc:
        return {
            "name": path.name,
            "path": str(path),
            "status": f"unreadable: {exc}",
            "files": 0,
            "python": 0,
            "markdown": 0,
            "git": git_metadata(path),
        }

    return {
        "name": path.name,
        "path": str(path),
        "status": "present",
        "files": len(files),
        "python": sum(item.suffix.lower() == ".py" for item in files),
        "markdown": sum(item.suffix.lower() == ".md" for item in files),
        "git": git_metadata(path),
    }


def discover_workspaces() -> list[Path]:
    candidates = []
    if WORKTREES_ROOT.is_dir():
        candidates.extend(path for path in WORKTREES_ROOT.iterdir() if path.is_dir())
    if REPOSITORIES_ROOT.is_dir():
        candidates.extend(path for path in REPOSITORIES_ROOT.iterdir() if path.is_dir())
    return sorted(candidates, key=lambda path: str(path).lower())


def render(summaries: list[dict[str, str | int]], generated: datetime) -> str:
    lines = [
        "# Workspace inventory",
        "",
        f"Generated: {generated.astimezone().isoformat(timespec='seconds')}",
        "Scope: metadata only; no files were modified, moved, deleted, or archived.",
        "",
        "## Canonical workspace",
        "",
        f"- `{CURRENT_ROOT.name}`: {CURRENT_ROOT}",
        "",
        "## Related workspaces",
        "",
        "| Name | Location | Git metadata | Files | Python | Markdown | Status |",
        "| --- | --- | --- | ---: | ---: | ---: | --- |",
    ]
    for summary in summaries:
        lines.append(
            "| {name} | `{path}` | {git} | {files} | {python} | {markdown} | {status} |".format(
                **summary
            )
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- This report does not decide which workspace should be synchronized.",
            "- File counts do not prove that two workspaces contain equivalent code.",
            "- Review the canonical workspace first, then inspect differences before any changes.",
            "- Do not run deletion, archive, or synchronization scripts based on this report alone.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Inventory related Kepler workspaces without modifying them")
    parser.add_argument(
        "--output",
        type=Path,
        default=CURRENT_ROOT / "reports" / "workspace-inventory.md",
        help="Report path relative to the current directory or as an absolute path",
    )
    args = parser.parse_args()

    output = args.output if args.output.is_absolute() else CURRENT_ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    report = render([workspace_summary(path) for path in discover_workspaces()], datetime.now().astimezone())
    output.write_text(report, encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

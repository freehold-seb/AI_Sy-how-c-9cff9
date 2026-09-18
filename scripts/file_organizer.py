"""Scan and classify files in disposable fixtures without modifying them."""

from __future__ import annotations

import argparse
import json
import shutil
from collections.abc import Mapping
from pathlib import Path
from typing import Sequence, TypedDict

ROOT = Path(__file__).resolve().parents[1]
FIXTURES_ROOT = (ROOT / "tests" / "fixtures").resolve()
SCHEMA_PATH = Path(__file__).resolve().parent / "file_organizer_schema.json"
MOVE_LOG_NAME = "move_log.txt"
CONFIRMATION_PHRASE = "I APPROVE FILE MOVES"

EXTENSION_CATEGORIES = {
    ".aac": "audio",
    ".bmp": "image",
    ".doc": "document",
    ".docx": "document",
    ".flac": "audio",
    ".gif": "image",
    ".jpeg": "image",
    ".jpg": "image",
    ".m4a": "audio",
    ".md": "document",
    ".mp3": "audio",
    ".odt": "document",
    ".ogg": "audio",
    ".pdf": "document",
    ".png": "image",
    ".rtf": "document",
    ".svg": "image",
    ".txt": "document",
    ".wav": "audio",
    ".webp": "image",
}


class ScannedFile(TypedDict):
    name: str
    extension: str


class ClassifiedFile(ScannedFile):
    category: str


class PlannedMove(TypedDict):
    name: str
    category: str
    source: Path
    destination: Path
    conflict: bool


KNOWN_CATEGORIES = frozenset(EXTENSION_CATEGORIES.values()) | {"unknown"}


def scan_fixture_directory(directory: Path) -> list[ScannedFile]:
    """Return file names and normalized extensions for a fixture directory."""
    target = directory.resolve()
    try:
        target.relative_to(FIXTURES_ROOT)
    except ValueError as exc:
        raise ValueError("scan target must be inside tests/fixtures") from exc

    if not target.is_dir():
        raise NotADirectoryError(target)

    return [
        {"name": path.name, "extension": path.suffix.lower()}
        for path in sorted(target.iterdir(), key=lambda item: item.name.casefold())
        if path.is_file()
    ]


def classify_scanned_files(files: Sequence[ScannedFile]) -> list[ClassifiedFile]:
    """Map scanned files to named categories using normalized extensions."""
    return [
        {
            "name": entry["name"],
            "extension": entry["extension"],
            "category": EXTENSION_CATEGORIES.get(entry["extension"].lower(), "unknown"),
        }
        for entry in files
    ]


def load_schema(path: Path = SCHEMA_PATH) -> dict[str, str]:
    """Load and validate the category-to-target-folder schema mapping."""
    schema = json.loads(path.read_text(encoding="utf-8"))

    if not isinstance(schema, dict):
        raise ValueError("schema must be a JSON object mapping categories to folder names")

    missing = KNOWN_CATEGORIES - schema.keys()
    if missing:
        raise ValueError(f"schema is missing categories: {sorted(missing)}")

    for category, folder in schema.items():
        if category not in KNOWN_CATEGORIES:
            raise ValueError(f"schema has unknown category: {category!r}")
        if not isinstance(folder, str) or not folder.strip():
            raise ValueError(f"schema folder name for {category!r} must be a non-empty string")

    return schema


def plan_moves(
    files: Sequence[ClassifiedFile],
    schema: Mapping[str, str],
    source_directory: Path,
) -> list[PlannedMove]:
    """Compute planned fixture moves and route conflicts to ``unsorted``."""
    source = source_directory.resolve()
    unsorted = source / schema["unknown"].strip()
    planned_destinations: set[Path] = set()
    planned: list[PlannedMove] = []

    for entry in files:
        destination = source / schema[entry["category"]].strip() / entry["name"]
        conflict = destination.exists() or destination in planned_destinations
        if conflict:
            destination = unsorted / entry["name"]
        if destination.exists() or destination in planned_destinations:
            raise FileExistsError(f"cannot route conflict to unsorted: {destination}")
        planned_destinations.add(destination)
        move: PlannedMove = {
            "name": entry["name"],
            "category": entry["category"],
            "source": source / entry["name"],
            "destination": destination,
            "conflict": conflict,
        }
        planned.append(move)

    return planned


def execute_moves(planned_moves: Sequence[PlannedMove], log_path: Path) -> list[str]:
    """Execute already-planned fixture moves and log each result."""
    log_lines: list[str] = []
    for move in planned_moves:
        source = move["source"]
        destination = move["destination"]
        if not source.is_file():
            log_lines.append(f"SKIP missing {source.name}")
            continue
        if destination.exists():
            log_lines.append(f"SKIP conflict {destination.relative_to(source.parent)}")
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(source), str(destination))
        log_lines.append(f"MOVE {source.name} -> {destination.relative_to(source.parent)}")

    log_path.write_text("\n".join(log_lines) + "\n", encoding="utf-8")
    return log_lines


def validate_moves(planned_moves: Sequence[PlannedMove]) -> None:
    """Confirm every planned source was moved to its planned destination."""
    failures = [
        move["name"]
        for move in planned_moves
        if move["source"].exists() or not move["destination"].is_file()
    ]
    if failures:
        raise RuntimeError(f"post-move validation failed: {', '.join(failures)}")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="List and classify files in a disposable fixture directory"
    )
    parser.add_argument("directory", type=Path)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned moves without creating directories or moving files",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Execute planned moves inside tests/fixtures and validate the result",
    )
    parser.add_argument(
        "--confirm",
        help="Exact confirmation phrase required before any move executes",
    )
    args = parser.parse_args(argv)

    scanned_files = scan_fixture_directory(args.directory)
    classified_files = classify_scanned_files(scanned_files)
    if args.dry_run:
        schema = load_schema()
        for move in plan_moves(classified_files, schema, args.directory):
            marker = " [CONFLICT -> unsorted]" if move["conflict"] else ""
            print(f"{move['name']} -> {move['destination'].relative_to(args.directory.resolve())}{marker}")
        return 0

    if args.execute:
        if args.confirm != CONFIRMATION_PHRASE:
            print(f'Move blocked: pass --confirm "{CONFIRMATION_PHRASE}".')
            return 2
        schema = load_schema()
        planned = plan_moves(classified_files, schema, args.directory)
        log_lines = execute_moves(planned, args.directory.resolve() / MOVE_LOG_NAME)
        validate_moves(planned)
        for line in log_lines:
            print(line)
        print("VALIDATED post-move layout")
        return 0

    for entry in classified_files:
        extension = entry["extension"] or "<none>"
        print(f"{entry['name']}\t{extension}\t{entry['category']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

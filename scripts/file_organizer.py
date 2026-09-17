"""Scan and classify files in disposable fixtures without modifying them."""

from __future__ import annotations

import argparse
import json
from collections.abc import Mapping
from pathlib import Path
from typing import Sequence, TypedDict

ROOT = Path(__file__).resolve().parents[1]
FIXTURES_ROOT = (ROOT / "tests" / "fixtures").resolve()
SCHEMA_PATH = Path(__file__).resolve().parent / "file_organizer_schema.json"

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
    """Compute planned fixture moves without touching the filesystem."""
    source = source_directory.resolve()
    return [
        {
            "name": entry["name"],
            "category": entry["category"],
            "source": source / entry["name"],
            "destination": source / schema[entry["category"]].strip() / entry["name"],
        }
        for entry in files
    ]


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
    args = parser.parse_args(argv)

    scanned_files = scan_fixture_directory(args.directory)
    classified_files = classify_scanned_files(scanned_files)
    if args.dry_run:
        schema = load_schema()
        for move in plan_moves(classified_files, schema, args.directory):
            print(f"{move['name']} -> {move['destination'].relative_to(args.directory.resolve())}")
        return 0

    for entry in classified_files:
        extension = entry["extension"] or "<none>"
        print(f"{entry['name']}\t{extension}\t{entry['category']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

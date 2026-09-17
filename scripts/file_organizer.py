"""Scan and classify files in disposable fixtures without modifying them."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence, TypedDict

ROOT = Path(__file__).resolve().parents[1]
FIXTURES_ROOT = (ROOT / "tests" / "fixtures").resolve()

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


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="List and classify files in a disposable fixture directory"
    )
    parser.add_argument("directory", type=Path)
    args = parser.parse_args(argv)

    scanned_files = scan_fixture_directory(args.directory)
    for entry in classify_scanned_files(scanned_files):
        extension = entry["extension"] or "<none>"
        print(f"{entry['name']}\t{extension}\t{entry['category']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

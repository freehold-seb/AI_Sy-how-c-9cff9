"""List files in disposable file-organization fixtures without modifying them."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

ROOT = Path(__file__).resolve().parents[1]
FIXTURES_ROOT = (ROOT / "tests" / "fixtures").resolve()


def scan_fixture_directory(directory: Path) -> list[dict[str, str]]:
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


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="List files in a disposable fixture directory")
    parser.add_argument("directory", type=Path)
    args = parser.parse_args(argv)

    for entry in scan_fixture_directory(args.directory):
        extension = entry["extension"] or "<none>"
        print(f"{entry['name']}\t{extension}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

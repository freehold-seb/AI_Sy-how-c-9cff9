"""Turn an explicit voice transcript into a fixture-only organizer dry run."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Sequence

import pyperclip

from scripts.file_organizer import main as organizer_main

ORGANIZE_PATTERN = re.compile(r"^\s*organize\s+files(?:\s+in)?\s+(.+?)\s*$", re.IGNORECASE)


def directory_from_transcript(transcript: str) -> Path:
    """Extract a directory only from the explicit supported voice command."""
    match = ORGANIZE_PATTERN.match(transcript)
    if not match:
        raise ValueError("say: organize files in <fixture directory>")
    return Path(match.group(1).strip().strip('"'))


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("transcript", nargs="?", help="Transcript from the local voice bridge")
    parser.add_argument(
        "--clipboard",
        action="store_true",
        help="Read the transcript copied by the local voice bridge",
    )
    args = parser.parse_args(argv)
    if args.clipboard:
        if args.transcript:
            parser.error("provide either a transcript or --clipboard, not both")
        args.transcript = pyperclip.paste()
    if not args.transcript:
        parser.error("provide a transcript or --clipboard")
    try:
        directory = directory_from_transcript(args.transcript)
    except ValueError as exc:
        parser.error(str(exc))
    return organizer_main([str(directory), "--dry-run"])


if __name__ == "__main__":
    raise SystemExit(main())

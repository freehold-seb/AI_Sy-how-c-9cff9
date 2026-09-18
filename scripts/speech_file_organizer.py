"""Convert a local speech transcript into a fixture-only organizer dry run."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from scripts import file_organizer

DRY_RUN_TRIGGERS = ("dry run", "dry-run", "preview")
ORGANIZE_TRIGGERS = ("organize", "organise", "organization", "organisation", "sort")
EXECUTION_TRIGGERS = ("execute", "move files", "move them", "run it for real")


def transcript_requests_dry_run(transcript: str) -> bool:
    """Return true when a transcript asks for a file organization preview."""
    normalized = " ".join(transcript.casefold().split())
    return any(trigger in normalized for trigger in ORGANIZE_TRIGGERS) and any(
        trigger in normalized for trigger in DRY_RUN_TRIGGERS
    )


def transcript_requests_execution(transcript: str) -> bool:
    """Return true when speech attempts to cross into the real-move path."""
    normalized = " ".join(transcript.casefold().split())
    return file_organizer.CONFIRMATION_PHRASE.casefold() in normalized or any(
        trigger in normalized for trigger in EXECUTION_TRIGGERS
    )


def read_clipboard_transcript() -> str:
    try:
        import pyperclip
    except ImportError as exc:
        raise RuntimeError(
            "pyperclip is required when --transcript is not supplied"
        ) from exc

    return pyperclip.paste().strip()


def run_dry_run_from_transcript(transcript: str, directory: Path) -> int:
    cleaned = transcript.strip()
    if not cleaned:
        print("Speech organizer blocked: transcript is empty.")
        return 1

    if transcript_requests_execution(cleaned):
        print(
            "Speech organizer blocked: transcripts can only request dry-runs; "
            "real moves still require scripts\\file_organizer.py --execute "
            "with the exact confirmation phrase."
        )
        return 2

    if not transcript_requests_dry_run(cleaned):
        print(
            'Speech organizer ignored: say "organize files dry run" '
            'or "preview file organization".'
        )
        return 1

    print(f"Transcript accepted for dry-run: {cleaned}")
    return file_organizer.main([str(directory), "--dry-run"])


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run a fixture-only file organizer dry-run from a speech transcript"
    )
    parser.add_argument("directory", type=Path, help="Fixture directory to preview")
    parser.add_argument(
        "--transcript",
        help="Transcript text to parse; defaults to the current clipboard transcript",
    )
    args = parser.parse_args(argv)

    transcript = (
        args.transcript if args.transcript is not None else read_clipboard_transcript()
    )
    return run_dry_run_from_transcript(transcript, args.directory)


if __name__ == "__main__":
    raise SystemExit(main())

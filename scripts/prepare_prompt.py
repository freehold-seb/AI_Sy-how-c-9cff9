"""Prepare a mode-labelled prompt from the current clipboard transcript."""

from __future__ import annotations

import argparse

MODES = ("TRANSLATE", "SAUCE", "POLISH", "ELABORATE")


def _load_clipboard():
    try:
        import pyperclip
    except ModuleNotFoundError:
        return None
    return pyperclip


def strip_existing_mode_label(transcript: str) -> str:
    normalized = transcript.strip()
    upper = normalized.upper()
    for mode in MODES:
        prefix = f"{mode}:"
        if upper.startswith(prefix):
            return normalized[len(prefix) :].lstrip()
    return normalized


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Prefix the clipboard transcript with a refinement mode."
    )
    parser.add_argument("mode", type=str.upper, choices=MODES, help="Refinement mode to apply")
    args = parser.parse_args()

    clipboard = _load_clipboard()
    if clipboard is None:
        parser.error(
            "pyperclip is not installed; run `pip install -r requirements.txt` in this workspace"
        )

    transcript = strip_existing_mode_label(clipboard.paste())
    if not transcript:
        parser.error("clipboard is empty; capture speech with OCHRE Bridge first")

    prompt = f"{args.mode}: {transcript}"
    clipboard.copy(prompt)
    print(f"Prepared {args.mode} prompt ({len(prompt)} characters).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

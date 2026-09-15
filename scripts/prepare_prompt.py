"""Prepare a mode-labelled prompt from the current clipboard transcript."""

from __future__ import annotations

import argparse

import pyperclip

MODES = ("TRANSLATE", "SAUCE", "POLISH", "ELABORATE")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Prefix the clipboard transcript with a refinement mode."
    )
    parser.add_argument("mode", choices=MODES, help="Refinement mode to apply")
    args = parser.parse_args()

    transcript = pyperclip.paste().strip()
    if not transcript:
        parser.error("clipboard is empty; capture speech with OCHRE Bridge first")

    prompt = f"{args.mode}: {transcript}"
    pyperclip.copy(prompt)
    print(f"Prepared {args.mode} prompt ({len(prompt)} characters).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

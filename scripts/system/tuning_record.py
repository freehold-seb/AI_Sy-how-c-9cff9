"""Record reversible hardware tuning decisions without changing the system."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Sequence

DEFAULT_PATH = Path.home() / "AppData" / "Local" / "Kepler" / "hardware-tuning.jsonl"


def append_record(
    path: Path,
    *,
    setting: str,
    before: str,
    after: str,
    rollback: str,
    evidence: str,
) -> None:
    """Append one complete record; this function performs no tuning action."""
    values = {
        "recorded_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "setting": setting.strip(),
        "before": before.strip(),
        "after": after.strip(),
        "rollback": rollback.strip(),
        "evidence": evidence.strip(),
    }
    if not all(values[key] for key in ("setting", "before", "after", "rollback", "evidence")):
        raise ValueError("setting, before, after, rollback, and evidence are required")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(values, sort_keys=True) + "\n")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--setting", required=True)
    parser.add_argument("--before", required=True)
    parser.add_argument("--after", required=True)
    parser.add_argument("--rollback", required=True)
    parser.add_argument("--evidence", required=True)
    parser.add_argument("--output", type=Path, default=DEFAULT_PATH)
    args = parser.parse_args(argv)
    append_record(
        args.output,
        setting=args.setting,
        before=args.before,
        after=args.after,
        rollback=args.rollback,
        evidence=args.evidence,
    )
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

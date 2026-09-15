"""Minimal control panel entrypoint for the local recovery workspace."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def main() -> int:
    """Placeholder control-panel entrypoint for the local repo."""
    print(f"Control panel ready at {ROOT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

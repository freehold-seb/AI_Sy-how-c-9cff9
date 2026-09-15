"""Fail-closed adapter for the future orchestration boundary."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class OrchestratorAdapter:
    """Describe routing without executing external work."""

    enabled: bool = False

    def route(self, task: Any) -> dict[str, Any]:
        if not self.enabled:
            return {"status": "blocked", "reason": "orchestration_disabled", "task": task}
        return {"status": "ready", "task": task}

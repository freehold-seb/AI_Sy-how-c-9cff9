"""Fail-closed adapter for the future orchestration boundary."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any


STATIC_ROUTES = [
    {
        "name": "default",
        "description": "Default route",
        "conditions": None,
    },
    {
        "name": "fallback",
        "description": "Fallback route",
        "conditions": None,
    },
]


@dataclass(frozen=True)
class OrchestratorAdapter:
    """Describe routing without executing external work."""

    enabled: bool = False

    def route(self, task: Any) -> dict[str, Any]:
        result = {
            "status": "ready" if self.enabled else "blocked",
            "reason": (
                "orchestration_ready"
                if self.enabled
                else "orchestration_disabled"
            ),
            "task": task,
            "routes": deepcopy(STATIC_ROUTES),
            "selected": None,
            "mode": "describe",
        }
        return result

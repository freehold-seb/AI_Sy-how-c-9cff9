"""Read-only pipeline state snapshots."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, is_dataclass
from datetime import datetime
from typing import Any, Mapping, Sequence


def collect_pipeline_trace(
    config: Mapping[str, Any],
    taskspec: Any,
    verifier_events: Sequence[Mapping[str, Any]],
    dry_run: bool,
) -> dict[str, Any]:
    """Return a detached snapshot of the supplied pipeline state."""
    if not isinstance(config, Mapping):
        raise TypeError("config must be a mapping")
    if not isinstance(verifier_events, Sequence) or isinstance(
        verifier_events, (str, bytes)
    ):
        raise TypeError("verifier_events must be a sequence")
    if not isinstance(dry_run, bool):
        raise TypeError("dry_run must be a bool")

    if is_dataclass(taskspec) and not isinstance(taskspec, type):
        normalized_taskspec = asdict(taskspec)
    elif isinstance(taskspec, Mapping):
        normalized_taskspec = dict(taskspec)
    else:
        raise TypeError("taskspec must be a dataclass or mapping")

    return {
        "config": deepcopy(dict(config)),
        "taskspec": deepcopy(normalized_taskspec),
        "verifier_trace": deepcopy(list(verifier_events)),
        "dry_run": dry_run,
        "mode": "dry_run" if dry_run else "normal",
        "timestamp": datetime.now().astimezone().isoformat(),
    }

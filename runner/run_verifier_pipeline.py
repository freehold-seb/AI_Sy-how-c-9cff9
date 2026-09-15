"""Bounded, fail-closed runner/verifier pipeline."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from runner.orchestrator_adapter import OrchestratorAdapter
from verifier import TaskSpec, choose_best_candidate

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "agent_config.json"


def load_taskspec(source: str | Path | Mapping[str, Any]) -> TaskSpec:
    if isinstance(source, Mapping):
        payload = source
    else:
        payload = json.loads(Path(source).read_text(encoding="utf-8"))
    if not isinstance(payload, Mapping):
        raise ValueError("taskspec must be a JSON object")
    return TaskSpec.from_mapping(payload)


def _load_config(config_path: str | Path = CONFIG_PATH) -> Mapping[str, Any]:
    return json.loads(Path(config_path).read_text(encoding="utf-8"))


def run_pipeline(
    taskspec: TaskSpec | Mapping[str, Any],
    candidates: Sequence[Mapping[str, Any]] | None = None,
    config_path: str | Path = CONFIG_PATH,
) -> dict[str, Any]:
    task = taskspec if isinstance(taskspec, TaskSpec) else load_taskspec(taskspec)
    config = _load_config(config_path)
    adapter = OrchestratorAdapter(enabled=bool(config.get("orchestrator_enabled")))
    route = adapter.route(task.task_id)
    if route["status"] == "blocked" or bool(config.get("dry_run", True)):
        return {
            "status": "blocked",
            "task_id": task.task_id,
            "reason": route.get("reason", "dry_run_enabled"),
        }
    selected = choose_best_candidate(candidates or [])
    if selected is None:
        return {"status": "awaiting_candidate", "task_id": task.task_id}
    return {"status": "verified", "task_id": task.task_id, "candidate": dict(selected)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("taskspec", type=Path)
    args = parser.parse_args()
    print(json.dumps(run_pipeline(load_taskspec(args.taskspec)), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

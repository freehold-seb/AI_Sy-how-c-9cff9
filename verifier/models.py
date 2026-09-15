from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Mapping


@dataclass(frozen=True)
class CandidateOutput:
    text: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class TaskSpec:
    task_id: str
    objective: str
    input: Any = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def prompt(self) -> str:
        return self.objective

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "TaskSpec":
        task_id = value.get("task_id") or value.get("id")
        objective = value.get("objective") or value.get("prompt")
        if not isinstance(task_id, str) or not task_id.strip():
            raise ValueError("taskspec requires a non-empty task_id")
        if not isinstance(objective, str) or not objective.strip():
            raise ValueError("taskspec requires a non-empty objective")
        return cls(
            task_id=task_id,
            objective=objective,
            input=value.get("input"),
            metadata=dict(value.get("metadata", {}))
            if isinstance(value.get("metadata"), Mapping)
            else {},
        )


@dataclass(frozen=True)
class QCDecision:
    accept: bool = True
    reason: str = "accepted"
    score: float = 1.0


@dataclass(frozen=True)
class VerifiedCandidate:
    candidate: Mapping[str, Any]
    score: float = 0.0
    accepted: bool = True
    notes: str = ""


@dataclass(frozen=True)
class VerifierResult:
    accepted: bool
    reason: str
    candidate: Mapping[str, Any] | None = None

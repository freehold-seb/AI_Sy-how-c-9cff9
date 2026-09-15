"""Small deterministic verifier boundary for the recovery workspace."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

__all__ = [
    "Verifier",
    "DomainRules",
    "MetricsEngine",
    "CandidateOutput",
    "QCDecision",
    "TaskSpec",
    "VerifiedCandidate",
    "VerifierResult",
    "QCLearning",
    "SchemaEnforcer",
    "apply_qc_decision",
    "choose_best_candidate",
    "evaluate_candidate",
]


@dataclass(frozen=True)
class TaskSpec:
    task_id: str
    objective: str
    input: Any = None

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "TaskSpec":
        task_id = value.get("task_id") or value.get("id")
        objective = value.get("objective")
        if not isinstance(task_id, str) or not task_id.strip():
            raise ValueError("taskspec requires a non-empty task_id")
        if not isinstance(objective, str) or not objective.strip():
            raise ValueError("taskspec requires a non-empty objective")
        return cls(task_id=task_id, objective=objective, input=value.get("input"))


@dataclass(frozen=True)
class VerifierResult:
    accepted: bool
    reason: str
    candidate: Mapping[str, Any] | None = None


class Verifier:
    """Validate candidate shape without calling external services."""

    def evaluate(self, candidate: Mapping[str, Any]) -> VerifierResult:
        return evaluate_candidate(candidate)


class DomainRules:
    pass


class MetricsEngine:
    pass


class CandidateOutput:
    pass


class QCDecision:
    pass


class VerifiedCandidate:
    pass


class QCLearning:
    pass


class SchemaEnforcer:
    pass


def apply_qc_decision(result: VerifierResult) -> Mapping[str, Any] | None:
    return result.candidate if result.accepted else None


def choose_best_candidate(candidates: Sequence[Mapping[str, Any]]) -> Mapping[str, Any] | None:
    valid = [candidate for candidate in candidates if evaluate_candidate(candidate).accepted]
    return max(valid, key=lambda candidate: candidate.get("score", 0)) if valid else None


def evaluate_candidate(candidate: Mapping[str, Any]) -> VerifierResult:
    if not isinstance(candidate, Mapping):
        return VerifierResult(False, "candidate_not_mapping")
    output = candidate.get("output")
    if not isinstance(output, str) or not output.strip():
        return VerifierResult(False, "candidate_output_missing")
    score = candidate.get("score", 0)
    if not isinstance(score, (int, float)):
        return VerifierResult(False, "candidate_score_invalid")
    return VerifierResult(True, "candidate_valid", candidate)

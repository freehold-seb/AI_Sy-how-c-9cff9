"""Small deterministic verifier boundary for the recovery workspace."""

from __future__ import annotations

from dataclasses import dataclass
import json
import math
from typing import Any, Mapping, Sequence

__all__ = [
    "Verifier",
    "DomainRules",
    "MetricsEngine",
    "CandidateOutput",
    "QCDecision",
    "TaskSpec",
    "validate_task_spec",
    "VerifiedCandidate",
    "VerifierResult",
    "QCLearning",
    "SchemaEnforcer",
    "apply_qc_decision",
    "choose_best_candidate",
    "evaluate_candidate",
    "log_verifier_event",
    "validate_score",
]


@dataclass(frozen=True)
class TaskSpec:
    task_id: str
    objective: str
    input: Any = None

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "TaskSpec":
        return validate_task_spec(value)


def validate_task_spec(value: Mapping[str, Any]) -> TaskSpec:
    if not isinstance(value, Mapping):
        raise TypeError("taskspec must be a JSON object")

    allowed_keys = {"task_id", "id", "objective", "input"}
    unknown_keys = set(value) - allowed_keys
    if unknown_keys:
        raise ValueError(f"unknown taskspec keys: {sorted(unknown_keys)}")
    if "task_id" in value and "id" in value:
        raise ValueError("taskspec must use either task_id or id, not both")

    task_id = value.get("task_id", value.get("id"))
    objective = value.get("objective")
    if not isinstance(task_id, str) or not task_id.strip():
        raise ValueError("taskspec requires a non-empty task_id")
    if not isinstance(objective, str) or not objective.strip():
        raise ValueError("taskspec requires a non-empty objective")
    return TaskSpec(task_id=task_id, objective=objective, input=value.get("input"))


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


def log_verifier_event(event: str, **details: Any) -> None:
    payload = json.dumps(details, sort_keys=True, default=str)
    print(f"[VERIFIER] {event}: {payload}")


def _candidate_id(candidate: object) -> Any:
    if isinstance(candidate, Mapping):
        return candidate.get("candidate_id", candidate.get("id"))
    return None


def choose_best_candidate(
    candidates: Sequence[Mapping[str, Any]],
) -> Mapping[str, Any] | None:
    valid = [candidate for candidate in candidates if evaluate_candidate(candidate).accepted]
    if not valid:
        log_verifier_event("candidate_selection_empty", candidate_count=len(candidates))
        return None
    selected = max(valid, key=lambda candidate: candidate.get("score", 0))
    log_verifier_event(
        "candidate_selected",
        candidate_id=_candidate_id(selected),
        score=selected.get("score"),
    )
    return selected


def evaluate_candidate(candidate: Mapping[str, Any]) -> VerifierResult:
    if not isinstance(candidate, Mapping):
        reason = "candidate_not_mapping"
        log_verifier_event("candidate_rejected", candidate_id=None, reason=reason)
        return VerifierResult(False, reason)
    output = candidate.get("output")
    if not isinstance(output, str) or not output.strip():
        reason = "candidate_output_missing"
        log_verifier_event(
            "candidate_rejected", candidate_id=_candidate_id(candidate), reason=reason
        )
        return VerifierResult(False, reason)
    score = candidate.get("score", 0)
    try:
        score_is_valid = validate_score(score)
    except TypeError:
        score_is_valid = False
    if not score_is_valid:
        if isinstance(score, (int, float)) and not isinstance(score, bool):
            log_verifier_event(
                "score_rejected_non_finite",
                candidate_id=_candidate_id(candidate),
                score=score,
            )
        reason = "candidate_score_invalid"
        log_verifier_event(
            "candidate_rejected", candidate_id=_candidate_id(candidate), reason=reason
        )
        return VerifierResult(False, reason)
    log_verifier_event(
        "candidate_accepted",
        candidate_id=_candidate_id(candidate),
        score=score,
    )
    return VerifierResult(True, "candidate_valid", candidate)


def validate_score(score: object) -> bool:
    if isinstance(score, bool) or not isinstance(score, (int, float)):
        raise TypeError("score must be numeric")
    return math.isfinite(score)

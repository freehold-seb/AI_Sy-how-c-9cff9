"""Small deterministic verifier boundary for the recovery workspace."""

from __future__ import annotations

from typing import Any, Mapping, Sequence

from .domain_rules import DomainRules
from .metrics import MetricsEngine
from .models import CandidateOutput, QCDecision, TaskSpec, VerifiedCandidate, VerifierResult
from .qc_learning import QCLearning
from .schemas import SchemaEnforcer

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


class Verifier:
    """Validate candidate shape without calling external services."""

    def evaluate(self, candidate: Mapping[str, Any]) -> VerifierResult:
        return evaluate_candidate(candidate)


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

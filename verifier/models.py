from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class CandidateOutput:
    text: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TaskSpec:
    task_id: str = "task"
    prompt: str = ""
    constraints: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class QCDecision:
    accept: bool = True
    reason: str = "accepted"
    score: float = 1.0


@dataclass
class VerifiedCandidate:
    candidate: CandidateOutput
    score: float = 0.0
    accepted: bool = True
    notes: str = ""


@dataclass
class VerifierResult:
    winner: Optional[VerifiedCandidate] = None
    candidates: List[VerifiedCandidate] = field(default_factory=list)
    accepted: bool = True
    summary: str = "no candidates evaluated"

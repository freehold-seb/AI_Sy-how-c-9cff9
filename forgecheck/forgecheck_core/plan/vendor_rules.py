from __future__ import annotations

from .recommendation_matrix import RECOMMENDATION_MATRIX


def recommendations_for_system_class(system_class: str) -> list[dict]:
    rows = RECOMMENDATION_MATRIX.get(system_class, RECOMMENDATION_MATRIX["unknown"])
    return [
        {
            "id": action_id,
            "severity": "recommended",
            "message": message,
        }
        for action_id, message in rows
    ]

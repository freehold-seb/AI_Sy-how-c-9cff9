from __future__ import annotations

RECOMMENDATION_MATRIX: dict[str, list[tuple[str, str]]] = {
    "unknown": [
        (
            "manual_review",
            "Review the system classification manually before approving vendor actions.",
        )
    ]
}

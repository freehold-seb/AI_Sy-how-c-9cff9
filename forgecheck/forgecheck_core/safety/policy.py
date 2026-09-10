from __future__ import annotations


def action_matches_blocked_keywords(action: dict, blocked_actions: list[str]) -> bool:
    action_text = " ".join(
        [
            str(action.get("id", "")),
            str(action.get("title", "")),
            str(action.get("suggested_action", "")),
        ]
    ).lower()

    return any(blocked.lower() in action_text for blocked in blocked_actions)

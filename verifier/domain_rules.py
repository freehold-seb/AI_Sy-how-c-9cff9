from __future__ import annotations


class DomainRules:
    """Minimal domain-rules stub for the recovered verifier shell."""

    def __init__(self, rules=None):
        self.rules = rules or {}

    def validate(self, payload):
        return {"ok": True, "payload": payload, "rules": self.rules}

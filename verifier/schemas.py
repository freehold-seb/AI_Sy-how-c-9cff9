from __future__ import annotations


class SchemaEnforcer:
    """Minimal schema-enforcement stub for the recovered verifier shell."""

    def __init__(self, schema=None):
        self.schema = schema or {}

    def validate(self, payload):
        return {"ok": True, "schema": self.schema, "payload": payload}

from __future__ import annotations


class MetricsEngine:
    """Minimal metrics stub for the recovered verifier shell."""

    def __init__(self):
        self.samples = []

    def record(self, metric_name, value):
        self.samples.append({"metric": metric_name, "value": value})
        return value

    def summary(self):
        return {"samples": list(self.samples)}

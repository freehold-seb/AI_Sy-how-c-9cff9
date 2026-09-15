from __future__ import annotations


class QCLearning:
    """Minimal QC learning stub for the recovered verifier shell."""

    def __init__(self):
        self.history = []

    def learn(self, decision):
        self.history.append(decision)
        return decision

    def summary(self):
        return {"decisions": len(self.history)}

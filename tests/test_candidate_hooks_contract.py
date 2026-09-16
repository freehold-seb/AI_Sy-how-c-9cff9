from copy import deepcopy
from datetime import datetime
import math

import pytest

from agent_core.candidate_hooks import CandidateHookRunner


class RecordingIntrospector:
    def __init__(self):
        self.events = []

    def record(self, event):
        self.events.append(deepcopy(event))


def _config(*, enabled=True, pre=None, post=None):
    return {
        "hooks": {
            "enabled": enabled,
            "pre": pre or [],
            "post": post or [],
        }
    }


def _candidate():
    return {"id": "candidate-1", "output": "value", "score": 0.5}


def test_hooks_are_opt_in_and_disabled_by_default():
    calls = []

    def hook(candidate, context):
        calls.append("called")
        return {**candidate, "changed": True}

    result = CandidateHookRunner(
        _config(enabled=False, pre=[{"name": "transform", "enabled": True}]),
        RecordingIntrospector(),
        {"transform": hook},
    ).run_pre_hooks(_candidate(), {})

    assert result == _candidate()
    assert calls == []


def test_registry_name_resolution_runs_only_declared_enabled_hooks():
    calls = []

    def hook(candidate, context):
        calls.append("transform")
        return {**candidate, "changed": True}

    config = _config(
        pre=[
            {"name": "transform", "enabled": True},
            {"name": "transform", "enabled": False},
        ]
    )
    result = CandidateHookRunner(
        config, RecordingIntrospector(), {"transform": hook}
    ).run_pre_hooks(_candidate(), {})

    assert result["changed"] is True
    assert calls == ["transform"]


def test_pre_hook_transforms_without_mutating_original():
    candidate = _candidate()
    original = deepcopy(candidate)

    def add_metadata(value, context):
        return {**value, "metadata": {"source": context["source"]}}

    result = CandidateHookRunner(
        _config(pre=[{"name": "metadata", "enabled": True}]),
        RecordingIntrospector(),
        {"metadata": add_metadata},
    ).run_pre_hooks(candidate, {"source": "test"})

    assert result["metadata"] == {"source": "test"}
    assert candidate == original
    assert result is not candidate


def test_pre_hooks_run_in_declared_order():
    order = []

    def make_hook(name):
        def hook(candidate, context):
            order.append(name)
            return candidate

        return hook

    names = ["first", "second", "third"]
    config = _config(pre=[{"name": name, "enabled": True} for name in names])
    registry = {name: make_hook(name) for name in names}
    introspector = RecordingIntrospector()

    CandidateHookRunner(config, introspector, registry).run_pre_hooks(_candidate(), {})

    assert order == names
    assert [event["hook_name"] for event in introspector.events] == names
    assert [event["order_index"] for event in introspector.events] == [0, 1, 2]


def test_post_hook_can_return_candidate_and_score_tuple():
    def adjust(candidate, score, context):
        return ({**candidate, "reviewed": True}, score + 0.1)

    result = CandidateHookRunner(
        _config(post=[{"name": "adjust", "enabled": True}]),
        RecordingIntrospector(),
        {"adjust": adjust},
    ).run_post_hooks(_candidate(), 0.5, {})

    assert result[0]["reviewed"] is True
    assert result[1] == 0.6


def test_post_hooks_run_in_declared_order():
    order = []

    def make_hook(name):
        def hook(candidate, score, context):
            order.append(name)
            return candidate, score

        return hook

    names = ["first", "second", "third"]
    config = _config(post=[{"name": name, "enabled": True} for name in names])
    registry = {name: make_hook(name) for name in names}
    introspector = RecordingIntrospector()

    CandidateHookRunner(config, introspector, registry).run_post_hooks(
        _candidate(), 0.5, {}
    )

    assert order == names
    assert [event["hook_name"] for event in introspector.events] == names
    assert [event["order_index"] for event in introspector.events] == [0, 1, 2]


@pytest.mark.parametrize("unsafe_score", [-0.1, 1.1, math.nan, math.inf, -math.inf])
def test_post_hook_rejects_unsafe_scores(unsafe_score):
    def score_breaker(candidate, score, context):
        return candidate, unsafe_score

    result = CandidateHookRunner(
        _config(post=[{"name": "unsafe", "enabled": True}]),
        RecordingIntrospector(),
        {"unsafe": score_breaker},
    ).run_post_hooks(_candidate(), 0.5, {})

    assert result[1] == 0.5
    assert math.isfinite(result[1])
    assert 0 <= result[1] <= 1


def test_missing_registry_name_is_reported_without_crashing():
    introspector = RecordingIntrospector()
    result = CandidateHookRunner(
        _config(pre=[{"name": "missing", "enabled": True}]),
        introspector,
        {},
    ).run_pre_hooks(_candidate(), {})

    assert result == _candidate()
    assert introspector.events[0]["error"] == "hook_not_found"
    assert introspector.events[0]["hook_name"] == "missing"


def test_hook_errors_preserve_candidate_and_score():
    def failing(*args):
        raise RuntimeError("hook exploded")

    introspector = RecordingIntrospector()
    result = CandidateHookRunner(
        _config(post=[{"name": "exploder", "enabled": True}]),
        introspector,
        {"exploder": failing},
    ).run_post_hooks(_candidate(), 0.5, {})

    assert result == (_candidate(), 0.5)
    assert introspector.events[0]["error"] == "hook exploded"


def test_dry_run_calls_hooks_but_discards_transformations():
    calls = []

    def transform(candidate, context):
        calls.append("called")
        return {**candidate, "changed": True}

    introspector = RecordingIntrospector()
    result = CandidateHookRunner(
        _config(pre=[{"name": "transform", "enabled": True}]),
        introspector,
        {"transform": transform},
    ).run_pre_hooks(_candidate(), {"dry_run": True})

    assert calls == ["called"]
    assert result == _candidate()
    assert introspector.events[0]["dry_run"] is True
    assert introspector.events[0]["event"] == "hook_skipped_due_to_dry_run"
    assert introspector.events[0]["output_candidate"] == introspector.events[0]["input_candidate"]


def test_hook_events_have_complete_shape_and_timestamp():
    def noop(candidate, context):
        return None

    introspector = RecordingIntrospector()
    CandidateHookRunner(
        _config(pre=[{"name": "noop", "enabled": True}]),
        introspector,
        {"noop": noop},
    ).run_pre_hooks(_candidate(), {})
    event = introspector.events[0]

    assert set(event) == {
        "event",
        "hook_type",
        "hook_name",
        "input_candidate",
        "output_candidate",
        "input_score",
        "output_score",
        "dry_run",
        "error",
        "timestamp",
        "order_index",
    }
    assert isinstance(event["hook_type"], str)
    assert isinstance(event["hook_name"], str)
    assert isinstance(event["dry_run"], bool)
    assert isinstance(event["order_index"], int)
    assert event["error"] is None
    datetime.fromisoformat(event["timestamp"])


def test_registry_is_not_mutated_by_execution():
    def noop(candidate, context):
        return None

    registry = {"noop": noop}
    original_registry = registry.copy()

    CandidateHookRunner(
        _config(pre=[{"name": "noop", "enabled": True}]),
        RecordingIntrospector(),
        registry,
    ).run_pre_hooks(_candidate(), {})

    assert registry == original_registry

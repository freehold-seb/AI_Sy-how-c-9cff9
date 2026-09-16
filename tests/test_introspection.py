from copy import deepcopy
from datetime import datetime

import pytest

from agent_core.introspection import collect_pipeline_trace
from verifier import TaskSpec


def test_collect_pipeline_trace_returns_required_fields_and_types():
    trace = collect_pipeline_trace(
        {"dry_run": True},
        TaskSpec("demo", "check"),
        [{"event": "candidate_rejected"}],
        True,
    )

    assert set(trace) == {
        "config",
        "taskspec",
        "verifier_trace",
        "dry_run",
        "mode",
        "timestamp",
    }
    assert isinstance(trace["config"], dict)
    assert isinstance(trace["taskspec"], dict)
    assert isinstance(trace["verifier_trace"], list)
    assert isinstance(trace["dry_run"], bool)
    assert trace["mode"] == "dry_run"
    datetime.fromisoformat(trace["timestamp"])


def test_collect_pipeline_trace_supports_normal_mode_and_events():
    trace = collect_pipeline_trace(
        {"dry_run": False},
        {"task_id": "demo", "objective": "check"},
        [{"event": "candidate_selected", "candidate_id": "a"}],
        False,
    )

    assert trace["dry_run"] is False
    assert trace["mode"] == "normal"
    assert trace["verifier_trace"][0]["event"] == "candidate_selected"


def test_collect_pipeline_trace_does_not_mutate_or_share_inputs():
    config = {"nested": {"enabled": True}}
    taskspec = {"task_id": "demo", "objective": "check"}
    events = [{"details": {"score": 1}}]
    original = deepcopy((config, taskspec, events))

    trace = collect_pipeline_trace(config, taskspec, events, False)
    trace["config"]["nested"]["enabled"] = False
    trace["taskspec"]["task_id"] = "changed"
    trace["verifier_trace"][0]["details"]["score"] = 99

    assert (config, taskspec, events) == original


def test_collect_pipeline_trace_accepts_empty_events():
    trace = collect_pipeline_trace({}, TaskSpec("demo", "check"), [], True)

    assert trace["verifier_trace"] == []


@pytest.mark.parametrize(
    "config,taskspec,events,dry_run",
    [
        ([], TaskSpec("demo", "check"), [], False),
        ({}, "not a taskspec", [], False),
        ({}, TaskSpec("demo", "check"), "not events", False),
        ({}, TaskSpec("demo", "check"), [], "false"),
    ],
)
def test_collect_pipeline_trace_rejects_invalid_inputs(
    config, taskspec, events, dry_run
):
    with pytest.raises(TypeError):
        collect_pipeline_trace(config, taskspec, events, dry_run)

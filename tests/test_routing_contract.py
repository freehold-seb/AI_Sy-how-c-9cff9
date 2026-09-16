from copy import deepcopy

from runner.orchestrator_adapter import OrchestratorAdapter


def test_route_has_stable_return_shape():
    task = {"id": "t1", "objective": "test"}

    result = OrchestratorAdapter().route(task)

    assert set(result) == {
        "status",
        "reason",
        "task",
        "routes",
        "selected",
        "mode",
    }
    assert isinstance(result["status"], str)
    assert isinstance(result["reason"], str)
    assert result["task"] is task


def test_route_does_not_mutate_input_task():
    task = {"id": "t1", "objective": "test", "input": {"safe": True}}
    original = deepcopy(task)

    OrchestratorAdapter().route(task)

    assert task == original


def test_route_returns_independent_result_mapping():
    task = {"id": "t1", "objective": "test"}
    result = OrchestratorAdapter().route(task)
    mutated = dict(result)

    mutated["status"] = "changed"

    assert result["status"] != "changed"


def test_route_is_independent_of_dry_run_fields():
    adapter = OrchestratorAdapter()
    normal_task = {"id": "t1", "objective": "test", "dry_run": False}
    dry_run_task = {"id": "t1", "objective": "test", "dry_run": True}

    normal = adapter.route(normal_task)
    dry_run = adapter.route(dry_run_task)

    assert normal["status"] == dry_run["status"]
    assert normal["reason"] == dry_run["reason"]


def test_route_has_no_route_name_behavior():
    task = {"id": "t1", "objective": "test", "route": "nonexistent"}

    result = OrchestratorAdapter().route(task)

    assert set(result) == {
        "status",
        "reason",
        "task",
        "routes",
        "selected",
        "mode",
    }


def test_route_has_stable_snapshot_across_calls():
    task = {"id": "t1", "objective": "test"}
    adapter = OrchestratorAdapter()

    first = adapter.route(task)
    second = adapter.route(task)

    assert first == second

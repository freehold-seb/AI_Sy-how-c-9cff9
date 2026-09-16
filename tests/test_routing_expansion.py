from copy import deepcopy

from runner.orchestrator_adapter import OrchestratorAdapter


def test_route_has_additive_expanded_shape():
    result = OrchestratorAdapter(enabled=True).route({"id": "t1"})

    assert set(result) == {
        "status",
        "reason",
        "task",
        "routes",
        "selected",
        "mode",
    }
    assert result["status"] == "ready"
    assert result["reason"] == "orchestration_ready"
    assert isinstance(result["routes"], list)
    assert result["selected"] is None
    assert result["mode"] == "describe"


def test_route_exposes_static_descriptors():
    routes = OrchestratorAdapter(enabled=True).route({"id": "t1"})["routes"]

    assert routes
    for route in routes:
        assert set(route) == {"name", "description", "conditions"}
        assert isinstance(route["name"], str)
        assert isinstance(route["description"], str)
        assert route["conditions"] is None


def test_blocked_status_and_reason_are_preserved():
    result = OrchestratorAdapter(enabled=False).route({"id": "t1"})

    assert result["status"] == "blocked"
    assert result["reason"] == "orchestration_disabled"
    assert result["selected"] is None
    assert result["mode"] == "describe"


def test_routes_are_independent_copies():
    adapter = OrchestratorAdapter(enabled=True)
    first = adapter.route({"id": "t1"})
    first["routes"][0]["name"] = "changed"
    first["routes"].append({"name": "extra", "description": "", "conditions": None})

    second = adapter.route({"id": "t1"})

    assert second["routes"][0]["name"] == "default"
    assert len(second["routes"]) == 2


def test_route_fields_are_neutral_to_dry_run_and_arbitrary_route_name():
    adapter = OrchestratorAdapter(enabled=True)
    normal = adapter.route({"id": "t1", "dry_run": False})
    dry = adapter.route({"id": "t1", "dry_run": True, "route": "nonexistent"})

    assert normal["status"] == dry["status"]
    assert normal["reason"] == dry["reason"]
    assert normal["routes"] == dry["routes"]
    assert normal["selected"] == dry["selected"] is None


def test_route_does_not_mutate_task():
    task = {"id": "t1", "nested": {"safe": True}}
    original = deepcopy(task)

    OrchestratorAdapter(enabled=True).route(task)

    assert task == original

import pytest

from runner.run_verifier_pipeline import load_taskspec
from verifier import TaskSpec, validate_task_spec


def test_validate_task_spec_accepts_actual_contract():
    value = {"task_id": "demo", "objective": "check", "input": {"mode": "safe"}}

    result = validate_task_spec(value)

    assert result == TaskSpec("demo", "check", {"mode": "safe"})


def test_validate_task_spec_accepts_legacy_id_alias():
    assert validate_task_spec({"id": "demo", "objective": "check"}).task_id == "demo"


@pytest.mark.parametrize("missing", ["task_id", "objective"])
def test_validate_task_spec_rejects_missing_required_fields(missing):
    value = {"task_id": "demo", "objective": "check"}
    del value[missing]

    with pytest.raises(ValueError, match="requires"):
        validate_task_spec(value)


def test_validate_task_spec_rejects_unknown_key():
    with pytest.raises(ValueError, match="unknown taskspec keys"):
        validate_task_spec({"task_id": "demo", "objective": "check", "timeout": 30})


@pytest.mark.parametrize(
    "value",
    [
        {"task_id": 123, "objective": "check"},
        {"task_id": "demo", "objective": 123},
        {"task_id": "", "objective": "check"},
        {"task_id": "demo", "objective": ""},
    ],
)
def test_validate_task_spec_rejects_invalid_required_values(value):
    with pytest.raises(ValueError):
        validate_task_spec(value)


def test_validate_task_spec_rejects_ambiguous_ids():
    with pytest.raises(ValueError, match="either task_id or id"):
        validate_task_spec({"task_id": "demo", "id": "other", "objective": "check"})


def test_load_taskspec_uses_validation_entrypoint():
    with pytest.raises(ValueError, match="unknown taskspec keys"):
        load_taskspec({"task_id": "demo", "objective": "check", "dry_run": True})

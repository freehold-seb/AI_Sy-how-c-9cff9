import importlib
import json

from runner.run_verifier_pipeline import run_pipeline
from verifier import evaluate_candidate


def test_core_entrypoints_import():
    importlib.import_module("core.agent")
    importlib.import_module("core.control_panel")
    importlib.import_module("core.queue_worker")
    importlib.import_module("services.queue_worker")
    importlib.import_module("verifier")


def test_root_entrypoints_import():
    importlib.import_module("agent")
    importlib.import_module("control_panel")


def test_pipeline_is_blocked_by_default_config():
    result = run_pipeline({"task_id": "demo", "objective": "check"})

    assert result == {
        "status": "blocked",
        "task_id": "demo",
        "reason": "orchestration_disabled",
    }


def test_verifier_rejects_missing_output():
    result = evaluate_candidate({"score": 1})

    assert result.accepted is False
    assert result.reason == "candidate_output_missing"


def test_pipeline_selects_best_candidate_when_explicitly_enabled(tmp_path):
    config_path = tmp_path / "agent_config.json"
    config_path.write_text(
        json.dumps(
            {
                "api_key": "",
                "model": "qwen3:8b",
                "max_history_turns": 30,
                "dry_run": False,
                "admin_timeout_minutes": 60,
                "admin_require_confirmation": True,
                "downloads_dir": "",
                "media_output_dir": "",
                "orchestrator_enabled": True,
            }
        ),
        encoding="utf-8",
    )

    result = run_pipeline(
        {"task_id": "demo", "objective": "check"},
        candidates=[
            {"output": "low", "score": 1},
            {"output": "high", "score": 2},
        ],
        config_path=config_path,
    )

    assert result == {
        "status": "verified",
        "task_id": "demo",
        "candidate": {"output": "high", "score": 2},
    }

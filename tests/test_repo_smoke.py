import importlib
import json
import sys
from types import SimpleNamespace

import pytest

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


def test_verifier_exports_use_implemented_helpers():
    import verifier
    from verifier.domain_rules import DomainRules
    from verifier.metrics import MetricsEngine
    from verifier.models import TaskSpec
    from verifier.qc_learning import QCLearning
    from verifier.schemas import SchemaEnforcer

    assert verifier.DomainRules is DomainRules
    assert verifier.MetricsEngine is MetricsEngine
    assert verifier.QCLearning is QCLearning
    assert verifier.SchemaEnforcer is SchemaEnforcer
    assert verifier.TaskSpec is TaskSpec
    assert verifier.TaskSpec.from_mapping({"task_id": "demo", "objective": "check"}).prompt == "check"


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
        json.dumps({"orchestrator_enabled": True, "dry_run": False}),
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


def test_daily_briefing_recent_files_ignores_git_dirs(tmp_path, monkeypatch):
    module = importlib.import_module("scripts.daily_briefing")
    monkeypatch.setattr(module, "ROOT", tmp_path)

    visible = tmp_path / "notes.txt"
    visible.write_text("ok", encoding="utf-8")
    git_file = tmp_path / ".git" / "objects" / "sample"
    git_file.parent.mkdir(parents=True)
    git_file.write_text("internal", encoding="utf-8")

    for path in (visible, git_file):
        path.touch()

    recent = module.recent_files()

    assert visible in recent
    assert git_file not in recent


def test_forgecheck_vendor_rules_import_and_fallback():
    module = importlib.import_module("forgecheck.forgecheck_core.plan.vendor_rules")

    assert module.recommendations_for_system_class("unknown") == [
        {
            "id": "manual_review",
            "severity": "recommended",
            "message": "Review the system classification manually before approving vendor actions.",
        }
    ]


def test_prepare_prompt_replaces_existing_mode_label(monkeypatch):
    module = importlib.import_module("scripts.prepare_prompt")
    copied = {}

    clipboard = SimpleNamespace(
        paste=lambda: "SAUCE: tighten this statement",
        copy=lambda value: copied.setdefault("value", value),
    )
    monkeypatch.setattr(module, "_load_clipboard", lambda: clipboard)
    monkeypatch.setattr(sys, "argv", ["prepare_prompt.py", "translate"])

    assert module.main() == 0
    assert copied["value"] == "TRANSLATE: tighten this statement"


def test_prepare_prompt_errors_when_clipboard_dependency_missing(monkeypatch):
    module = importlib.import_module("scripts.prepare_prompt")
    monkeypatch.setattr(module, "_load_clipboard", lambda: None)
    monkeypatch.setattr(sys, "argv", ["prepare_prompt.py", "TRANSLATE"])

    with pytest.raises(SystemExit):
        module.main()

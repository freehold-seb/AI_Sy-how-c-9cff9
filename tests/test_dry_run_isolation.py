import json

from runner import run_verifier_pipeline


def _write_config(path, *, dry_run, orchestrator_enabled=True):
    path.write_text(
        json.dumps(
            {
                "api_key": "",
                "model": "qwen3:8b",
                "max_history_turns": 30,
                "dry_run": dry_run,
                "admin_timeout_minutes": 60,
                "admin_require_confirmation": True,
                "downloads_dir": "",
                "media_output_dir": "",
                "orchestrator_enabled": orchestrator_enabled,
            }
        ),
        encoding="utf-8",
    )


def test_dry_run_blocks_downstream_selection_and_logs_event(tmp_path, monkeypatch, capfd):
    config_path = tmp_path / "agent_config.json"
    _write_config(config_path, dry_run=True)

    def unexpected_selection(_candidates):
        raise AssertionError("candidate selection must not run during dry-run")

    monkeypatch.setattr(
        run_verifier_pipeline, "choose_best_candidate", unexpected_selection
    )

    result = run_verifier_pipeline.run_pipeline(
        {"task_id": "demo", "objective": "check"},
        candidates=[{"output": "would-run", "score": 1}],
        config_path=config_path,
    )

    assert result == {
        "status": "blocked",
        "task_id": "demo",
        "reason": "dry_run_enabled",
    }
    out, err = capfd.readouterr()
    assert err == ""
    assert '"event": "dry_run_blocked"' in out
    assert '"action": "pipeline_execution"' in out


def test_normal_mode_preserves_candidate_selection(tmp_path, capfd):
    config_path = tmp_path / "agent_config.json"
    _write_config(config_path, dry_run=False)
    candidates = [
        {"output": "low", "score": 1},
        {"output": "high", "score": 2},
    ]

    result = run_verifier_pipeline.run_pipeline(
        {"task_id": "demo", "objective": "check"},
        candidates=candidates,
        config_path=config_path,
    )

    assert result == {
        "status": "verified",
        "task_id": "demo",
        "candidate": candidates[1],
    }
    out, err = capfd.readouterr()
    assert err == ""
    assert "dry_run_blocked" not in out

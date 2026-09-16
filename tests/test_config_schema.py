import pytest

from agent_core.config import validate_config


VALID_CONFIG = {
    "api_key": "",
    "model": "qwen3:8b",
    "max_history_turns": 30,
    "dry_run": True,
    "admin_timeout_minutes": 60,
    "admin_require_confirmation": True,
    "downloads_dir": "",
    "media_output_dir": "",
    "orchestrator_enabled": False,
}


def test_validate_config_accepts_complete_config():
    assert validate_config(VALID_CONFIG) == VALID_CONFIG


def test_validate_config_rejects_missing_required_key():
    config = VALID_CONFIG.copy()
    del config["model"]

    with pytest.raises(ValueError, match="missing config keys"):
        validate_config(config)


def test_validate_config_rejects_unknown_key():
    config = {**VALID_CONFIG, "modle": "typo"}

    with pytest.raises(ValueError, match="unknown config keys"):
        validate_config(config)


def test_validate_config_rejects_wrong_type():
    config = {**VALID_CONFIG, "max_history_turns": "30"}

    with pytest.raises(TypeError, match="max_history_turns"):
        validate_config(config)

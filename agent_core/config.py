"""Strict configuration value parsing."""

from __future__ import annotations

from typing import Any, Mapping


CONFIG_SCHEMA = {
    "api_key": str,
    "model": str,
    "max_history_turns": int,
    "dry_run": bool,
    "admin_timeout_minutes": int,
    "admin_require_confirmation": bool,
    "downloads_dir": str,
    "media_output_dir": str,
    "orchestrator_enabled": bool,
}

def parse_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if not isinstance(value, str):
        raise TypeError("boolean value must be a string or bool")
    normalized = value.strip().lower()
    if normalized == "true":
        return True
    if normalized == "false":
        return False
    raise ValueError("boolean value must be true or false")


def validate_config(config: Mapping[str, Any]) -> Mapping[str, Any]:
    if not isinstance(config, Mapping):
        raise TypeError("config must be a JSON object")

    unknown_keys = set(config) - set(CONFIG_SCHEMA)
    if unknown_keys:
        raise ValueError(f"unknown config keys: {sorted(unknown_keys)}")

    missing_keys = set(CONFIG_SCHEMA) - set(config)
    if missing_keys:
        raise ValueError(f"missing config keys: {sorted(missing_keys)}")

    for key, expected_type in CONFIG_SCHEMA.items():
        value = config[key]
        if expected_type is bool:
            valid = isinstance(value, bool)
        else:
            valid = isinstance(value, expected_type) and not isinstance(value, bool)
        if not valid:
            raise TypeError(f"config key {key!r} must be {expected_type.__name__}")
    return config

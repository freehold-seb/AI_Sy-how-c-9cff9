from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "config" / "agent_config.json"


@dataclass(frozen=True)
class AgentConfig:
    model: str
    max_history_turns: int
    bind_host: str
    control_panel_port: int
    ollama_host: str
    ollama_port: int
    database_path: Path
    system_prompt: str


def load_config(path: Path = CONFIG_PATH) -> AgentConfig:
    raw = json.loads(path.read_text(encoding="utf-8"))
    bind_host = str(raw.get("bind_host", "127.0.0.1"))
    ollama_host = str(raw.get("ollama_host", "127.0.0.1"))
    if bind_host not in {"127.0.0.1", "::1"}:
        raise ValueError("bind_host must be a literal loopback address")
    if ollama_host not in {"127.0.0.1", "::1"}:
        raise ValueError("ollama_host must be a literal loopback address")

    database_value = str(raw.get("database_path", "data/ai_system.sqlite3"))
    database_path = Path(database_value)
    if not database_path.is_absolute():
        database_path = ROOT / database_path

    port = int(raw.get("control_panel_port", 8765))
    ollama_port = int(raw.get("ollama_port", 11434))
    if not 1 <= port <= 65535 or not 1 <= ollama_port <= 65535:
        raise ValueError("configured ports must be between 1 and 65535")

    return AgentConfig(
        model=str(raw.get("model", "qwen3:8b")),
        max_history_turns=max(1, int(raw.get("max_history_turns", 30))),
        bind_host=bind_host,
        control_panel_port=port,
        ollama_host=ollama_host,
        ollama_port=ollama_port,
        database_path=database_path,
        system_prompt=str(
            raw.get(
                "system_prompt",
                "You are a private, local assistant. Be accurate, concise, and explicit about uncertainty.",
            )
        ),
    )

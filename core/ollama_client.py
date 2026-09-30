from __future__ import annotations

import http.client
import json
from dataclasses import dataclass
from typing import Any


class OllamaError(RuntimeError):
    """Raised when the local Ollama service cannot complete a request."""


@dataclass(frozen=True)
class OllamaClient:
    host: str = "127.0.0.1"
    port: int = 11434
    timeout_seconds: float = 180.0

    def __post_init__(self) -> None:
        if self.host not in {"127.0.0.1", "::1"}:
            raise ValueError("Ollama must use a literal loopback address")

    def _request(self, method: str, path: str, payload: dict[str, Any] | None = None) -> dict:
        connection = http.client.HTTPConnection(
            self.host, self.port, timeout=self.timeout_seconds
        )
        body = json.dumps(payload).encode("utf-8") if payload is not None else None
        headers = {"Content-Type": "application/json"} if body is not None else {}
        try:
            connection.request(method, path, body=body, headers=headers)
            response = connection.getresponse()
            raw = response.read(16 * 1024 * 1024)
        except (OSError, TimeoutError, http.client.HTTPException) as exc:
            raise OllamaError(f"local Ollama request failed: {type(exc).__name__}") from exc
        finally:
            connection.close()

        if response.status < 200 or response.status >= 300:
            raise OllamaError(f"local Ollama returned HTTP {response.status}")
        try:
            parsed = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise OllamaError("local Ollama returned invalid JSON") from exc
        if not isinstance(parsed, dict):
            raise OllamaError("local Ollama returned an unexpected response")
        return parsed

    def list_models(self) -> list[str]:
        payload = self._request("GET", "/api/tags")
        models = payload.get("models", [])
        if not isinstance(models, list):
            return []
        return [
            item["name"]
            for item in models
            if isinstance(item, dict) and isinstance(item.get("name"), str)
        ]

    def chat(self, model: str, messages: list[dict[str, str]]) -> str:
        payload = self._request(
            "POST",
            "/api/chat",
            {
                "model": model,
                "messages": messages,
                "stream": False,
                "think": False,
            },
        )
        message = payload.get("message")
        content = message.get("content") if isinstance(message, dict) else None
        if not isinstance(content, str) or not content.strip():
            raise OllamaError("local Ollama returned an empty response")
        return content.strip()

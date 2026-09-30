from __future__ import annotations

import http.client
import json
import sqlite3
import tempfile
import threading
import unittest
from contextlib import closing
from pathlib import Path

from core.agent import LocalAgent
from core.config import AgentConfig
from core.control_panel import ControlPanelServer
from core.ollama_client import OllamaClient
from core.storage import Storage
from services.queue_worker import process_one


class FakeOllamaClient:
    def __init__(self):
        self.requests: list[tuple[str, list[dict[str, str]]]] = []

    def list_models(self) -> list[str]:
        return ["qwen3:8b"]

    def chat(self, model: str, messages: list[dict[str, str]]) -> str:
        self.requests.append((model, messages))
        return f"local response to: {messages[-1]['content']}"


class BlockingOllamaClient(FakeOllamaClient):
    def __init__(self):
        super().__init__()
        self.started = threading.Event()
        self.release = threading.Event()

    def chat(self, model: str, messages: list[dict[str, str]]) -> str:
        self.started.set()
        self.release.wait(timeout=5)
        return super().chat(model, messages)


def make_agent(path: Path) -> LocalAgent:
    config = AgentConfig(
        model="qwen3:8b",
        max_history_turns=10,
        bind_host="127.0.0.1",
        control_panel_port=8765,
        ollama_host="127.0.0.1",
        ollama_port=11434,
        database_path=path,
        system_prompt="Test system prompt",
    )
    return LocalAgent(config, Storage(path), FakeOllamaClient())


class StorageTests(unittest.TestCase):
    def test_conversation_messages_persist_across_instances(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "runtime.sqlite3"
            first = Storage(path)
            conversation_id = first.create_conversation("qwen3:8b")
            first.add_message(conversation_id, "user", "hello")

            second = Storage(path)
            conversation = second.get_conversation(conversation_id)

        self.assertIsNotNone(conversation)
        self.assertEqual(conversation["messages"][0]["content"], "hello")

    def test_queue_claim_and_completion(self):
        with tempfile.TemporaryDirectory() as directory:
            storage = Storage(Path(directory) / "runtime.sqlite3")
            job_id = storage.enqueue("do work")
            claimed = storage.claim_next_job()
            storage.finish_job(job_id, "done", None)
            finished = storage.get_job(job_id)

        self.assertEqual(claimed["id"], job_id)
        self.assertEqual(finished["status"], "completed")
        self.assertEqual(finished["result"], "done")

    def test_expired_running_job_is_reclaimed(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "runtime.sqlite3"
            storage = Storage(path)
            job_id = storage.enqueue("retry work")
            storage.claim_next_job()
            with closing(sqlite3.connect(path)) as connection, connection:
                connection.execute(
                    "UPDATE jobs SET lease_expires_at='2000-01-01T00:00:00Z' WHERE id=?",
                    (job_id,),
                )
            reclaimed = storage.claim_next_job()
        self.assertEqual(reclaimed["id"], job_id)


class AgentTests(unittest.TestCase):
    def test_chat_persists_user_and_assistant_messages(self):
        with tempfile.TemporaryDirectory() as directory:
            agent = make_agent(Path(directory) / "runtime.sqlite3")
            result = agent.chat("hello")
            conversation = agent.storage.get_conversation(result["conversation_id"])

        self.assertEqual(result["response"], "local response to: hello")
        self.assertEqual(
            [message["role"] for message in conversation["messages"]],
            ["user", "assistant"],
        )

    def test_health_reports_configured_model(self):
        with tempfile.TemporaryDirectory() as directory:
            health = make_agent(Path(directory) / "runtime.sqlite3").health()
        self.assertEqual(health["status"], "ok")
        self.assertEqual(health["model"], "qwen3:8b")

    def test_queue_worker_processes_one_job(self):
        with tempfile.TemporaryDirectory() as directory:
            agent = make_agent(Path(directory) / "runtime.sqlite3")
            job_id = agent.storage.enqueue("queued prompt")
            processed = process_one(agent)
            job = agent.storage.get_job(job_id)
        self.assertTrue(processed)
        self.assertEqual(job["status"], "completed")

    def test_delete_waits_for_active_conversation_turn(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "runtime.sqlite3"
            agent = make_agent(path)
            blocking_client = BlockingOllamaClient()
            agent.client = blocking_client
            conversation_id = agent.storage.create_conversation("qwen3:8b")
            errors: list[Exception] = []
            deleted: list[bool] = []
            delete_started = threading.Event()

            def run_chat():
                try:
                    agent.chat("hello", conversation_id)
                except Exception as exc:
                    errors.append(exc)

            chat_thread = threading.Thread(target=run_chat)
            def run_delete():
                delete_started.set()
                deleted.append(agent.delete_conversation(conversation_id))

            delete_thread = threading.Thread(target=run_delete)
            chat_thread.start()
            self.assertTrue(blocking_client.started.wait(timeout=2))
            delete_thread.start()
            self.assertTrue(delete_started.wait(timeout=2))
            self.assertTrue(delete_thread.is_alive())
            blocking_client.release.set()
            chat_thread.join(timeout=5)
            delete_thread.join(timeout=5)

        self.assertEqual(errors, [])
        self.assertEqual(deleted, [True])


class ControlPanelTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.agent = make_agent(
            Path(self.temporary_directory.name) / "runtime.sqlite3"
        )
        self.server = ControlPanelServer(("127.0.0.1", 0), self.agent)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.port = self.server.server_address[1]

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)
        self.temporary_directory.cleanup()

    def request(
        self,
        method: str,
        path: str,
        payload: dict | None = None,
        headers: dict[str, str] | None = None,
    ):
        connection = http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)
        body = json.dumps(payload) if payload is not None else None
        request_headers = {"Content-Type": "application/json"} if body else {}
        request_headers.update(headers or {})
        connection.request(method, path, body=body, headers=request_headers)
        response = connection.getresponse()
        raw = response.read()
        connection.close()
        return response.status, response.headers, json.loads(raw) if raw else None

    def test_health_and_chat_routes(self):
        status, headers, health = self.request("GET", "/api/health")
        self.assertEqual(status, 200)
        self.assertEqual(health["status"], "ok")
        self.assertEqual(headers["X-Frame-Options"], "DENY")

        status, _, reply = self.request(
            "POST", "/api/chat", {"message": "hello", "model": "qwen3:8b"}
        )
        self.assertEqual(status, 200)
        self.assertEqual(reply["response"], "local response to: hello")

        status, _, conversation = self.request(
            "GET", f"/api/conversations/{reply['conversation_id']}"
        )
        self.assertEqual(status, 200)
        self.assertEqual(len(conversation["messages"]), 2)

    def test_rejects_non_loopback_bind(self):
        with self.assertRaises(ValueError):
            ControlPanelServer(("0.0.0.0", 0), self.agent)

    def test_rejects_cross_origin_write(self):
        status, _, payload = self.request(
            "POST",
            "/api/jobs",
            {"prompt": "do work"},
            {"Origin": "https://attacker.example"},
        )
        self.assertEqual(status, 403)
        self.assertIn("cross-origin", payload["error"])

    def test_rejects_invalid_field_types(self):
        status, _, payload = self.request(
            "POST", "/api/chat", {"message": "hello", "model": 123}
        )
        self.assertEqual(status, 400)
        self.assertEqual(payload["error"], "model must be a string")

    def test_rejects_non_json_write(self):
        status, _, payload = self.request(
            "POST",
            "/api/jobs",
            {"prompt": "do work"},
            {"Content-Type": "text/plain"},
        )
        self.assertEqual(status, 400)
        self.assertIn("application/json", payload["error"])

    def test_rejects_oversized_queued_prompt(self):
        status, _, payload = self.request(
            "POST", "/api/jobs", {"prompt": "x" * 100_001}
        )
        self.assertEqual(status, 400)
        self.assertIn("100000", payload["error"])


class OllamaClientTests(unittest.TestCase):
    def test_rejects_remote_host(self):
        with self.assertRaises(ValueError):
            OllamaClient("example.com")


if __name__ == "__main__":
    unittest.main()

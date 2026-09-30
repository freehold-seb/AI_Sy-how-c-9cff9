from __future__ import annotations

import json
import sqlite3
import uuid
from contextlib import closing
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class Storage:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path, timeout=10)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA journal_mode = WAL")
        return connection

    def _initialize(self) -> None:
        with closing(self._connect()) as connection, connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS conversations (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    model TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id TEXT NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
                    role TEXT NOT NULL CHECK(role IN ('user', 'assistant', 'system')),
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_messages_conversation
                    ON messages(conversation_id, id);
                CREATE TABLE IF NOT EXISTS jobs (
                    id TEXT PRIMARY KEY,
                    prompt TEXT NOT NULL,
                    model TEXT,
                    status TEXT NOT NULL,
                    result TEXT,
                    error TEXT,
                    attempts INTEGER NOT NULL DEFAULT 0,
                    lease_expires_at TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
                """
            )
            columns = {
                row["name"]
                for row in connection.execute("PRAGMA table_info(jobs)").fetchall()
            }
            if "attempts" not in columns:
                connection.execute(
                    "ALTER TABLE jobs ADD COLUMN attempts INTEGER NOT NULL DEFAULT 0"
                )
            if "lease_expires_at" not in columns:
                connection.execute("ALTER TABLE jobs ADD COLUMN lease_expires_at TEXT")

    def create_conversation(self, model: str, title: str | None = None) -> str:
        conversation_id = uuid.uuid4().hex
        now = utc_now()
        safe_title = (title or "New conversation").strip()[:120] or "New conversation"
        with closing(self._connect()) as connection, connection:
            connection.execute(
                "INSERT INTO conversations(id,title,model,created_at,updated_at) VALUES(?,?,?,?,?)",
                (conversation_id, safe_title, model, now, now),
            )
        return conversation_id

    def conversation_exists(self, conversation_id: str) -> bool:
        with closing(self._connect()) as connection, connection:
            row = connection.execute(
                "SELECT 1 FROM conversations WHERE id=?", (conversation_id,)
            ).fetchone()
        return row is not None

    def add_message(self, conversation_id: str, role: str, content: str) -> None:
        now = utc_now()
        with closing(self._connect()) as connection, connection:
            connection.execute(
                "INSERT INTO messages(conversation_id,role,content,created_at) VALUES(?,?,?,?)",
                (conversation_id, role, content, now),
            )
            connection.execute(
                "UPDATE conversations SET updated_at=? WHERE id=?",
                (now, conversation_id),
            )

    def update_title_from_message(self, conversation_id: str, message: str) -> None:
        title = " ".join(message.strip().split())[:80]
        if not title:
            return
        with closing(self._connect()) as connection, connection:
            connection.execute(
                "UPDATE conversations SET title=? WHERE id=? AND title='New conversation'",
                (title, conversation_id),
            )

    def get_messages(self, conversation_id: str, limit: int = 60) -> list[dict[str, str]]:
        with closing(self._connect()) as connection, connection:
            rows = connection.execute(
                """
                SELECT role,content,created_at FROM (
                    SELECT id,role,content,created_at
                    FROM messages WHERE conversation_id=?
                    ORDER BY id DESC LIMIT ?
                ) ORDER BY id
                """,
                (conversation_id, limit),
            ).fetchall()
        return [dict(row) for row in rows]

    def list_conversations(self, limit: int = 50) -> list[dict[str, Any]]:
        with closing(self._connect()) as connection, connection:
            rows = connection.execute(
                """
                SELECT c.id,c.title,c.model,c.created_at,c.updated_at,
                       COUNT(m.id) AS message_count
                FROM conversations c
                LEFT JOIN messages m ON m.conversation_id=c.id
                GROUP BY c.id
                ORDER BY c.updated_at DESC LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [dict(row) for row in rows]

    def get_conversation(self, conversation_id: str) -> dict[str, Any] | None:
        with closing(self._connect()) as connection, connection:
            row = connection.execute(
                "SELECT id,title,model,created_at,updated_at FROM conversations WHERE id=?",
                (conversation_id,),
            ).fetchone()
        if row is None:
            return None
        result = dict(row)
        result["messages"] = self.get_messages(conversation_id, limit=500)
        return result

    def delete_conversation(self, conversation_id: str) -> bool:
        with closing(self._connect()) as connection, connection:
            cursor = connection.execute(
                "DELETE FROM conversations WHERE id=?", (conversation_id,)
            )
        return cursor.rowcount > 0

    def enqueue(self, prompt: str, model: str | None = None) -> str:
        job_id = uuid.uuid4().hex
        now = utc_now()
        with closing(self._connect()) as connection, connection:
            connection.execute(
                "INSERT INTO jobs(id,prompt,model,status,created_at,updated_at) VALUES(?,?,?,?,?,?)",
                (job_id, prompt, model, "pending", now, now),
            )
        return job_id

    def claim_next_job(self) -> dict[str, Any] | None:
        with closing(self._connect()) as connection, connection:
            connection.execute("BEGIN IMMEDIATE")
            now = utc_now()
            connection.execute(
                """
                UPDATE jobs
                SET status='failed',
                    error='job lease expired after retry limit',
                    lease_expires_at=NULL,
                    updated_at=?
                WHERE status='running'
                  AND lease_expires_at<=?
                  AND attempts>=3
                """,
                (now, now),
            )
            row = connection.execute(
                """
                SELECT id,prompt,model FROM jobs
                WHERE attempts<3
                  AND (
                    status='pending'
                    OR (status='running' AND lease_expires_at<=?)
                  )
                ORDER BY created_at LIMIT 1
                """,
                (now,),
            ).fetchone()
            if row is None:
                return None
            lease_expires_at = (
                datetime.now(timezone.utc) + timedelta(hours=1)
            ).strftime("%Y-%m-%dT%H:%M:%SZ")
            connection.execute(
                """
                UPDATE jobs
                SET status='running',
                    attempts=attempts+1,
                    lease_expires_at=?,
                    updated_at=?
                WHERE id=?
                """,
                (lease_expires_at, now, row["id"]),
            )
        return dict(row)

    def finish_job(self, job_id: str, result: str | None, error: str | None) -> None:
        status = "failed" if error else "completed"
        with closing(self._connect()) as connection, connection:
            connection.execute(
                """
                UPDATE jobs
                SET status=?,result=?,error=?,lease_expires_at=NULL,updated_at=?
                WHERE id=?
                """,
                (status, result, error, utc_now(), job_id),
            )

    def get_job(self, job_id: str) -> dict[str, Any] | None:
        with closing(self._connect()) as connection, connection:
            row = connection.execute(
                """
                SELECT id,prompt,model,status,result,error,attempts,
                       lease_expires_at,created_at,updated_at
                FROM jobs WHERE id=?
                """,
                (job_id,),
            ).fetchone()
        return dict(row) if row is not None else None

    def export_conversation_json(self, conversation_id: str) -> str:
        conversation = self.get_conversation(conversation_id)
        if conversation is None:
            raise KeyError(conversation_id)
        return json.dumps(conversation, indent=2, ensure_ascii=False)

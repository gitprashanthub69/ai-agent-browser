"""SQLite-backed memory store for profiles, notes, forms, contacts, and history."""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional

DB_PATH = Path(__file__).resolve().parents[1] / "data" / "memory.db"


def _conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _now() -> str:
    return datetime.utcnow().isoformat()


def init_db() -> None:
    with _conn() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS profile (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                category TEXT DEFAULT 'general',
                updated_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                doc_type TEXT NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                tags TEXT DEFAULT '[]',
                used_count INTEGER DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS form_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                form_title TEXT DEFAULT '',
                fields_json TEXT NOT NULL,
                submitted INTEGER DEFAULT 0,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT DEFAULT '',
                content TEXT NOT NULL,
                source_url TEXT DEFAULT '',
                tags TEXT DEFAULT '[]',
                note_type TEXT DEFAULT 'summary',
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT DEFAULT '',
                group_name TEXT DEFAULT '',
                notes TEXT DEFAULT '',
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS task_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                command TEXT NOT NULL,
                modules TEXT DEFAULT '[]',
                result_json TEXT DEFAULT '{}',
                status TEXT DEFAULT 'completed',
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS preferences (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS email_templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                subject TEXT NOT NULL,
                body TEXT NOT NULL,
                used_count INTEGER DEFAULT 0,
                created_at TEXT NOT NULL
            );
            """
        )


def get_profile() -> dict:
    init_db()
    with _conn() as conn:
        rows = conn.execute("SELECT key, value, category FROM profile").fetchall()
    return {row["key"]: row["value"] for row in rows}


def set_profile_field(key: str, value: str, category: str = "general") -> None:
    init_db()
    with _conn() as conn:
        conn.execute(
            "INSERT INTO profile (key, value, category, updated_at) VALUES (?,?,?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value, updated_at=excluded.updated_at",
            (key, value, category, _now()),
        )


def set_profile_bulk(data: dict, category: str = "general") -> None:
    for key, value in data.items():
        set_profile_field(str(key), str(value), category)


def save_document(doc_type: str, title: str, content: str, tags: Optional[list] = None) -> int:
    init_db()
    with _conn() as conn:
        cursor = conn.execute(
            "INSERT INTO documents (doc_type, title, content, tags, created_at, updated_at) VALUES (?,?,?,?,?,?)",
            (doc_type, title, content, json.dumps(tags or []), _now(), _now()),
        )
        return cursor.lastrowid


def get_documents(doc_type: Optional[str] = None) -> list[dict]:
    init_db()
    with _conn() as conn:
        if doc_type:
            rows = conn.execute("SELECT * FROM documents WHERE doc_type=? ORDER BY used_count DESC", (doc_type,)).fetchall()
        else:
            rows = conn.execute("SELECT * FROM documents ORDER BY used_count DESC").fetchall()
    return [dict(row) for row in rows]


def save_form_history(url: str, form_title: str, fields: list[dict], submitted: bool = True) -> None:
    init_db()
    with _conn() as conn:
        conn.execute(
            "INSERT INTO form_history (url, form_title, fields_json, submitted, created_at) VALUES (?,?,?,?,?)",
            (url, form_title, json.dumps(fields), int(submitted), _now()),
        )


def get_form_history(limit: int = 20) -> list[dict]:
    init_db()
    with _conn() as conn:
        rows = conn.execute("SELECT * FROM form_history ORDER BY created_at DESC LIMIT ?", (limit,)).fetchall()
    result = []
    for row in rows:
        data = dict(row)
        data["fields"] = json.loads(data["fields_json"])
        result.append(data)
    return result


def save_note(content: str, title: str = "", source_url: str = "", tags: Optional[list] = None, note_type: str = "summary") -> int:
    init_db()
    with _conn() as conn:
        cursor = conn.execute(
            "INSERT INTO notes (title, content, source_url, tags, note_type, created_at) VALUES (?,?,?,?,?,?)",
            (title, content, source_url, json.dumps(tags or []), note_type, _now()),
        )
        return cursor.lastrowid


def get_notes(note_type: Optional[str] = None, limit: int = 50) -> list[dict]:
    init_db()
    with _conn() as conn:
        if note_type:
            rows = conn.execute("SELECT * FROM notes WHERE note_type=? ORDER BY created_at DESC LIMIT ?", (note_type, limit)).fetchall()
        else:
            rows = conn.execute("SELECT * FROM notes ORDER BY created_at DESC LIMIT ?", (limit,)).fetchall()
    return [dict(row) for row in rows]


def search_history(query: str) -> list[dict]:
    init_db()
    q = f"%{query}%"
    results = []
    with _conn() as conn:
        notes = conn.execute("SELECT 'note' as source, title, content, created_at FROM notes WHERE title LIKE ? OR content LIKE ? LIMIT 5", (q, q)).fetchall()
        results.extend([dict(row) for row in notes])
        forms = conn.execute("SELECT 'form' as source, form_title as title, fields_json as content, created_at FROM form_history WHERE form_title LIKE ? OR fields_json LIKE ? LIMIT 5", (q, q)).fetchall()
        results.extend([dict(row) for row in forms])
        tasks = conn.execute("SELECT 'task' as source, command as title, result_json as content, created_at FROM task_history WHERE command LIKE ? OR result_json LIKE ? LIMIT 5", (q, q)).fetchall()
        results.extend([dict(row) for row in tasks])
    return results


def save_task(command: str, modules: Optional[list] = None, result_json: Optional[dict] = None, status: str = "completed") -> None:
    init_db()
    with _conn() as conn:
        conn.execute(
            "INSERT INTO task_history (command, modules, result_json, status, created_at) VALUES (?,?,?,?,?)",
            (command, json.dumps(modules or []), json.dumps(result_json or {}), status, _now()),
        )


if __name__ == "__main__":
    init_db()
    print("Memory store initialized")

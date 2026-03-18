from __future__ import annotations

import os
import sqlite3
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

DEFAULT_DB_PATH = Path(__file__).resolve().parent / "taskhub.db"
VALID_STATUSES = {"ACTIVE", "COMPLETED"}
VALID_PRIORITIES = {"LOW", "MEDIUM", "HIGH"}
_MISSING = object()


def get_db_path(db_path: str | Path | None = None) -> Path:
    if db_path is not None:
        return Path(db_path)
    env_path = os.getenv("TASKHUB_DB_PATH")
    if env_path:
        return Path(env_path)
    return DEFAULT_DB_PATH


def connect(db_path: str | Path | None = None) -> sqlite3.Connection:
    resolved_path = get_db_path(db_path)
    resolved_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(resolved_path)
    connection.row_factory = sqlite3.Row
    return connection


@contextmanager
def managed_connection(db_path: str | Path | None = None):
    connection = connect(db_path)
    try:
        yield connection
    finally:
        connection.close()


def init_database(db_path: str | Path | None = None) -> None:
    with managed_connection(db_path) as connection:
        connection.executescript(
            """
            PRAGMA foreign_keys = ON;

            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password_hash TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                status TEXT NOT NULL DEFAULT 'ACTIVE' CHECK (status IN ('ACTIVE', 'COMPLETED')),
                priority TEXT NOT NULL DEFAULT 'MEDIUM'
                    CHECK (priority IN ('LOW', 'MEDIUM', 'HIGH')),
                due_date TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                owner_username TEXT NOT NULL,
                FOREIGN KEY(owner_username) REFERENCES users(username) ON DELETE CASCADE
            );
            """
        )
        connection.commit()


def reset_database(db_path: str | Path | None = None) -> None:
    resolved_path = get_db_path(db_path)
    if resolved_path.exists():
        resolved_path.unlink()
    init_database(resolved_path)


def upsert_user(
    username: str, password_hash: str, db_path: str | Path | None = None
) -> dict[str, Any]:
    normalized_username = username.strip()
    if not normalized_username:
        raise ValueError("Username is required.")
    if not password_hash:
        raise ValueError("Password hash is required.")

    with managed_connection(db_path) as connection:
        connection.execute(
            """
            INSERT INTO users (username, password_hash)
            VALUES (?, ?)
            ON CONFLICT(username) DO UPDATE SET password_hash = excluded.password_hash
            """,
            (normalized_username, password_hash),
        )
        connection.commit()

    user = get_user(normalized_username, db_path)
    if user is None:
        raise RuntimeError("Failed to read back user after upsert.")
    return user


def get_user(username: str, db_path: str | Path | None = None) -> dict[str, Any] | None:
    with managed_connection(db_path) as connection:
        row = connection.execute(
            "SELECT username, password_hash FROM users WHERE username = ?",
            (username,),
        ).fetchone()
    return _row_to_dict(row)


def list_tasks(
    owner_username: str,
    status_filter: str = "all",
    db_path: str | Path | None = None,
) -> list[dict[str, Any]]:
    normalized_filter = status_filter.lower().strip()
    status_value: str | None
    if normalized_filter == "all":
        status_value = None
    elif normalized_filter == "active":
        status_value = "ACTIVE"
    elif normalized_filter == "completed":
        status_value = "COMPLETED"
    else:
        raise ValueError("Invalid filter. Use all, active, or completed.")

    query = """
        SELECT
            id,
            title,
            description,
            status,
            priority,
            due_date,
            created_at,
            updated_at,
            owner_username
        FROM tasks
        WHERE owner_username = ?
    """
    params: list[Any] = [owner_username]

    if status_value is not None:
        query += " AND status = ?"
        params.append(status_value)

    query += """
        ORDER BY
            CASE status WHEN 'ACTIVE' THEN 0 ELSE 1 END,
            due_date IS NULL,
            due_date,
            updated_at DESC,
            id DESC
    """

    with managed_connection(db_path) as connection:
        rows = connection.execute(query, params).fetchall()
    return [_row_to_dict(row) for row in rows]


def create_task(
    owner_username: str,
    title: str,
    description: str | None = None,
    status: str = "ACTIVE",
    priority: str = "MEDIUM",
    due_date: str | None = None,
    db_path: str | Path | None = None,
) -> dict[str, Any]:
    normalized_title = _normalize_required_title(title)
    normalized_description = _normalize_optional_text(description)
    normalized_status = _normalize_status(status)
    normalized_priority = _normalize_priority(priority)
    normalized_due_date = _normalize_optional_date(due_date)
    timestamp = _utc_now_iso()

    with managed_connection(db_path) as connection:
        cursor = connection.execute(
            """
            INSERT INTO tasks (
                title,
                description,
                status,
                priority,
                due_date,
                created_at,
                updated_at,
                owner_username
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                normalized_title,
                normalized_description,
                normalized_status,
                normalized_priority,
                normalized_due_date,
                timestamp,
                timestamp,
                owner_username,
            ),
        )
        task_id = int(cursor.lastrowid)
        connection.commit()

    task = get_task_by_id(task_id, owner_username, db_path)
    if task is None:
        raise RuntimeError("Failed to read back task after creation.")
    return task


def get_task_by_id(
    task_id: int,
    owner_username: str,
    db_path: str | Path | None = None,
) -> dict[str, Any] | None:
    with managed_connection(db_path) as connection:
        row = connection.execute(
            """
            SELECT
                id,
                title,
                description,
                status,
                priority,
                due_date,
                created_at,
                updated_at,
                owner_username
            FROM tasks
            WHERE id = ? AND owner_username = ?
            """,
            (task_id, owner_username),
        ).fetchone()
    return _row_to_dict(row)


def get_task_owner(
    task_id: int,
    db_path: str | Path | None = None,
) -> str | None:
    """Return the owner_username of a task regardless of ownership, or None if not found."""
    with managed_connection(db_path) as connection:
        row = connection.execute(
            "SELECT owner_username FROM tasks WHERE id = ?",
            (task_id,),
        ).fetchone()
    return row["owner_username"] if row else None


def update_task(
    task_id: int,
    owner_username: str,
    *,
    title: str | object = _MISSING,
    description: str | None | object = _MISSING,
    status: str | object = _MISSING,
    priority: str | object = _MISSING,
    due_date: str | None | object = _MISSING,
    db_path: str | Path | None = None,
) -> dict[str, Any] | None:
    current_task = get_task_by_id(task_id, owner_username, db_path)
    if current_task is None:
        return None

    next_title = _normalize_required_title(
        current_task["title"] if title is _MISSING else _to_optional_str(title)
    )
    next_description = _normalize_optional_text(
        current_task["description"] if description is _MISSING else _to_optional_str(description)
    )
    next_status = _normalize_status(
        current_task["status"] if status is _MISSING else _to_optional_str(status)
    )
    next_priority = _normalize_priority(
        current_task["priority"] if priority is _MISSING else _to_optional_str(priority)
    )
    next_due_date = _normalize_optional_date(
        current_task["due_date"] if due_date is _MISSING else _to_optional_str(due_date)
    )

    with managed_connection(db_path) as connection:
        connection.execute(
            """
            UPDATE tasks
            SET
                title = ?,
                description = ?,
                status = ?,
                priority = ?,
                due_date = ?,
                updated_at = ?
            WHERE id = ? AND owner_username = ?
            """,
            (
                next_title,
                next_description,
                next_status,
                next_priority,
                next_due_date,
                _utc_now_iso(),
                task_id,
                owner_username,
            ),
        )
        connection.commit()

    return get_task_by_id(task_id, owner_username, db_path)


def delete_task(task_id: int, owner_username: str, db_path: str | Path | None = None) -> bool:
    with managed_connection(db_path) as connection:
        cursor = connection.execute(
            "DELETE FROM tasks WHERE id = ? AND owner_username = ?",
            (task_id, owner_username),
        )
        connection.commit()
    return cursor.rowcount > 0


def delete_tasks_for_owner(owner_username: str, db_path: str | Path | None = None) -> int:
    with managed_connection(db_path) as connection:
        cursor = connection.execute("DELETE FROM tasks WHERE owner_username = ?", (owner_username,))
        connection.commit()
    return cursor.rowcount


def count_all_tasks(db_path: str | Path | None = None) -> int:
    with managed_connection(db_path) as connection:
        row = connection.execute("SELECT COUNT(1) AS task_count FROM tasks").fetchone()
    if row is None:
        return 0
    return int(row["task_count"])


def count_tasks_for_owner(owner_username: str, db_path: str | Path | None = None) -> int:
    with managed_connection(db_path) as connection:
        row = connection.execute(
            "SELECT COUNT(1) AS task_count FROM tasks WHERE owner_username = ?",
            (owner_username,),
        ).fetchone()
    if row is None:
        return 0
    return int(row["task_count"])


def reset_task_id_sequence(db_path: str | Path | None = None) -> None:
    with managed_connection(db_path) as connection:
        connection.execute("DELETE FROM sqlite_sequence WHERE name = 'tasks'")
        connection.commit()


def _normalize_required_title(value: str | None) -> str:
    if value is None:
        raise ValueError("Title is required.")
    normalized = value.strip()
    if not normalized:
        raise ValueError("Title is required.")
    return normalized


def _normalize_optional_text(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = value.strip()
    return normalized or None


def _normalize_status(value: str | None) -> str:
    if value is None:
        raise ValueError("Status must be ACTIVE or COMPLETED.")
    normalized = value.strip().upper()
    if normalized not in VALID_STATUSES:
        raise ValueError("Status must be ACTIVE or COMPLETED.")
    return normalized


def _normalize_priority(value: str | None) -> str:
    if value is None:
        raise ValueError("Priority must be LOW, MEDIUM, or HIGH.")
    normalized = value.strip().upper()
    if normalized not in VALID_PRIORITIES:
        raise ValueError("Priority must be LOW, MEDIUM, or HIGH.")
    return normalized


def _normalize_optional_date(value: str | None) -> str | None:
    normalized = _normalize_optional_text(value)
    if normalized is None:
        return None

    try:
        datetime.strptime(normalized, "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError("Due date must use YYYY-MM-DD format.") from exc

    return normalized


def _row_to_dict(row: sqlite3.Row | None) -> dict[str, Any] | None:
    if row is None:
        return None
    return {key: row[key] for key in row.keys()}


def _utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def _to_optional_str(value: object) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        return value
    return str(value)

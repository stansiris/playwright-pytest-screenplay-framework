"""Deterministic seed helpers for TaskHub users and tasks."""

from __future__ import annotations

from typing import Any

from werkzeug.security import generate_password_hash

from . import db

DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = "admin123"

DEFAULT_TASKS: tuple[dict[str, Any], ...] = (
    {
        "title": "Review TaskHub smoke checks",
        "description": "Confirm login, create, edit, complete, and delete all behave as expected.",
        "status": "ACTIVE",
        "priority": "HIGH",
        "due_date": "2030-01-15",
    },
    {
        "title": "Document API examples",
        "description": "Add curl examples for CRUD endpoints in README.",
        "status": "ACTIVE",
        "priority": "MEDIUM",
        "due_date": "2030-01-20",
    },
    {
        "title": "Archive old exploratory notes",
        "description": "Cleanup notes that are no longer needed.",
        "status": "COMPLETED",
        "priority": "LOW",
        "due_date": None,
    },
)


def seed_default_user(db_path: str | None = None) -> dict[str, Any]:
    return db.upsert_user(
        DEFAULT_USERNAME,
        generate_password_hash(DEFAULT_PASSWORD),
        db_path=db_path,
    )


def seed_default_tasks(
    *,
    owner_username: str = DEFAULT_USERNAME,
    replace_existing: bool = True,
    db_path: str | None = None,
) -> list[dict[str, Any]]:
    if replace_existing:
        db.delete_tasks_for_owner(owner_username, db_path=db_path)
        if db.count_all_tasks(db_path=db_path) == 0:
            db.reset_task_id_sequence(db_path=db_path)

    created_tasks: list[dict[str, Any]] = []
    for task in DEFAULT_TASKS:
        created_tasks.append(
            db.create_task(
                owner_username=owner_username,
                title=task["title"],
                description=task["description"],
                status=task["status"],
                priority=task["priority"],
                due_date=task["due_date"],
                db_path=db_path,
            )
        )
    return created_tasks


def reset_and_seed(db_path: str | None = None) -> dict[str, Any]:
    db.reset_database(db_path=db_path)
    seed_default_user(db_path=db_path)
    tasks = seed_default_tasks(db_path=db_path, replace_existing=True)
    return {
        "username": DEFAULT_USERNAME,
        "task_count": len(tasks),
    }

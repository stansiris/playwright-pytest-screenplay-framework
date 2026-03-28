"""Deterministic seed helpers for Work Items users and work items."""

from __future__ import annotations

from typing import Any

from werkzeug.security import generate_password_hash

from . import db

DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = "admin123"

SECONDARY_USERNAME = "guest"
SECONDARY_PASSWORD = "guest123"

DEFAULT_WORK_ITEMS: tuple[dict[str, Any], ...] = (
    {
        "title": "Review Work Items smoke checks",
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


def seed_secondary_user(db_path: str | None = None) -> dict[str, Any]:
    return db.upsert_user(
        SECONDARY_USERNAME,
        generate_password_hash(SECONDARY_PASSWORD),
        db_path=db_path,
    )


def seed_default_work_items(
    *,
    owner_username: str = DEFAULT_USERNAME,
    replace_existing: bool = True,
    db_path: str | None = None,
) -> list[dict[str, Any]]:
    if replace_existing:
        db.delete_work_items_for_owner(owner_username, db_path=db_path)
        if db.count_all_work_items(db_path=db_path) == 0:
            db.reset_work_item_id_sequence(db_path=db_path)

    created_work_items: list[dict[str, Any]] = []
    for work_item in DEFAULT_WORK_ITEMS:
        created_work_items.append(
            db.create_work_item(
                owner_username=owner_username,
                title=work_item["title"],
                description=work_item["description"],
                status=work_item["status"],
                priority=work_item["priority"],
                due_date=work_item["due_date"],
                db_path=db_path,
            )
        )
    return created_work_items


def reset_and_seed(db_path: str | None = None) -> dict[str, Any]:
    db.reset_database(db_path=db_path)
    seed_default_user(db_path=db_path)
    seed_secondary_user(db_path=db_path)
    work_items = seed_default_work_items(db_path=db_path, replace_existing=True)
    return {
        "username": DEFAULT_USERNAME,
        "secondary_username": SECONDARY_USERNAME,
        "work_item_count": len(work_items),
    }

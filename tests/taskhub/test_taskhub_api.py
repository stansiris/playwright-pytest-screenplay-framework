"""TaskHub API integration tests using Screenplay API Tasks and Questions."""

from __future__ import annotations

import pytest

from examples.taskhub.automation.questions.api_questions import (
    CurrentUserViaApi,
    FetchTasksViaApi,
    FetchTaskViaApi,
    TaskExistsViaApi,
    TaskFieldEqualsViaApi,
)
from examples.taskhub.automation.tasks.api_tasks import (
    CreateTaskViaApi,
    DeleteTaskViaApi,
    LoginToTaskHubApi,
    ResetTaskHubDataViaApi,
    SeedTaskHubDataViaApi,
    UpdateTaskViaApi,
)
from screenplay_core.core.actor import Actor

pytestmark = [pytest.mark.api, pytest.mark.integration]


def _items_from_tasks_payload(payload: object) -> list[dict]:
    if not isinstance(payload, dict):
        return []

    items = payload.get("items")
    if not isinstance(items, list):
        return []

    return [item for item in items if isinstance(item, dict)]


def _current_task_snapshot(taskhub_api_actor: Actor) -> list[dict]:
    taskhub_api_actor.attempts_to(LoginToTaskHubApi.with_credentials("admin", "admin123"))
    tasks_response = taskhub_api_actor.asks_for(FetchTasksViaApi.all())
    assert tasks_response.status_code == 200

    return [
        {
            "id": item.get("id"),
            "title": item.get("title"),
            "description": item.get("description"),
            "status": item.get("status"),
            "priority": item.get("priority"),
            "due_date": item.get("due_date"),
        }
        for item in _items_from_tasks_payload(tasks_response.payload)
    ]


def test_api_login(taskhub_api_actor: Actor) -> None:
    """Verify API login returns a 200 with the authenticated user's profile."""
    login = LoginToTaskHubApi.with_credentials("admin", "admin123")
    taskhub_api_actor.attempts_to(login)
    assert login.result.status_code == 200
    assert isinstance(login.result.payload, dict)
    assert login.result.payload["username"] == "admin"

    me_response = taskhub_api_actor.asks_for(CurrentUserViaApi())
    assert me_response.status_code == 200
    assert isinstance(me_response.payload, dict)
    assert me_response.payload["username"] == "admin"


def test_api_get_tasks(taskhub_api_actor: Actor) -> None:
    """Verify the tasks endpoint returns the seeded task list after login."""
    taskhub_api_actor.attempts_to(LoginToTaskHubApi.with_credentials("admin", "admin123"))
    tasks_response = taskhub_api_actor.asks_for(FetchTasksViaApi.all())
    assert tasks_response.status_code == 200
    assert len(_items_from_tasks_payload(tasks_response.payload)) >= 3


def test_api_create_task(taskhub_api_actor: Actor) -> None:
    """Verify creating a task via API returns 201 and the task is retrievable."""
    create_task = CreateTaskViaApi.with_payload(
        {
            "title": "API create task",
            "description": "Created through API test",
            "priority": "HIGH",
            "due_date": "2030-04-01",
        }
    )
    taskhub_api_actor.attempts_to(
        LoginToTaskHubApi.with_credentials("admin", "admin123"),
        create_task,
    )

    assert create_task.result.status_code == 201
    assert isinstance(create_task.result.payload, dict)
    assert create_task.result.payload["title"] == "API create task"
    assert create_task.result.payload["status"] == "ACTIVE"
    assert create_task.task_id is not None
    assert taskhub_api_actor.asks_for(TaskExistsViaApi(create_task.task_id))
    assert taskhub_api_actor.asks_for(
        TaskFieldEqualsViaApi(create_task.task_id, "description", "Created through API test")
    )


def test_api_update_task(taskhub_api_actor: Actor) -> None:
    """Verify updating a task via API persists the new title, priority, and status."""
    create_task = CreateTaskViaApi.with_payload({"title": "API update target", "priority": "LOW"})
    taskhub_api_actor.attempts_to(
        LoginToTaskHubApi.with_credentials("admin", "admin123"),
        create_task,
    )
    assert create_task.task_id is not None

    update_task = UpdateTaskViaApi.for_task(
        create_task.task_id,
        {
            "title": "API updated task",
            "description": "Updated via API",
            "priority": "MEDIUM",
            "status": "COMPLETED",
        },
    )
    taskhub_api_actor.attempts_to(update_task)

    assert update_task.result.status_code == 200
    assert taskhub_api_actor.asks_for(
        TaskFieldEqualsViaApi(create_task.task_id, "title", "API updated task")
    )
    assert taskhub_api_actor.asks_for(
        TaskFieldEqualsViaApi(create_task.task_id, "status", "COMPLETED")
    )
    assert taskhub_api_actor.asks_for(
        TaskFieldEqualsViaApi(create_task.task_id, "priority", "MEDIUM")
    )


def test_api_delete_task(taskhub_api_actor: Actor) -> None:
    """Verify deleting a task via API returns 200 and a subsequent fetch returns 404."""
    create_task = CreateTaskViaApi.with_payload({"title": "API delete target"})
    taskhub_api_actor.attempts_to(
        LoginToTaskHubApi.with_credentials("admin", "admin123"),
        create_task,
    )
    assert create_task.task_id is not None

    delete_task = DeleteTaskViaApi.for_task(create_task.task_id)
    taskhub_api_actor.attempts_to(delete_task)
    assert delete_task.result.status_code == 200
    assert isinstance(delete_task.result.payload, dict)
    assert delete_task.result.payload["message"] == "Task deleted."

    task_response = taskhub_api_actor.asks_for(FetchTaskViaApi.by_id(create_task.task_id))
    assert task_response.status_code == 404


def test_api_unauthorized_requests(taskhub_api_actor: Actor) -> None:
    """Verify read and write API endpoints return 401 when called without a session."""
    get_tasks_response = taskhub_api_actor.asks_for(FetchTasksViaApi.all())
    assert get_tasks_response.status_code == 401
    assert isinstance(get_tasks_response.payload, dict)
    assert get_tasks_response.payload["error"] == "Unauthorized."

    create_task = CreateTaskViaApi.with_payload({"title": "should not work"})
    taskhub_api_actor.attempts_to(create_task)
    assert create_task.result.status_code == 401
    assert isinstance(create_task.result.payload, dict)
    assert create_task.result.payload["error"] == "Unauthorized."


def test_api_reset_and_seed_are_deterministic(taskhub_api_actor: Actor) -> None:
    """Verify reset and seed endpoints produce identical task snapshots across repeated calls."""
    reset_snapshots = []
    for _ in range(3):
        reset_data = ResetTaskHubDataViaApi()
        taskhub_api_actor.attempts_to(reset_data)
        assert reset_data.result.status_code == 200
        reset_snapshots.append(_current_task_snapshot(taskhub_api_actor))
    assert all(snapshot == reset_snapshots[0] for snapshot in reset_snapshots[1:])

    seed_snapshots = []
    for _ in range(3):
        seed_data = SeedTaskHubDataViaApi()
        taskhub_api_actor.attempts_to(seed_data)
        assert seed_data.result.status_code == 200
        assert isinstance(seed_data.result.payload, dict)
        assert seed_data.result.payload["task_count"] >= 3
        seed_snapshots.append(_current_task_snapshot(taskhub_api_actor))
    assert all(snapshot == seed_snapshots[0] for snapshot in seed_snapshots[1:])

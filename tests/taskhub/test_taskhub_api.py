"""TaskHub API integration tests using the Screenplay `CallTheAPI` ability."""

from __future__ import annotations

import pytest

from screenplay_core.abilities.call_the_api import CallTheAPI
from screenplay_core.core.actor import Actor
from taskhub.automation.api.client import TaskHubApiClient


def _taskhub_api(actor: Actor) -> TaskHubApiClient:
    return TaskHubApiClient(actor.ability_to(CallTheAPI))


def _current_task_snapshot(taskhub_api_actor: Actor) -> list[dict]:
    taskhub_api = _taskhub_api(taskhub_api_actor)
    taskhub_api.post_login("admin", "admin123")
    tasks_response = taskhub_api.get_tasks()
    tasks_response.raise_for_status()
    return [
        {
            "id": item["id"],
            "title": item["title"],
            "description": item["description"],
            "status": item["status"],
            "priority": item["priority"],
            "due_date": item["due_date"],
        }
        for item in tasks_response.json()["items"]
    ]


@pytest.mark.integration
def test_api_login(taskhub_api_actor: Actor) -> None:
    taskhub_api = _taskhub_api(taskhub_api_actor)
    login_response = taskhub_api.post_login("admin", "admin123")
    assert login_response.status_code == 200
    assert login_response.json()["username"] == "admin"

    me_response = taskhub_api.get_me()
    assert me_response.status_code == 200
    assert me_response.json()["username"] == "admin"


@pytest.mark.integration
def test_api_get_tasks(taskhub_api_actor: Actor) -> None:
    taskhub_api = _taskhub_api(taskhub_api_actor)
    taskhub_api.post_login("admin", "admin123")
    tasks_response = taskhub_api.get_tasks()
    assert tasks_response.status_code == 200

    payload = tasks_response.json()
    assert "items" in payload
    assert len(payload["items"]) >= 3


@pytest.mark.integration
def test_api_create_task(taskhub_api_actor: Actor) -> None:
    taskhub_api = _taskhub_api(taskhub_api_actor)
    taskhub_api.post_login("admin", "admin123")
    create_response = taskhub_api.create_task(
        {
            "title": "API create task",
            "description": "Created through API test",
            "priority": "HIGH",
            "due_date": "2030-04-01",
        }
    )
    assert create_response.status_code == 201
    payload = create_response.json()
    assert payload["title"] == "API create task"
    assert payload["status"] == "ACTIVE"


@pytest.mark.integration
def test_api_update_task(taskhub_api_actor: Actor) -> None:
    taskhub_api = _taskhub_api(taskhub_api_actor)
    taskhub_api.post_login("admin", "admin123")
    create_response = taskhub_api.create_task({"title": "API update target", "priority": "LOW"})
    task_id = create_response.json()["id"]

    update_response = taskhub_api.update_task(
        task_id,
        {
            "title": "API updated task",
            "description": "Updated via API",
            "priority": "MEDIUM",
            "status": "COMPLETED",
        },
    )
    assert update_response.status_code == 200
    payload = update_response.json()
    assert payload["title"] == "API updated task"
    assert payload["status"] == "COMPLETED"
    assert payload["priority"] == "MEDIUM"


@pytest.mark.integration
def test_api_delete_task(taskhub_api_actor: Actor) -> None:
    taskhub_api = _taskhub_api(taskhub_api_actor)
    taskhub_api.post_login("admin", "admin123")
    create_response = taskhub_api.create_task({"title": "API delete target"})
    task_id = create_response.json()["id"]

    delete_response = taskhub_api.delete_task(task_id)
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Task deleted."

    get_response = taskhub_api.get_task(task_id)
    assert get_response.status_code == 404


@pytest.mark.integration
def test_api_unauthorized_requests(taskhub_api_actor: Actor) -> None:
    taskhub_api = _taskhub_api(taskhub_api_actor)
    get_tasks_response = taskhub_api.get_tasks()
    assert get_tasks_response.status_code == 401
    assert get_tasks_response.json()["error"] == "Unauthorized."

    create_response = taskhub_api.create_task({"title": "should not work"})
    assert create_response.status_code == 401
    assert create_response.json()["error"] == "Unauthorized."


@pytest.mark.integration
def test_api_reset_and_seed_are_deterministic(taskhub_api_actor: Actor) -> None:
    taskhub_api = _taskhub_api(taskhub_api_actor)
    reset_snapshots = []
    for _ in range(3):
        reset_response = taskhub_api.reset_test_data()
        assert reset_response.status_code == 200
        reset_snapshots.append(_current_task_snapshot(taskhub_api_actor))
    assert all(snapshot == reset_snapshots[0] for snapshot in reset_snapshots[1:])

    seed_snapshots = []
    for _ in range(3):
        seed_response = taskhub_api.seed_test_data()
        assert seed_response.status_code == 200
        assert seed_response.json()["task_count"] >= 3
        seed_snapshots.append(_current_task_snapshot(taskhub_api_actor))
    assert all(snapshot == seed_snapshots[0] for snapshot in seed_snapshots[1:])

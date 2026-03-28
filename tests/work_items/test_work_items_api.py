"""Work Items API integration tests using Screenplay tasks and questions."""

from __future__ import annotations

import pytest

from examples.work_items.automation.questions.api_questions import (
    CurrentUserViaApi,
    FetchWorkItemsViaApi,
    FetchWorkItemViaApi,
    WorkItemExistsViaApi,
    WorkItemFieldEqualsViaApi,
)
from examples.work_items.automation.tasks.api_tasks import (
    CreateWorkItemViaApi,
    DeleteWorkItemViaApi,
    LoginToWorkItemsApi,
    ResetWorkItemsDataViaApi,
    SeedWorkItemsDataViaApi,
    UpdateWorkItemViaApi,
)
from screenplay_core.core.actor import Actor

pytestmark = [pytest.mark.api, pytest.mark.integration]


def _work_items_from_payload(payload: object) -> list[dict]:
    if not isinstance(payload, dict):
        return []

    work_items = payload.get("work_items")
    if not isinstance(work_items, list):
        return []

    return [work_item for work_item in work_items if isinstance(work_item, dict)]


def _current_work_item_snapshot(work_items_api_actor: Actor) -> list[dict]:
    work_items_api_actor.attempts_to(LoginToWorkItemsApi.with_credentials("admin", "admin123"))
    work_items_response = work_items_api_actor.asks_for(FetchWorkItemsViaApi.all())
    assert work_items_response.status_code == 200

    return [
        {
            "id": work_item.get("id"),
            "title": work_item.get("title"),
            "description": work_item.get("description"),
            "status": work_item.get("status"),
            "priority": work_item.get("priority"),
            "due_date": work_item.get("due_date"),
        }
        for work_item in _work_items_from_payload(work_items_response.payload)
    ]


def test_api_login(work_items_api_actor: Actor) -> None:
    """Verify API login returns a 200 with the authenticated user's profile."""
    login = LoginToWorkItemsApi.with_credentials("admin", "admin123")
    work_items_api_actor.attempts_to(login)
    assert login.result.status_code == 200
    assert isinstance(login.result.payload, dict)
    assert login.result.payload["username"] == "admin"

    me_response = work_items_api_actor.asks_for(CurrentUserViaApi())
    assert me_response.status_code == 200
    assert isinstance(me_response.payload, dict)
    assert me_response.payload["username"] == "admin"


def test_api_get_work_items(work_items_api_actor: Actor) -> None:
    """Verify the list endpoint returns the seeded work item list after login."""
    work_items_api_actor.attempts_to(LoginToWorkItemsApi.with_credentials("admin", "admin123"))
    work_items_response = work_items_api_actor.asks_for(FetchWorkItemsViaApi.all())
    assert work_items_response.status_code == 200
    assert len(_work_items_from_payload(work_items_response.payload)) >= 3


def test_api_create_work_item(work_items_api_actor: Actor) -> None:
    """Verify creating a work item via API returns 201 and the record is retrievable."""
    create_work_item = CreateWorkItemViaApi.with_payload(
        {
            "title": "API create work item",
            "description": "Created through API test",
            "priority": "HIGH",
            "due_date": "2030-04-01",
        }
    )
    work_items_api_actor.attempts_to(
        LoginToWorkItemsApi.with_credentials("admin", "admin123"),
        create_work_item,
    )

    assert create_work_item.result.status_code == 201
    assert isinstance(create_work_item.result.payload, dict)
    assert create_work_item.result.payload["title"] == "API create work item"
    assert create_work_item.result.payload["status"] == "ACTIVE"
    assert create_work_item.work_item_id is not None
    assert work_items_api_actor.asks_for(WorkItemExistsViaApi(create_work_item.work_item_id))
    assert work_items_api_actor.asks_for(
        WorkItemFieldEqualsViaApi(
            create_work_item.work_item_id,
            "description",
            "Created through API test",
        )
    )


def test_api_update_work_item(work_items_api_actor: Actor) -> None:
    """Verify updating a work item via API persists the new fields."""
    create_work_item = CreateWorkItemViaApi.with_payload(
        {"title": "API update target", "priority": "LOW"}
    )
    work_items_api_actor.attempts_to(
        LoginToWorkItemsApi.with_credentials("admin", "admin123"),
        create_work_item,
    )
    assert create_work_item.work_item_id is not None

    update_work_item = UpdateWorkItemViaApi.for_work_item(
        create_work_item.work_item_id,
        {
            "title": "API updated work item",
            "description": "Updated via API",
            "priority": "MEDIUM",
            "status": "COMPLETED",
        },
    )
    work_items_api_actor.attempts_to(update_work_item)

    assert update_work_item.result.status_code == 200
    assert work_items_api_actor.asks_for(
        WorkItemFieldEqualsViaApi(
            create_work_item.work_item_id,
            "title",
            "API updated work item",
        )
    )
    assert work_items_api_actor.asks_for(
        WorkItemFieldEqualsViaApi(create_work_item.work_item_id, "status", "COMPLETED")
    )
    assert work_items_api_actor.asks_for(
        WorkItemFieldEqualsViaApi(create_work_item.work_item_id, "priority", "MEDIUM")
    )


def test_api_delete_work_item(work_items_api_actor: Actor) -> None:
    """Verify deleting a work item returns 204 and a subsequent fetch returns 404."""
    create_work_item = CreateWorkItemViaApi.with_payload({"title": "API delete target"})
    work_items_api_actor.attempts_to(
        LoginToWorkItemsApi.with_credentials("admin", "admin123"),
        create_work_item,
    )
    assert create_work_item.work_item_id is not None

    delete_work_item = DeleteWorkItemViaApi.for_work_item(create_work_item.work_item_id)
    work_items_api_actor.attempts_to(delete_work_item)
    assert delete_work_item.result.status_code == 204
    assert delete_work_item.result.payload is None

    work_item_response = work_items_api_actor.asks_for(
        FetchWorkItemViaApi.by_id(create_work_item.work_item_id)
    )
    assert work_item_response.status_code == 404


def test_api_unauthorized_requests(work_items_api_actor: Actor) -> None:
    """Verify read and write API endpoints return 401 when called without a session."""
    work_items_response = work_items_api_actor.asks_for(FetchWorkItemsViaApi.all())
    assert work_items_response.status_code == 401
    assert isinstance(work_items_response.payload, dict)
    assert work_items_response.payload["error"] == "Unauthorized."

    create_work_item = CreateWorkItemViaApi.with_payload({"title": "should not work"})
    work_items_api_actor.attempts_to(create_work_item)
    assert create_work_item.result.status_code == 401
    assert isinstance(create_work_item.result.payload, dict)
    assert create_work_item.result.payload["error"] == "Unauthorized."


def test_api_reset_and_seed_are_deterministic(work_items_api_actor: Actor) -> None:
    """Verify reset and seed endpoints produce identical work item snapshots."""
    reset_snapshots = []
    for _ in range(3):
        reset_work_items_data = ResetWorkItemsDataViaApi()
        work_items_api_actor.attempts_to(reset_work_items_data)
        assert reset_work_items_data.result.status_code == 200
        reset_snapshots.append(_current_work_item_snapshot(work_items_api_actor))
    assert all(snapshot == reset_snapshots[0] for snapshot in reset_snapshots[1:])

    seed_snapshots = []
    for _ in range(3):
        seed_work_items_data = SeedWorkItemsDataViaApi()
        work_items_api_actor.attempts_to(seed_work_items_data)
        assert seed_work_items_data.result.status_code == 200
        assert isinstance(seed_work_items_data.result.payload, dict)
        assert seed_work_items_data.result.payload["work_item_count"] >= 3
        seed_snapshots.append(_current_work_item_snapshot(work_items_api_actor))
    assert all(snapshot == seed_snapshots[0] for snapshot in seed_snapshots[1:])

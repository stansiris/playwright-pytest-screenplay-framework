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
from screenplay_core.http.call_the_api import CallTheApi

pytestmark = [pytest.mark.api, pytest.mark.integration]


def _last_response(actor: Actor):
    response = actor.ability_to(CallTheApi).last_response
    assert response is not None
    return response


def _json_or_none(response):
    try:
        return response.json()
    except ValueError:
        return None


def _last_payload_dict(actor: Actor) -> dict:
    payload = _json_or_none(_last_response(actor))
    assert isinstance(payload, dict)
    return payload


def _last_work_item_id(actor: Actor) -> int | None:
    payload = _json_or_none(_last_response(actor))
    if not isinstance(payload, dict):
        return None

    work_item_id = payload.get("id")
    try:
        return int(work_item_id)
    except (TypeError, ValueError):
        return None


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
    work_items_api_actor.attempts_to(LoginToWorkItemsApi.with_credentials("admin", "admin123"))
    assert _last_response(work_items_api_actor).status_code == 200
    assert _last_payload_dict(work_items_api_actor)["username"] == "admin"

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
    work_items_api_actor.attempts_to(
        LoginToWorkItemsApi.with_credentials("admin", "admin123"),
        CreateWorkItemViaApi.with_payload(
            {
                "title": "API create work item",
                "description": "Created through API test",
                "priority": "HIGH",
                "due_date": "2030-04-01",
            }
        ),
    )

    assert _last_response(work_items_api_actor).status_code == 201
    payload = _last_payload_dict(work_items_api_actor)
    assert payload["title"] == "API create work item"
    assert payload["status"] == "ACTIVE"

    work_item_id = _last_work_item_id(work_items_api_actor)
    assert work_item_id is not None
    assert work_items_api_actor.asks_for(WorkItemExistsViaApi(work_item_id))
    assert work_items_api_actor.asks_for(
        WorkItemFieldEqualsViaApi(
            work_item_id,
            "description",
            "Created through API test",
        )
    )


def test_api_update_work_item(work_items_api_actor: Actor) -> None:
    """Verify updating a work item via API persists the new fields."""
    work_items_api_actor.attempts_to(
        LoginToWorkItemsApi.with_credentials("admin", "admin123"),
        CreateWorkItemViaApi.with_payload({"title": "API update target", "priority": "LOW"}),
    )
    work_item_id = _last_work_item_id(work_items_api_actor)
    assert work_item_id is not None

    work_items_api_actor.attempts_to(
        UpdateWorkItemViaApi.for_work_item(
            work_item_id,
            {
                "title": "API updated work item",
                "description": "Updated via API",
                "priority": "MEDIUM",
                "status": "COMPLETED",
            },
        )
    )

    assert _last_response(work_items_api_actor).status_code == 200
    assert work_items_api_actor.asks_for(
        WorkItemFieldEqualsViaApi(
            work_item_id,
            "title",
            "API updated work item",
        )
    )
    assert work_items_api_actor.asks_for(
        WorkItemFieldEqualsViaApi(work_item_id, "status", "COMPLETED")
    )
    assert work_items_api_actor.asks_for(
        WorkItemFieldEqualsViaApi(work_item_id, "priority", "MEDIUM")
    )


def test_api_delete_work_item(work_items_api_actor: Actor) -> None:
    """Verify deleting a work item returns 204 and a subsequent fetch returns 404."""
    work_items_api_actor.attempts_to(
        LoginToWorkItemsApi.with_credentials("admin", "admin123"),
        CreateWorkItemViaApi.with_payload({"title": "API delete target"}),
    )
    work_item_id = _last_work_item_id(work_items_api_actor)
    assert work_item_id is not None

    work_items_api_actor.attempts_to(DeleteWorkItemViaApi.for_work_item(work_item_id))
    assert _last_response(work_items_api_actor).status_code == 204
    assert _json_or_none(_last_response(work_items_api_actor)) is None

    work_item_response = work_items_api_actor.asks_for(FetchWorkItemViaApi.by_id(work_item_id))
    assert work_item_response.status_code == 404


def test_api_unauthorized_requests(work_items_api_actor: Actor) -> None:
    """Verify read and write API endpoints return 401 when called without a session."""
    work_items_response = work_items_api_actor.asks_for(FetchWorkItemsViaApi.all())
    assert work_items_response.status_code == 401
    assert isinstance(work_items_response.payload, dict)
    assert work_items_response.payload["error"] == "Unauthorized."

    work_items_api_actor.attempts_to(
        CreateWorkItemViaApi.with_payload({"title": "should not work"})
    )
    assert _last_response(work_items_api_actor).status_code == 401
    assert _last_payload_dict(work_items_api_actor)["error"] == "Unauthorized."


def test_api_reset_and_seed_are_deterministic(work_items_api_actor: Actor) -> None:
    """Verify reset and seed endpoints produce identical work item snapshots."""
    reset_snapshots = []
    for _ in range(3):
        work_items_api_actor.attempts_to(ResetWorkItemsDataViaApi())
        assert _last_response(work_items_api_actor).status_code == 200
        reset_snapshots.append(_current_work_item_snapshot(work_items_api_actor))
    assert all(snapshot == reset_snapshots[0] for snapshot in reset_snapshots[1:])

    seed_snapshots = []
    for _ in range(3):
        work_items_api_actor.attempts_to(SeedWorkItemsDataViaApi())
        assert _last_response(work_items_api_actor).status_code == 200
        assert _last_payload_dict(work_items_api_actor)["work_item_count"] >= 3
        seed_snapshots.append(_current_work_item_snapshot(work_items_api_actor))
    assert all(snapshot == seed_snapshots[0] for snapshot in seed_snapshots[1:])

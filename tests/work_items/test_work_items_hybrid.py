"""Work Items hybrid integration tests that cross UI and API boundaries."""

from __future__ import annotations

import pytest

from examples.work_items.automation.questions.api_questions import (
    WorkItemExistsViaApi,
    WorkItemFieldEqualsViaApi,
    WorkItemIdForTitleViaApi,
)
from examples.work_items.automation.tasks.api_tasks import (
    CreateWorkItemViaApi,
    LoginToWorkItemsApi,
)
from examples.work_items.automation.tasks.create_work_item import CreateWorkItem
from examples.work_items.automation.tasks.login import LoginToWorkItems
from examples.work_items.automation.tasks.open_work_items import OpenWorkItems
from examples.work_items.automation.ui.targets import WorkItemsTargets
from screenplay_core.http.call_the_api import CallTheApi
from screenplay_core.playwright.ensure import Ensure

pytestmark = [pytest.mark.hybrid, pytest.mark.integration]


def _last_response(actor):
    response = actor.ability_to(CallTheApi).last_response
    assert response is not None
    return response


def _last_work_item_id(actor) -> int | None:
    payload = _last_response(actor).json()
    if not isinstance(payload, dict):
        return None

    work_item_id = payload.get("id")
    try:
        return int(work_item_id)
    except (TypeError, ValueError):
        return None


def test_create_work_item_via_api_verify_in_ui(
    work_items_api_actor,
    work_items_customer,
) -> None:
    title = "Hybrid API to UI work item"
    work_items_api_actor.attempts_to(
        LoginToWorkItemsApi.with_credentials("admin", "admin123"),
        CreateWorkItemViaApi.with_payload(
            {
                "title": title,
                "description": "Created through API then validated in UI",
                "priority": "HIGH",
            }
        ),
    )
    assert _last_response(work_items_api_actor).status_code == 201
    work_item_id = _last_work_item_id(work_items_api_actor)
    assert work_item_id is not None

    work_items_customer.attempts_to(
        OpenWorkItems.app(),
        LoginToWorkItems.with_credentials("admin", "admin123"),
        Ensure.that(WorkItemsTargets.work_item_for_id(work_item_id)).to_be_visible(),
        Ensure.that(WorkItemsTargets.work_item_title_text_for_id(work_item_id)).to_have_text(title),
    )


def test_create_work_item_via_ui_verify_in_api(
    work_items_logged_in_customer,
    work_items_api_actor,
) -> None:
    title = "Hybrid UI to API work item"
    work_items_logged_in_customer.attempts_to(
        CreateWorkItem.named(
            title=title,
            description="Created through UI then validated in API",
            priority="MEDIUM",
            due_date="2030-05-01",
        ),
    )

    work_items_api_actor.attempts_to(LoginToWorkItemsApi.with_credentials("admin", "admin123"))
    work_item_id = work_items_api_actor.asks_for(WorkItemIdForTitleViaApi(title))
    assert work_item_id is not None
    work_items_logged_in_customer.attempts_to(
        Ensure.that(WorkItemsTargets.work_item_for_id(work_item_id)).to_be_visible(),
    )

    assert work_items_api_actor.asks_for(WorkItemExistsViaApi(work_item_id))
    assert work_items_api_actor.asks_for(WorkItemFieldEqualsViaApi(work_item_id, "title", title))

"""Work Items UI integration tests expressed with Screenplay tasks and questions."""

import pytest

from examples.work_items.automation.questions.on_work_items_page import OnWorkItemsPage
from examples.work_items.automation.questions.work_item_completed import WorkItemCompleted
from examples.work_items.automation.questions.work_item_id_for_title import WorkItemIdForTitle
from examples.work_items.automation.tasks.create_work_item import CreateWorkItem
from examples.work_items.automation.tasks.delete_work_item import DeleteWorkItem
from examples.work_items.automation.tasks.edit_work_item import EditWorkItem
from examples.work_items.automation.tasks.filter_work_items import FilterWorkItems
from examples.work_items.automation.tasks.login import LoginToWorkItems
from examples.work_items.automation.tasks.open_work_items import OpenWorkItems
from examples.work_items.automation.tasks.toggle_work_item_completion import (
    ToggleWorkItemCompletion,
)
from examples.work_items.automation.ui.targets import WorkItemsTargets
from screenplay_core.playwright.ensure import Ensure

pytestmark = [pytest.mark.ui, pytest.mark.integration]


def test_successful_login(work_items_customer) -> None:
    """Verify valid credentials navigate the user to the work item list."""
    work_items_customer.attempts_to(
        OpenWorkItems.app(),
        Ensure.that(WorkItemsTargets.LOGIN_SUBMIT_BUTTON).to_be_visible(),
        LoginToWorkItems.with_credentials("admin", "admin123"),
        Ensure.that(WorkItemsTargets.WORK_ITEM_LIST_CONTAINER).to_be_visible(),
    )
    assert work_items_customer.asks_for(OnWorkItemsPage())


def test_failed_login(work_items_customer) -> None:
    """Verify invalid credentials display an error message on the login page."""
    work_items_customer.attempts_to(
        OpenWorkItems.app(),
        Ensure.that(WorkItemsTargets.LOGIN_SUBMIT_BUTTON).to_be_visible(),
        LoginToWorkItems.with_credentials("admin", "wrong-password"),
        Ensure.that(WorkItemsTargets.LOGIN_ERROR_MESSAGE).to_be_visible(),
        Ensure.that(WorkItemsTargets.LOGIN_ERROR_MESSAGE).to_contain_text(
            "Invalid username or password."
        ),
    )


def test_create_work_item(work_items_logged_in_customer) -> None:
    """Verify a newly created work item appears in the list with a stable id."""
    new_title = "UI create work item"
    work_items_logged_in_customer.attempts_to(
        CreateWorkItem.named(
            title=new_title,
            description="Created from UI test",
            priority="HIGH",
            due_date="2030-02-01",
        ),
    )

    work_item_id = work_items_logged_in_customer.asks_for(WorkItemIdForTitle(new_title))
    assert work_item_id is not None
    work_items_logged_in_customer.attempts_to(
        Ensure.that(WorkItemsTargets.work_item_for_id(work_item_id)).to_be_visible(),
    )


def test_edit_work_item(work_items_logged_in_customer) -> None:
    """Verify editing a work item updates its fields in the list."""
    original_title = "UI edit work item original"
    updated_title = "UI edit work item updated"
    work_items_logged_in_customer.attempts_to(
        CreateWorkItem.named(title=original_title, description="Original", priority="LOW"),
    )

    work_item_id = work_items_logged_in_customer.asks_for(WorkItemIdForTitle(original_title))
    assert work_item_id is not None

    work_items_logged_in_customer.attempts_to(
        EditWorkItem.for_work_item_id(
            work_item_id=work_item_id,
            new_title=updated_title,
            new_description="Updated description",
            new_priority="HIGH",
            new_due_date="2030-03-01",
        ),
        Ensure.that(WorkItemsTargets.work_item_for_id(work_item_id)).to_be_visible(),
        Ensure.that(WorkItemsTargets.work_item_title_text_for_id(work_item_id)).to_have_text(
            updated_title
        ),
    )


def test_complete_work_item(work_items_logged_in_customer) -> None:
    """Verify toggling completion marks the work item as completed."""
    title = "UI complete work item"
    work_items_logged_in_customer.attempts_to(
        CreateWorkItem.named(title=title, description="Needs completion"),
    )

    work_item_id = work_items_logged_in_customer.asks_for(WorkItemIdForTitle(title))
    assert work_item_id is not None
    work_items_logged_in_customer.attempts_to(
        ToggleWorkItemCompletion.for_work_item_id(work_item_id)
    )
    assert work_items_logged_in_customer.asks_for(WorkItemCompleted.for_work_item_id(work_item_id))


def test_delete_work_item(work_items_logged_in_customer) -> None:
    """Verify deleting a work item removes it from the list."""
    title = "UI delete work item"
    work_items_logged_in_customer.attempts_to(
        CreateWorkItem.named(title=title),
    )

    work_item_id = work_items_logged_in_customer.asks_for(WorkItemIdForTitle(title))
    assert work_item_id is not None
    work_items_logged_in_customer.attempts_to(
        DeleteWorkItem.with_id(work_item_id),
        Ensure.that(WorkItemsTargets.work_item_for_id(work_item_id)).to_have_count(0),
    )


def test_filter_completed_work_items(work_items_logged_in_customer) -> None:
    """Verify the completed filter shows only completed work items and hides active ones."""
    active_title = "UI active work item for filtering"
    completed_title = "UI completed work item for filtering"

    work_items_logged_in_customer.attempts_to(
        CreateWorkItem.named(title=active_title),
        CreateWorkItem.named(title=completed_title),
    )

    active_work_item_id = work_items_logged_in_customer.asks_for(WorkItemIdForTitle(active_title))
    completed_work_item_id = work_items_logged_in_customer.asks_for(
        WorkItemIdForTitle(completed_title)
    )
    assert active_work_item_id is not None
    assert completed_work_item_id is not None

    work_items_logged_in_customer.attempts_to(
        Ensure.that(WorkItemsTargets.work_item_for_id(active_work_item_id)).to_be_visible(),
        Ensure.that(WorkItemsTargets.work_item_for_id(completed_work_item_id)).to_be_visible(),
        ToggleWorkItemCompletion.for_work_item_id(completed_work_item_id),
        FilterWorkItems.by("completed"),
        Ensure.that(WorkItemsTargets.work_item_for_id(completed_work_item_id)).to_be_visible(),
        Ensure.that(WorkItemsTargets.work_item_for_id(active_work_item_id)).to_have_count(0),
    )


def test_empty_title_validation_error(work_items_logged_in_customer) -> None:
    """Verify submitting a work item with an empty title shows a validation error."""
    work_items_logged_in_customer.attempts_to(
        CreateWorkItem.named(title="", description="Missing title should fail"),
        Ensure.that(WorkItemsTargets.FLASH_MESSAGE_CONTAINER).to_contain_text("Title is required."),
    )

"""Work Items BDD scenarios using pytest-bdd and Screenplay tasks."""

from pytest_bdd import given, parsers, scenario, then, when

from examples.work_items.automation.questions.on_work_items_page import OnWorkItemsPage
from examples.work_items.automation.questions.work_item_id_for_title import WorkItemIdForTitle
from examples.work_items.automation.tasks.create_work_item import CreateWorkItem
from examples.work_items.automation.tasks.delete_work_item import DeleteWorkItem
from examples.work_items.automation.tasks.filter_work_items import FilterWorkItems
from examples.work_items.automation.tasks.login import LoginToWorkItems
from examples.work_items.automation.tasks.open_work_items import OpenWorkItems
from examples.work_items.automation.tasks.toggle_work_item_completion import (
    ToggleWorkItemCompletion,
)
from examples.work_items.automation.ui.targets import WorkItemsTargets
from screenplay_core.core.actor import Actor
from screenplay_core.playwright.ensure import Ensure


@scenario("features/work_item_management.feature", "Successful login reaches the work items page")
def test_successful_login_reaches_work_items_page() -> None:
    """Verify that valid credentials navigate the user to the Work Items page."""
    pass


@scenario(
    "features/work_item_management.feature", "Create a work item and verify it appears in the list"
)
def test_create_work_item_appears_in_list() -> None:
    """Verify that a newly created work item is immediately visible in the list."""
    pass


@scenario(
    "features/work_item_management.feature",
    "Complete a work item and filter to see only completed items",
)
def test_complete_work_item_visible_under_completed_filter() -> None:
    """Verify that completing a work item and applying the completed filter shows it correctly."""
    pass


@scenario("features/work_item_management.feature", "Delete a work item and verify it is removed")
def test_delete_work_item_removes_it_from_list() -> None:
    """Verify that deleting a work item removes it from the list entirely."""
    pass


@given("I open the Work Items application")
def open_work_items_application(work_items_customer: Actor) -> None:
    work_items_customer.attempts_to(
        OpenWorkItems.app(),
        Ensure.that(WorkItemsTargets.LOGIN_SUBMIT_BUTTON).to_be_visible(),
    )


@given("I am logged in to Work Items")
def i_am_logged_in_to_work_items(work_items_logged_in_customer: Actor) -> None:
    work_items_logged_in_customer.attempts_to(
        Ensure.that(WorkItemsTargets.WORK_ITEM_LIST_CONTAINER).to_be_visible(),
    )


@when(parsers.parse('I log in to Work Items with username "{username}" and password "{password}"'))
def log_in_to_work_items(work_items_customer: Actor, username: str, password: str) -> None:
    work_items_customer.attempts_to(LoginToWorkItems.with_credentials(username, password))


@when(parsers.parse('I create a work item titled "{title}" with priority "{priority}"'))
def create_work_item(work_items_logged_in_customer: Actor, title: str, priority: str) -> None:
    work_items_logged_in_customer.attempts_to(CreateWorkItem.named(title=title, priority=priority))


@when(parsers.parse('I mark the work item titled "{title}" as complete'))
def mark_work_item_complete(work_items_logged_in_customer: Actor, title: str) -> None:
    work_item_id = work_items_logged_in_customer.asks_for(WorkItemIdForTitle(title))
    assert work_item_id is not None, f"Work item '{title}' not found; cannot mark as complete"
    work_items_logged_in_customer.attempts_to(
        ToggleWorkItemCompletion.for_work_item_id(work_item_id)
    )


@when(parsers.parse('I filter work items by "{filter_name}"'))
def filter_work_items(work_items_logged_in_customer: Actor, filter_name: str) -> None:
    work_items_logged_in_customer.attempts_to(FilterWorkItems.by(filter_name))


@when(parsers.parse('I delete the work item titled "{title}"'))
def delete_work_item(work_items_logged_in_customer: Actor, title: str) -> None:
    work_item_id = work_items_logged_in_customer.asks_for(WorkItemIdForTitle(title))
    assert work_item_id is not None, f"Work item '{title}' not found; cannot delete"
    work_items_logged_in_customer.attempts_to(DeleteWorkItem.with_id(work_item_id))


@then("I should be on the Work Items page")
def should_be_on_work_items_page(work_items_customer: Actor) -> None:
    work_items_customer.attempts_to(
        Ensure.that(WorkItemsTargets.WORK_ITEM_LIST_CONTAINER).to_be_visible()
    )
    assert work_items_customer.asks_for(OnWorkItemsPage())


@then(parsers.parse('the work item titled "{title}" should be visible'))
def work_item_should_be_visible(work_items_logged_in_customer: Actor, title: str) -> None:
    work_item_id = work_items_logged_in_customer.asks_for(WorkItemIdForTitle(title))
    assert work_item_id is not None, f"Work item '{title}' not found in the list"
    work_items_logged_in_customer.attempts_to(
        Ensure.that(WorkItemsTargets.work_item_for_id(work_item_id)).to_be_visible(),
    )


@then(parsers.parse('the work item titled "{title}" should not be visible'))
def work_item_should_not_be_visible(work_items_logged_in_customer: Actor, title: str) -> None:
    work_item_id = work_items_logged_in_customer.asks_for(WorkItemIdForTitle(title))
    assert work_item_id is None, f"Work item '{title}' was found but should have been deleted"

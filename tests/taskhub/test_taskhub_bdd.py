"""TaskHub BDD scenarios using pytest-bdd and Screenplay tasks."""

from pytest_bdd import given, parsers, scenario, then, when

from examples.taskhub.automation.questions.on_tasks_page import OnTaskHubTasksPage
from examples.taskhub.automation.questions.task_id_for_title import TaskIdForTitle
from examples.taskhub.automation.tasks.create_task import CreateTask
from examples.taskhub.automation.tasks.delete_task import DeleteTask
from examples.taskhub.automation.tasks.filter_tasks import FilterTasks
from examples.taskhub.automation.tasks.login import LoginToTaskHub
from examples.taskhub.automation.tasks.open_taskhub import OpenTaskHub
from examples.taskhub.automation.tasks.toggle_task_completion import ToggleTaskCompletion
from examples.taskhub.automation.ui.targets import TaskHubTargets
from screenplay_core.playwright.ensure import Ensure
from screenplay_core.core.actor import Actor


@scenario("features/task_management.feature", "Successful login reaches the task list")
def test_successful_login_reaches_task_list() -> None:
    """Verify that valid credentials navigate the user to the task list."""
    pass


@scenario("features/task_management.feature", "Create a task and verify it appears in the list")
def test_create_task_appears_in_list() -> None:
    """Verify that a newly created task is immediately visible in the task list."""
    pass


@scenario(
    "features/task_management.feature",
    "Complete a task and filter to see only completed tasks",
)
def test_complete_task_visible_under_completed_filter() -> None:
    """Verify that completing a task and applying the completed filter shows it correctly."""
    pass


@scenario("features/task_management.feature", "Delete a task and verify it is removed")
def test_delete_task_removes_it_from_list() -> None:
    """Verify that deleting a task removes it from the task list entirely."""
    pass


# ---------------------------------------------------------------------------
# Given steps
# ---------------------------------------------------------------------------


@given("I open the TaskHub application")
def open_taskhub_application(taskhub_customer: Actor) -> None:
    taskhub_customer.attempts_to(
        OpenTaskHub.app(),
        Ensure.that(TaskHubTargets.LOGIN_SUBMIT_BUTTON).to_be_visible(),
    )


@given("I am logged in to TaskHub")
def i_am_logged_in_to_taskhub(taskhub_logged_in_customer: Actor) -> None:
    taskhub_logged_in_customer.attempts_to(
        Ensure.that(TaskHubTargets.TASK_LIST_CONTAINER).to_be_visible(),
    )


# ---------------------------------------------------------------------------
# When steps
# ---------------------------------------------------------------------------


@when(parsers.parse('I log in to TaskHub with username "{username}" and password "{password}"'))
def log_in_to_taskhub(taskhub_customer: Actor, username: str, password: str) -> None:
    taskhub_customer.attempts_to(LoginToTaskHub.with_credentials(username, password))


@when(parsers.parse('I create a TaskHub task titled "{title}" with priority "{priority}"'))
def create_taskhub_task(taskhub_logged_in_customer: Actor, title: str, priority: str) -> None:
    taskhub_logged_in_customer.attempts_to(CreateTask.named(title=title, priority=priority))


@when(parsers.parse('I mark the TaskHub task titled "{title}" as complete'))
def mark_taskhub_task_complete(taskhub_logged_in_customer: Actor, title: str) -> None:
    task_id = taskhub_logged_in_customer.asks_for(TaskIdForTitle(title))
    assert task_id is not None, f"Task '{title}' not found — cannot mark as complete"
    taskhub_logged_in_customer.attempts_to(ToggleTaskCompletion.for_task_id(task_id))


@when(parsers.parse('I filter the TaskHub task list by "{filter_name}"'))
def filter_taskhub_tasks(taskhub_logged_in_customer: Actor, filter_name: str) -> None:
    taskhub_logged_in_customer.attempts_to(FilterTasks.by(filter_name))


@when(parsers.parse('I delete the TaskHub task titled "{title}"'))
def delete_taskhub_task(taskhub_logged_in_customer: Actor, title: str) -> None:
    task_id = taskhub_logged_in_customer.asks_for(TaskIdForTitle(title))
    assert task_id is not None, f"Task '{title}' not found — cannot delete"
    taskhub_logged_in_customer.attempts_to(DeleteTask.with_id(task_id))


# ---------------------------------------------------------------------------
# Then steps
# ---------------------------------------------------------------------------


@then("I should be on the TaskHub task list")
def should_be_on_taskhub_task_list(taskhub_customer: Actor) -> None:
    taskhub_customer.attempts_to(Ensure.that(TaskHubTargets.TASK_LIST_CONTAINER).to_be_visible())
    assert taskhub_customer.asks_for(OnTaskHubTasksPage())


@then(parsers.parse('the TaskHub task titled "{title}" should be visible'))
def taskhub_task_should_be_visible(taskhub_logged_in_customer: Actor, title: str) -> None:
    task_id = taskhub_logged_in_customer.asks_for(TaskIdForTitle(title))
    assert task_id is not None, f"Task '{title}' not found in the task list"
    taskhub_logged_in_customer.attempts_to(
        Ensure.that(TaskHubTargets.task_item_for_id(task_id)).to_be_visible(),
    )


@then(parsers.parse('the TaskHub task titled "{title}" should not be visible'))
def taskhub_task_should_not_be_visible(taskhub_logged_in_customer: Actor, title: str) -> None:
    task_id = taskhub_logged_in_customer.asks_for(TaskIdForTitle(title))
    assert task_id is None, f"Task '{title}' was found but should have been deleted"

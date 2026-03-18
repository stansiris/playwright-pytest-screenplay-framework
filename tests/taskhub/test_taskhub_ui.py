"""TaskHub UI integration tests expressed with Screenplay tasks and questions."""

import pytest

from examples.taskhub.automation.questions.on_tasks_page import OnTaskHubTasksPage
from examples.taskhub.automation.questions.task_completed import TaskCompleted
from examples.taskhub.automation.questions.task_id_for_title import TaskIdForTitle
from examples.taskhub.automation.tasks.create_task import CreateTask
from examples.taskhub.automation.tasks.delete_task import DeleteTask
from examples.taskhub.automation.tasks.edit_task import EditTask
from examples.taskhub.automation.tasks.filter_tasks import FilterTasks
from examples.taskhub.automation.tasks.login import LoginToTaskHub
from examples.taskhub.automation.tasks.open_taskhub import OpenTaskHub
from examples.taskhub.automation.tasks.toggle_task_completion import ToggleTaskCompletion
from examples.taskhub.automation.ui.targets import TaskHubTargets
from screenplay_core.playwright.ensure import Ensure

pytestmark = [pytest.mark.ui, pytest.mark.integration]


def test_successful_login(taskhub_customer) -> None:
    """Verify valid credentials navigate the user to the task list."""
    taskhub_customer.attempts_to(
        OpenTaskHub.app(),
        Ensure.that(TaskHubTargets.LOGIN_SUBMIT_BUTTON).to_be_visible(),
        LoginToTaskHub.with_credentials("admin", "admin123"),
        Ensure.that(TaskHubTargets.TASK_LIST_CONTAINER).to_be_visible(),
    )
    assert taskhub_customer.asks_for(OnTaskHubTasksPage())


def test_failed_login(taskhub_customer) -> None:
    """Verify invalid credentials display an error message on the login page."""
    taskhub_customer.attempts_to(
        OpenTaskHub.app(),
        Ensure.that(TaskHubTargets.LOGIN_SUBMIT_BUTTON).to_be_visible(),
        LoginToTaskHub.with_credentials("admin", "wrong-password"),
        Ensure.that(TaskHubTargets.LOGIN_ERROR_MESSAGE).to_be_visible(),
        Ensure.that(TaskHubTargets.LOGIN_ERROR_MESSAGE).to_contain_text(
            "Invalid username or password."
        ),
    )


def test_create_task(taskhub_logged_in_customer) -> None:
    """Verify a newly created task appears in the task list with a stable task ID."""
    new_title = "UI create task"
    taskhub_logged_in_customer.attempts_to(
        CreateTask.named(
            title=new_title,
            description="Created from UI test",
            priority="HIGH",
            due_date="2030-02-01",
        ),
    )

    task_id = taskhub_logged_in_customer.asks_for(TaskIdForTitle(new_title))
    assert task_id is not None
    taskhub_logged_in_customer.attempts_to(
        Ensure.that(TaskHubTargets.task_item_for_id(task_id)).to_be_visible(),
    )


def test_edit_task(taskhub_logged_in_customer) -> None:
    """Verify editing a task updates its title and other fields in the task list."""
    original_title = "UI edit task original"
    updated_title = "UI edit task updated"
    taskhub_logged_in_customer.attempts_to(
        CreateTask.named(title=original_title, description="Original", priority="LOW"),
    )

    task_id = taskhub_logged_in_customer.asks_for(TaskIdForTitle(original_title))
    assert task_id is not None

    taskhub_logged_in_customer.attempts_to(
        EditTask.for_task_id(
            task_id=task_id,
            new_title=updated_title,
            new_description="Updated description",
            new_priority="HIGH",
            new_due_date="2030-03-01",
        ),
        Ensure.that(TaskHubTargets.task_item_for_id(task_id)).to_be_visible(),
        Ensure.that(TaskHubTargets.task_title_text_for_id(task_id)).to_have_text(updated_title),
    )


def test_complete_task(taskhub_logged_in_customer) -> None:
    """Verify toggling task completion marks the task as completed."""
    title = "UI complete task"
    taskhub_logged_in_customer.attempts_to(
        CreateTask.named(title=title, description="Needs completion"),
    )

    task_id = taskhub_logged_in_customer.asks_for(TaskIdForTitle(title))
    assert task_id is not None
    taskhub_logged_in_customer.attempts_to(ToggleTaskCompletion.for_task_id(task_id))
    assert taskhub_logged_in_customer.asks_for(TaskCompleted.for_task_id(task_id))


def test_delete_task(taskhub_logged_in_customer) -> None:
    """Verify deleting a task removes it from the task list."""
    title = "UI delete task"
    taskhub_logged_in_customer.attempts_to(
        CreateTask.named(title=title),
    )

    task_id = taskhub_logged_in_customer.asks_for(TaskIdForTitle(title))
    assert task_id is not None
    taskhub_logged_in_customer.attempts_to(
        DeleteTask.with_id(task_id),
        Ensure.that(TaskHubTargets.task_item_for_id(task_id)).to_have_count(0),
    )


def test_filter_completed_tasks(taskhub_logged_in_customer) -> None:
    """Verify the completed filter shows only completed tasks and hides active ones."""
    active_title = "UI active task for filtering"
    completed_title = "UI completed task for filtering"

    taskhub_logged_in_customer.attempts_to(
        CreateTask.named(title=active_title),
        CreateTask.named(title=completed_title),
    )

    active_task_id = taskhub_logged_in_customer.asks_for(TaskIdForTitle(active_title))
    completed_task_id = taskhub_logged_in_customer.asks_for(TaskIdForTitle(completed_title))
    assert active_task_id is not None
    assert completed_task_id is not None

    taskhub_logged_in_customer.attempts_to(
        Ensure.that(TaskHubTargets.task_item_for_id(active_task_id)).to_be_visible(),
        Ensure.that(TaskHubTargets.task_item_for_id(completed_task_id)).to_be_visible(),
        ToggleTaskCompletion.for_task_id(completed_task_id),
        FilterTasks.by("completed"),
        Ensure.that(TaskHubTargets.task_item_for_id(completed_task_id)).to_be_visible(),
        Ensure.that(TaskHubTargets.task_item_for_id(active_task_id)).to_have_count(0),
    )


def test_empty_title_validation_error(taskhub_logged_in_customer) -> None:
    """Verify submitting a task with an empty title shows a validation error message."""
    taskhub_logged_in_customer.attempts_to(
        CreateTask.named(title="", description="Missing title should fail"),
        Ensure.that(TaskHubTargets.FLASH_MESSAGE_CONTAINER).to_contain_text("Title is required."),
    )

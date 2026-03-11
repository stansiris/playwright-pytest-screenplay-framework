"""TaskHub UI integration tests expressed with Screenplay tasks and questions."""

import pytest

from screenplay_core.consequences.ensure import Ensure
from taskhub.automation.questions.on_tasks_page import OnTaskHubTasksPage
from taskhub.automation.questions.task_completed import TaskCompleted
from taskhub.automation.tasks.create_task import CreateTask
from taskhub.automation.tasks.delete_task import DeleteTask
from taskhub.automation.tasks.edit_task import EditTask
from taskhub.automation.tasks.filter_tasks import FilterTasks
from taskhub.automation.tasks.login import LoginToTaskHub
from taskhub.automation.tasks.open_taskhub import OpenTaskHub
from taskhub.automation.tasks.toggle_task_completion import ToggleTaskCompletion
from taskhub.automation.ui.targets import TaskHubTargets


@pytest.mark.ui
@pytest.mark.integration
def test_successful_login(taskhub_customer) -> None:
    taskhub_customer.attempts_to(
        OpenTaskHub.app(),
        Ensure.that(TaskHubTargets.LOGIN_SUBMIT_BUTTON).to_be_visible(),
        LoginToTaskHub.with_credentials("admin", "admin123"),
        Ensure.that(TaskHubTargets.TASK_LIST_CONTAINER).to_be_visible(),
    )
    assert taskhub_customer.asks_for(OnTaskHubTasksPage())


@pytest.mark.ui
@pytest.mark.integration
def test_failed_login(taskhub_customer) -> None:
    taskhub_customer.attempts_to(
        OpenTaskHub.app(),
        Ensure.that(TaskHubTargets.LOGIN_SUBMIT_BUTTON).to_be_visible(),
        LoginToTaskHub.with_credentials("admin", "wrong-password"),
        Ensure.that(TaskHubTargets.LOGIN_ERROR_MESSAGE).to_be_visible(),
        Ensure.that(TaskHubTargets.LOGIN_ERROR_MESSAGE).to_contain_text(
            "Invalid username or password."
        ),
    )


@pytest.mark.ui
@pytest.mark.integration
def test_create_task(taskhub_logged_in_customer) -> None:
    new_title = "UI create task"
    taskhub_logged_in_customer.attempts_to(
        CreateTask.named(
            title=new_title,
            description="Created from UI test",
            priority="HIGH",
            due_date="2030-02-01",
        ),
        Ensure.that(TaskHubTargets.task_item_for_title(new_title)).to_be_visible(),
    )


@pytest.mark.ui
@pytest.mark.integration
def test_edit_task(taskhub_logged_in_customer) -> None:
    original_title = "UI edit task original"
    updated_title = "UI edit task updated"
    taskhub_logged_in_customer.attempts_to(
        CreateTask.named(title=original_title, description="Original", priority="LOW"),
        Ensure.that(TaskHubTargets.task_item_for_title(original_title)).to_be_visible(),
        EditTask.from_title(
            current_title=original_title,
            new_title=updated_title,
            new_description="Updated description",
            new_priority="HIGH",
            new_due_date="2030-03-01",
        ),
        Ensure.that(TaskHubTargets.task_item_for_title(updated_title)).to_be_visible(),
        Ensure.that(TaskHubTargets.task_item_for_title(original_title)).to_have_count(0),
    )


@pytest.mark.ui
@pytest.mark.integration
def test_complete_task(taskhub_logged_in_customer) -> None:
    title = "UI complete task"
    taskhub_logged_in_customer.attempts_to(
        CreateTask.named(title=title, description="Needs completion"),
        Ensure.that(TaskHubTargets.task_item_for_title(title)).to_be_visible(),
        ToggleTaskCompletion.for_title(title),
    )
    assert taskhub_logged_in_customer.asks_for(TaskCompleted(title))


@pytest.mark.ui
@pytest.mark.integration
def test_delete_task(taskhub_logged_in_customer) -> None:
    title = "UI delete task"
    taskhub_logged_in_customer.attempts_to(
        CreateTask.named(title=title),
        Ensure.that(TaskHubTargets.task_item_for_title(title)).to_be_visible(),
        DeleteTask.named(title),
        Ensure.that(TaskHubTargets.task_item_for_title(title)).to_have_count(0),
    )


@pytest.mark.ui
@pytest.mark.integration
def test_filter_completed_tasks(taskhub_logged_in_customer) -> None:
    active_title = "UI active task for filtering"
    completed_title = "UI completed task for filtering"

    taskhub_logged_in_customer.attempts_to(
        CreateTask.named(title=active_title),
        CreateTask.named(title=completed_title),
        ToggleTaskCompletion.for_title(completed_title),
        FilterTasks.by("completed"),
        Ensure.that(TaskHubTargets.task_item_for_title(completed_title)).to_be_visible(),
        Ensure.that(TaskHubTargets.task_item_for_title(active_title)).to_have_count(0),
    )


@pytest.mark.ui
@pytest.mark.integration
def test_empty_title_validation_error(taskhub_logged_in_customer) -> None:
    taskhub_logged_in_customer.attempts_to(
        CreateTask.named(title="", description="Missing title should fail"),
        Ensure.that(TaskHubTargets.FLASH_MESSAGE_CONTAINER).to_contain_text("Title is required."),
    )

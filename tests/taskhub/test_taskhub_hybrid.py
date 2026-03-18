"""TaskHub hybrid integration tests that cross UI and API boundaries."""

from __future__ import annotations

import pytest

from examples.taskhub.automation.questions.api_questions import (
    TaskExistsViaApi,
    TaskFieldEqualsViaApi,
    TaskIdForTitleViaApi,
)
from examples.taskhub.automation.tasks.api_tasks import CreateTaskViaApi, LoginToTaskHubApi
from examples.taskhub.automation.tasks.create_task import CreateTask
from examples.taskhub.automation.tasks.login import LoginToTaskHub
from examples.taskhub.automation.tasks.open_taskhub import OpenTaskHub
from examples.taskhub.automation.ui.targets import TaskHubTargets
from screenplay_core.playwright.ensure import Ensure

pytestmark = [pytest.mark.hybrid, pytest.mark.integration]


def test_create_task_via_api_verify_in_ui(taskhub_api_actor, taskhub_customer) -> None:
    title = "Hybrid API to UI task"
    create_task = CreateTaskViaApi.with_payload(
        {
            "title": title,
            "description": "Created through API then validated in UI",
            "priority": "HIGH",
        }
    )
    taskhub_api_actor.attempts_to(
        LoginToTaskHubApi.with_credentials("admin", "admin123"),
        create_task,
    )
    assert create_task.result.status_code == 201
    assert create_task.task_id is not None

    taskhub_customer.attempts_to(
        OpenTaskHub.app(),
        LoginToTaskHub.with_credentials("admin", "admin123"),
        Ensure.that(TaskHubTargets.task_item_for_id(create_task.task_id)).to_be_visible(),
        Ensure.that(TaskHubTargets.task_title_text_for_id(create_task.task_id)).to_have_text(title),
    )


def test_create_task_via_ui_verify_in_api(
    taskhub_logged_in_customer,
    taskhub_api_actor,
) -> None:
    title = "Hybrid UI to API task"
    taskhub_logged_in_customer.attempts_to(
        CreateTask.named(
            title=title,
            description="Created through UI then validated in API",
            priority="MEDIUM",
            due_date="2030-05-01",
        ),
    )

    taskhub_api_actor.attempts_to(LoginToTaskHubApi.with_credentials("admin", "admin123"))
    task_id = taskhub_api_actor.asks_for(TaskIdForTitleViaApi(title))
    assert task_id is not None
    taskhub_logged_in_customer.attempts_to(
        Ensure.that(TaskHubTargets.task_item_for_id(task_id)).to_be_visible(),
    )

    assert taskhub_api_actor.asks_for(TaskExistsViaApi(task_id))
    assert taskhub_api_actor.asks_for(TaskFieldEqualsViaApi(task_id, "title", title))

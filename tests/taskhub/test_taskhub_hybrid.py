"""TaskHub hybrid integration tests that cross UI and API boundaries."""

from __future__ import annotations

import pytest

from screenplay_core.abilities.call_the_api import CallTheAPI
from screenplay_core.consequences.ensure import Ensure
from screenplay_core.core.actor import Actor
from taskhub.automation.api.client import TaskHubApiClient
from taskhub.automation.tasks.create_task import CreateTask
from taskhub.automation.tasks.login import LoginToTaskHub
from taskhub.automation.tasks.open_taskhub import OpenTaskHub
from taskhub.automation.ui.targets import TaskHubTargets


def _taskhub_api(actor: Actor) -> TaskHubApiClient:
    return TaskHubApiClient(actor.ability_to(CallTheAPI))


@pytest.mark.integration
def test_create_task_via_api_verify_in_ui(taskhub_api_actor: Actor, taskhub_customer) -> None:
    taskhub_api = _taskhub_api(taskhub_api_actor)
    title = "Hybrid API to UI task"
    taskhub_api.post_login("admin", "admin123")
    create_response = taskhub_api.create_task(
        {
            "title": title,
            "description": "Created through API then validated in UI",
            "priority": "HIGH",
        }
    )
    assert create_response.status_code == 201

    taskhub_customer.attempts_to(
        OpenTaskHub.app(),
        LoginToTaskHub.with_credentials("admin", "admin123"),
        Ensure.that(TaskHubTargets.task_item_for_title(title)).to_be_visible(),
    )


@pytest.mark.integration
def test_create_task_via_ui_verify_in_api(
    taskhub_logged_in_customer,
    taskhub_api_actor: Actor,
) -> None:
    taskhub_api = _taskhub_api(taskhub_api_actor)
    title = "Hybrid UI to API task"
    taskhub_logged_in_customer.attempts_to(
        CreateTask.named(
            title=title,
            description="Created through UI then validated in API",
            priority="MEDIUM",
            due_date="2030-05-01",
        ),
        Ensure.that(TaskHubTargets.task_item_for_title(title)).to_be_visible(),
    )

    taskhub_api.post_login("admin", "admin123")
    tasks_response = taskhub_api.get_tasks()
    assert tasks_response.status_code == 200
    task_titles = [item["title"] for item in tasks_response.json()["items"]]
    assert title in task_titles

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from examples.taskhub.automation.api.client import TaskHubApiClient
from screenplay_core.abilities.call_the_api import CallTheApi
from screenplay_core.core.actor import Actor
from screenplay_core.core.question import Question


@dataclass(frozen=True)
class ApiResponseSnapshot:
    status_code: int
    payload: Any


def _taskhub_api(actor: Actor) -> TaskHubApiClient:
    return TaskHubApiClient(actor.ability_to(CallTheApi))


def _snapshot(response) -> ApiResponseSnapshot:
    try:
        payload = response.json()
    except ValueError:
        payload = None
    return ApiResponseSnapshot(status_code=response.status_code, payload=payload)


class CurrentUserViaApi(Question):
    """Question: current authenticated user from /api/me."""

    def answered_by(self, actor: Actor) -> ApiResponseSnapshot:
        response = _taskhub_api(actor).get_me()
        return _snapshot(response)

    def __repr__(self) -> str:
        return "CurrentUserViaApi()"


class FetchTasksViaApi(Question):
    """Question: response snapshot from GET /api/tasks."""

    def __init__(self, filter_name: str = "all"):
        self.filter_name = filter_name

    def answered_by(self, actor: Actor) -> ApiResponseSnapshot:
        response = _taskhub_api(actor).get_tasks(filter_name=self.filter_name)
        return _snapshot(response)

    def __repr__(self) -> str:
        return f"FetchTasksViaApi(filter_name='{self.filter_name}')"

    @classmethod
    def all(cls) -> FetchTasksViaApi:
        return cls(filter_name="all")


class FetchTaskViaApi(Question):
    """Question: response snapshot from GET /api/tasks/<id>."""

    def __init__(self, task_id: int):
        self.task_id = task_id

    def answered_by(self, actor: Actor) -> ApiResponseSnapshot:
        response = _taskhub_api(actor).get_task(self.task_id)
        return _snapshot(response)

    def __repr__(self) -> str:
        return f"FetchTaskViaApi(task_id={self.task_id})"

    @classmethod
    def by_id(cls, task_id: int) -> FetchTaskViaApi:
        return cls(task_id=task_id)


class TaskExistsViaApi(Question):
    """Question: whether a task currently exists by ID."""

    def __init__(self, task_id: int):
        self.task_id = task_id

    def answered_by(self, actor: Actor) -> bool:
        response = _taskhub_api(actor).get_task(self.task_id)
        return response.status_code == 200

    def __repr__(self) -> str:
        return f"TaskExistsViaApi(task_id={self.task_id})"


class TaskFieldEqualsViaApi(Question):
    """Question: whether a task field equals an expected value."""

    def __init__(self, task_id: int, field_name: str, expected_value: Any):
        self.task_id = task_id
        self.field_name = field_name
        self.expected_value = expected_value

    def answered_by(self, actor: Actor) -> bool:
        response = _taskhub_api(actor).get_task(self.task_id)
        if response.status_code != 200:
            return False

        payload = response.json()
        if not isinstance(payload, dict):
            return False

        return payload.get(self.field_name) == self.expected_value

    def __repr__(self) -> str:
        return (
            f"TaskFieldEqualsViaApi(task_id={self.task_id}, "
            f"field_name='{self.field_name}', expected_value={self.expected_value!r})"
        )


class TaskIdForTitleViaApi(Question):
    """Question: resolve a task ID by exact title match in GET /api/tasks."""

    def __init__(self, title: str, filter_name: str = "all"):
        self.title = title
        self.filter_name = filter_name

    def answered_by(self, actor: Actor) -> int | None:
        response = _taskhub_api(actor).get_tasks(filter_name=self.filter_name)
        if response.status_code != 200:
            return None

        payload = response.json()
        if not isinstance(payload, dict):
            return None

        items = payload.get("items")
        if not isinstance(items, list):
            return None

        for item in items:
            if not isinstance(item, dict):
                continue
            if item.get("title") != self.title:
                continue

            task_id = item.get("id")
            try:
                return int(task_id)
            except (TypeError, ValueError):
                return None

        return None

    def __repr__(self) -> str:
        return f"TaskIdForTitleViaApi(title='{self.title}', filter_name='{self.filter_name}')"

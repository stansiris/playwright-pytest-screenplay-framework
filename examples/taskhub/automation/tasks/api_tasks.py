from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from examples.taskhub.automation.api.client import TaskHubApiClient
from screenplay_core.http.call_the_api import CallTheApi
from screenplay_core.core.task import Task


@dataclass
class ApiCallResult:
    status_code: int | None = None
    payload: Any = None


def _taskhub_api(actor) -> TaskHubApiClient:
    return TaskHubApiClient(actor.ability_to(CallTheApi))


def _response_payload(response) -> Any:
    try:
        return response.json()
    except ValueError:
        return None


class LoginToTaskHubApi(Task):
    """Task: authenticate to the TaskHub API."""

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.result = ApiCallResult()

    def __repr__(self) -> str:
        return f"LoginToTaskHubApi(username='{self.username}')"

    def perform_as(self, actor) -> None:
        response = _taskhub_api(actor).post_login(self.username, self.password)
        self.result.status_code = response.status_code
        self.result.payload = _response_payload(response)

    @classmethod
    def with_credentials(cls, username: str, password: str) -> LoginToTaskHubApi:
        return cls(username=username, password=password)


class CreateTaskViaApi(Task):
    """Task: create a TaskHub task using the API."""

    def __init__(self, payload: dict[str, Any]):
        self.payload = payload
        self.result = ApiCallResult()
        self.task_id: int | None = None

    def __repr__(self) -> str:
        title = self.payload.get("title", "")
        return f"CreateTaskViaApi(title='{title}')"

    def perform_as(self, actor) -> None:
        response = _taskhub_api(actor).create_task(self.payload)
        self.result.status_code = response.status_code
        self.result.payload = _response_payload(response)

        self.task_id = None
        if isinstance(self.result.payload, dict) and "id" in self.result.payload:
            try:
                self.task_id = int(self.result.payload["id"])
            except (TypeError, ValueError):
                self.task_id = None

    @classmethod
    def with_payload(cls, payload: dict[str, Any]) -> CreateTaskViaApi:
        return cls(payload=payload)


class UpdateTaskViaApi(Task):
    """Task: update an existing TaskHub task over API."""

    def __init__(self, task_id: int, payload: dict[str, Any]):
        self.task_id = task_id
        self.payload = payload
        self.result = ApiCallResult()

    def __repr__(self) -> str:
        return f"UpdateTaskViaApi(task_id={self.task_id})"

    def perform_as(self, actor) -> None:
        response = _taskhub_api(actor).update_task(self.task_id, self.payload)
        self.result.status_code = response.status_code
        self.result.payload = _response_payload(response)

    @classmethod
    def for_task(cls, task_id: int, payload: dict[str, Any]) -> UpdateTaskViaApi:
        return cls(task_id=task_id, payload=payload)


class DeleteTaskViaApi(Task):
    """Task: delete a TaskHub task over API."""

    def __init__(self, task_id: int):
        self.task_id = task_id
        self.result = ApiCallResult()

    def __repr__(self) -> str:
        return f"DeleteTaskViaApi(task_id={self.task_id})"

    def perform_as(self, actor) -> None:
        response = _taskhub_api(actor).delete_task(self.task_id)
        self.result.status_code = response.status_code
        self.result.payload = _response_payload(response)

    @classmethod
    def for_task(cls, task_id: int) -> DeleteTaskViaApi:
        return cls(task_id=task_id)


class ResetTaskHubDataViaApi(Task):
    """Task: call TaskHub test reset endpoint."""

    def __init__(self):
        self.result = ApiCallResult()

    def __repr__(self) -> str:
        return "ResetTaskHubDataViaApi()"

    def perform_as(self, actor) -> None:
        response = _taskhub_api(actor).reset_test_data()
        self.result.status_code = response.status_code
        self.result.payload = _response_payload(response)


class SeedTaskHubDataViaApi(Task):
    """Task: call TaskHub test seed endpoint."""

    def __init__(self):
        self.result = ApiCallResult()

    def __repr__(self) -> str:
        return "SeedTaskHubDataViaApi()"

    def perform_as(self, actor) -> None:
        response = _taskhub_api(actor).seed_test_data()
        self.result.status_code = response.status_code
        self.result.payload = _response_payload(response)

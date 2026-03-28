from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from examples.work_items.automation.api.client import WorkItemsApiClient
from screenplay_core.core.task import Task
from screenplay_core.http.call_the_api import CallTheApi


@dataclass
class ApiCallResult:
    status_code: int | None = None
    payload: Any = None


def _work_items_api(actor) -> WorkItemsApiClient:
    return WorkItemsApiClient(actor.ability_to(CallTheApi))


def _response_payload(response) -> Any:
    try:
        return response.json()
    except ValueError:
        return None


class LoginToWorkItemsApi(Task):
    """Task: authenticate to the Work Items API."""

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.result = ApiCallResult()

    def __repr__(self) -> str:
        return f"LoginToWorkItemsApi(username='{self.username}')"

    def perform_as(self, actor) -> None:
        response = _work_items_api(actor).post_login(self.username, self.password)
        self.result.status_code = response.status_code
        self.result.payload = _response_payload(response)

    @classmethod
    def with_credentials(cls, username: str, password: str) -> LoginToWorkItemsApi:
        return cls(username=username, password=password)


class CreateWorkItemViaApi(Task):
    """Task: create a work item using the API."""

    def __init__(self, payload: dict[str, Any]):
        self.payload = payload
        self.result = ApiCallResult()
        self.work_item_id: int | None = None

    def __repr__(self) -> str:
        title = self.payload.get("title", "")
        return f"CreateWorkItemViaApi(title='{title}')"

    def perform_as(self, actor) -> None:
        response = _work_items_api(actor).create_work_item(self.payload)
        self.result.status_code = response.status_code
        self.result.payload = _response_payload(response)

        self.work_item_id = None
        if isinstance(self.result.payload, dict) and "id" in self.result.payload:
            try:
                self.work_item_id = int(self.result.payload["id"])
            except (TypeError, ValueError):
                self.work_item_id = None

    @classmethod
    def with_payload(cls, payload: dict[str, Any]) -> CreateWorkItemViaApi:
        return cls(payload=payload)


class UpdateWorkItemViaApi(Task):
    """Task: update an existing work item over API."""

    def __init__(self, work_item_id: int, payload: dict[str, Any]):
        self.work_item_id = work_item_id
        self.payload = payload
        self.result = ApiCallResult()

    def __repr__(self) -> str:
        return f"UpdateWorkItemViaApi(work_item_id={self.work_item_id})"

    def perform_as(self, actor) -> None:
        response = _work_items_api(actor).update_work_item(self.work_item_id, self.payload)
        self.result.status_code = response.status_code
        self.result.payload = _response_payload(response)

    @classmethod
    def for_work_item(cls, work_item_id: int, payload: dict[str, Any]) -> UpdateWorkItemViaApi:
        return cls(work_item_id=work_item_id, payload=payload)


class DeleteWorkItemViaApi(Task):
    """Task: delete a work item over API."""

    def __init__(self, work_item_id: int):
        self.work_item_id = work_item_id
        self.result = ApiCallResult()

    def __repr__(self) -> str:
        return f"DeleteWorkItemViaApi(work_item_id={self.work_item_id})"

    def perform_as(self, actor) -> None:
        response = _work_items_api(actor).delete_work_item(self.work_item_id)
        self.result.status_code = response.status_code
        self.result.payload = _response_payload(response)

    @classmethod
    def for_work_item(cls, work_item_id: int) -> DeleteWorkItemViaApi:
        return cls(work_item_id=work_item_id)


class ResetWorkItemsDataViaApi(Task):
    """Task: call the Work Items test reset endpoint."""

    def __init__(self):
        self.result = ApiCallResult()

    def __repr__(self) -> str:
        return "ResetWorkItemsDataViaApi()"

    def perform_as(self, actor) -> None:
        response = _work_items_api(actor).reset_test_data()
        self.result.status_code = response.status_code
        self.result.payload = _response_payload(response)


class SeedWorkItemsDataViaApi(Task):
    """Task: call the Work Items test seed endpoint."""

    def __init__(self):
        self.result = ApiCallResult()

    def __repr__(self) -> str:
        return "SeedWorkItemsDataViaApi()"

    def perform_as(self, actor) -> None:
        response = _work_items_api(actor).seed_test_data()
        self.result.status_code = response.status_code
        self.result.payload = _response_payload(response)

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from examples.work_items.automation.api.work_items_api import WorkItemsApi
from screenplay_core.core.task import Task


def _payload_summary(payload: dict[str, Any]) -> str:
    """Return a compact, human-readable summary for work-item payloads."""
    parts: list[str] = []
    for key in ("title", "status", "priority"):
        value = payload.get(key)
        if value:
            parts.append(f"{key}={value!r}")

    if parts:
        return ", ".join(parts)

    return f"payload_keys={sorted(payload.keys())!r}"


@dataclass
class LoginToWorkItemsApi(Task):
    username: str
    password: str = field(repr=False)

    def perform_as(self, actor) -> None:
        WorkItemsApi.for_actor(actor).login(self.username, self.password)

    def __repr__(self) -> str:
        return f"LoginToWorkItemsApi(username={self.username!r})"

    @classmethod
    def with_credentials(cls, username: str, password: str) -> LoginToWorkItemsApi:
        return cls(username=username, password=password)


@dataclass
class CreateWorkItemViaApi(Task):
    payload: dict[str, Any]

    def perform_as(self, actor) -> None:
        WorkItemsApi.for_actor(actor).create_work_item(self.payload)

    def __repr__(self) -> str:
        return f"CreateWorkItemViaApi({_payload_summary(self.payload)})"

    @classmethod
    def with_payload(cls, payload: dict[str, Any]) -> CreateWorkItemViaApi:
        return cls(payload=payload)


@dataclass
class UpdateWorkItemViaApi(Task):
    work_item_id: int
    payload: dict[str, Any]

    def perform_as(self, actor) -> None:
        WorkItemsApi.for_actor(actor).update_work_item(
            self.work_item_id,
            self.payload,
        )

    def __repr__(self) -> str:
        return (
            f"UpdateWorkItemViaApi(work_item_id={self.work_item_id}, "
            f"{_payload_summary(self.payload)})"
        )

    @classmethod
    def for_work_item(
        cls,
        work_item_id: int,
        payload: dict[str, Any],
    ) -> UpdateWorkItemViaApi:
        return cls(work_item_id=work_item_id, payload=payload)


@dataclass
class DeleteWorkItemViaApi(Task):
    work_item_id: int

    def perform_as(self, actor) -> None:
        WorkItemsApi.for_actor(actor).delete_work_item(self.work_item_id)

    def __repr__(self) -> str:
        return f"DeleteWorkItemViaApi(work_item_id={self.work_item_id})"

    @classmethod
    def for_work_item(cls, work_item_id: int) -> DeleteWorkItemViaApi:
        return cls(work_item_id=work_item_id)


class ResetWorkItemsDataViaApi(Task):
    def perform_as(self, actor) -> None:
        WorkItemsApi.for_actor(actor).reset_test_data()


class SeedWorkItemsDataViaApi(Task):
    def perform_as(self, actor) -> None:
        WorkItemsApi.for_actor(actor).seed_test_data()

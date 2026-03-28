from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from examples.work_items.automation.api.client import WorkItemsApiClient
from screenplay_core.core.actor import Actor
from screenplay_core.core.question import Question
from screenplay_core.http.call_the_api import CallTheApi


@dataclass(frozen=True)
class ApiResponseSnapshot:
    status_code: int
    payload: Any


def _work_items_api(actor: Actor) -> WorkItemsApiClient:
    return WorkItemsApiClient(actor.ability_to(CallTheApi))


def _snapshot(response) -> ApiResponseSnapshot:
    try:
        payload = response.json()
    except ValueError:
        payload = None
    return ApiResponseSnapshot(status_code=response.status_code, payload=payload)


class CurrentUserViaApi(Question):
    """Question: current authenticated user from /api/me."""

    def answered_by(self, actor: Actor) -> ApiResponseSnapshot:
        response = _work_items_api(actor).get_me()
        return _snapshot(response)

    def __repr__(self) -> str:
        return "CurrentUserViaApi()"


class FetchWorkItemsViaApi(Question):
    """Question: response snapshot from GET /api/work-items."""

    def __init__(self, filter_name: str = "all"):
        self.filter_name = filter_name

    def answered_by(self, actor: Actor) -> ApiResponseSnapshot:
        response = _work_items_api(actor).get_work_items(filter_name=self.filter_name)
        return _snapshot(response)

    def __repr__(self) -> str:
        return f"FetchWorkItemsViaApi(filter_name='{self.filter_name}')"

    @classmethod
    def all(cls) -> FetchWorkItemsViaApi:
        return cls(filter_name="all")


class FetchWorkItemViaApi(Question):
    """Question: response snapshot from GET /api/work-items/<id>."""

    def __init__(self, work_item_id: int):
        self.work_item_id = work_item_id

    def answered_by(self, actor: Actor) -> ApiResponseSnapshot:
        response = _work_items_api(actor).get_work_item(self.work_item_id)
        return _snapshot(response)

    def __repr__(self) -> str:
        return f"FetchWorkItemViaApi(work_item_id={self.work_item_id})"

    @classmethod
    def by_id(cls, work_item_id: int) -> FetchWorkItemViaApi:
        return cls(work_item_id=work_item_id)


class WorkItemExistsViaApi(Question):
    """Question: whether a work item currently exists by id."""

    def __init__(self, work_item_id: int):
        self.work_item_id = work_item_id

    def answered_by(self, actor: Actor) -> bool:
        response = _work_items_api(actor).get_work_item(self.work_item_id)
        return response.status_code == 200

    def __repr__(self) -> str:
        return f"WorkItemExistsViaApi(work_item_id={self.work_item_id})"


class WorkItemFieldEqualsViaApi(Question):
    """Question: whether a work item field equals an expected value."""

    def __init__(self, work_item_id: int, field_name: str, expected_value: Any):
        self.work_item_id = work_item_id
        self.field_name = field_name
        self.expected_value = expected_value

    def answered_by(self, actor: Actor) -> bool:
        response = _work_items_api(actor).get_work_item(self.work_item_id)
        if response.status_code != 200:
            return False

        payload = response.json()
        if not isinstance(payload, dict):
            return False

        return payload.get(self.field_name) == self.expected_value

    def __repr__(self) -> str:
        return (
            f"WorkItemFieldEqualsViaApi(work_item_id={self.work_item_id}, "
            f"field_name='{self.field_name}', expected_value={self.expected_value!r})"
        )


class WorkItemIdForTitleViaApi(Question):
    """Question: resolve a work item id by exact title match in GET /api/work-items."""

    def __init__(self, title: str, filter_name: str = "all"):
        self.title = title
        self.filter_name = filter_name

    def answered_by(self, actor: Actor) -> int | None:
        response = _work_items_api(actor).get_work_items(filter_name=self.filter_name)
        if response.status_code != 200:
            return None

        payload = response.json()
        if not isinstance(payload, dict):
            return None

        work_items = payload.get("work_items")
        if not isinstance(work_items, list):
            return None

        for work_item in work_items:
            if not isinstance(work_item, dict):
                continue
            if work_item.get("title") != self.title:
                continue

            work_item_id = work_item.get("id")
            try:
                return int(work_item_id)
            except (TypeError, ValueError):
                return None

        return None

    def __repr__(self) -> str:
        return (
            f"WorkItemIdForTitleViaApi(title='{self.title}', " f"filter_name='{self.filter_name}')"
        )

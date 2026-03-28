from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from requests import Response

from examples.work_items.automation.api.work_items_api import WorkItemsApi
from screenplay_core.core.actor import Actor
from screenplay_core.core.question import Question


@dataclass(frozen=True)
class ApiResponseSnapshot:
    status_code: int
    payload: Any


def _json_or_none(response: Response) -> Any:
    try:
        return response.json()
    except ValueError:
        return None


def _snapshot(response: Response) -> ApiResponseSnapshot:
    return ApiResponseSnapshot(
        status_code=response.status_code,
        payload=_json_or_none(response),
    )


class CurrentUserViaApi(Question):
    """Question: current authenticated user from /api/me."""

    def answered_by(self, actor: Actor) -> ApiResponseSnapshot:
        response = WorkItemsApi.for_actor(actor).me()
        return _snapshot(response)

    def __repr__(self) -> str:
        return "CurrentUserViaApi()"


@dataclass(frozen=True)
class FetchWorkItemsViaApi(Question):
    """Question: response snapshot from GET /api/work-items."""

    filter_name: str = "all"

    def answered_by(self, actor: Actor) -> ApiResponseSnapshot:
        response = WorkItemsApi.for_actor(actor).work_items(filter_name=self.filter_name)
        return _snapshot(response)

    @classmethod
    def all(cls) -> FetchWorkItemsViaApi:
        return cls(filter_name="all")


@dataclass(frozen=True)
class FetchWorkItemViaApi(Question):
    """Question: response snapshot from GET /api/work-items/<id>."""

    work_item_id: int

    def answered_by(self, actor: Actor) -> ApiResponseSnapshot:
        response = WorkItemsApi.for_actor(actor).work_item(self.work_item_id)
        return _snapshot(response)

    @classmethod
    def by_id(cls, work_item_id: int) -> FetchWorkItemViaApi:
        return cls(work_item_id=work_item_id)


@dataclass(frozen=True)
class WorkItemExistsViaApi(Question):
    """Question: whether a work item currently exists by id."""

    work_item_id: int

    def answered_by(self, actor: Actor) -> bool:
        response = WorkItemsApi.for_actor(actor).work_item(self.work_item_id)
        return response.status_code == 200


@dataclass(frozen=True)
class WorkItemFieldEqualsViaApi(Question):
    """Question: whether a work item field equals an expected value."""

    work_item_id: int
    field_name: str
    expected_value: Any

    def answered_by(self, actor: Actor) -> bool:
        response = WorkItemsApi.for_actor(actor).work_item(self.work_item_id)
        if response.status_code != 200:
            return False

        payload = _json_or_none(response)
        if not isinstance(payload, dict):
            return False

        return payload.get(self.field_name) == self.expected_value


@dataclass(frozen=True)
class WorkItemIdForTitleViaApi(Question):
    """Question: resolve a work item id by exact title match in GET /api/work-items."""

    title: str
    filter_name: str = "all"

    def answered_by(self, actor: Actor) -> int | None:
        response = WorkItemsApi.for_actor(actor).work_items(filter_name=self.filter_name)
        if response.status_code != 200:
            return None

        payload = _json_or_none(response)
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

from __future__ import annotations

from typing import Any

from requests import Response

from screenplay_core.http.call_the_api import CallTheApi


class WorkItemsApi:
    """Work Items-specific facade over the generic CallTheApi ability."""

    def __init__(self, api: CallTheApi):
        self.api = api

    @classmethod
    def for_actor(cls, actor) -> WorkItemsApi:
        return cls(actor.ability_to(CallTheApi))

    def login(self, username: str, password: str) -> Response:
        return self.api.post(
            "/api/login",
            json={"username": username, "password": password},
        )

    def logout(self) -> Response:
        return self.api.post("/api/logout")

    def me(self) -> Response:
        return self.api.get("/api/me")

    def work_items(self, filter_name: str = "all") -> Response:
        return self.api.get(
            "/api/work-items",
            params={"filter": filter_name},
        )

    def create_work_item(self, payload: dict[str, Any]) -> Response:
        return self.api.post("/api/work-items", json=payload)

    def work_item(self, work_item_id: int) -> Response:
        return self.api.get(f"/api/work-items/{work_item_id}")

    def update_work_item(self, work_item_id: int, payload: dict[str, Any]) -> Response:
        return self.api.put(f"/api/work-items/{work_item_id}", json=payload)

    def delete_work_item(self, work_item_id: int) -> Response:
        return self.api.delete(f"/api/work-items/{work_item_id}")

    def reset_test_data(self) -> Response:
        return self.api.post("/api/test/reset")

    def seed_test_data(self) -> Response:
        return self.api.post("/api/test/seed")

from __future__ import annotations

from typing import Any

from requests import Response

from screenplay_core.http.call_the_api import CallTheApi


class TaskHubApiClient:
    """Small session-based helper for TaskHub JSON API endpoints."""

    def __init__(self, api_or_base_url: CallTheApi | str):
        if isinstance(api_or_base_url, CallTheApi):
            self.api = api_or_base_url
            self._owns_api_ability = False
            return

        self.api = CallTheApi.at(api_or_base_url)
        self._owns_api_ability = True

    def close(self) -> None:
        if self._owns_api_ability:
            self.api.close()

    def post_login(self, username: str, password: str) -> Response:
        return self.api.post(
            "/api/login",
            json={"username": username, "password": password},
        )

    def post_logout(self) -> Response:
        return self.api.post("/api/logout")

    def get_me(self) -> Response:
        return self.api.get("/api/me")

    def get_tasks(self, filter_name: str = "all") -> Response:
        return self.api.get(
            "/api/tasks",
            params={"filter": filter_name},
        )

    def create_task(self, payload: dict[str, Any]) -> Response:
        return self.api.post("/api/tasks", json=payload)

    def get_task(self, task_id: int) -> Response:
        return self.api.get(f"/api/tasks/{task_id}")

    def update_task(self, task_id: int, payload: dict[str, Any]) -> Response:
        return self.api.put(f"/api/tasks/{task_id}", json=payload)

    def delete_task(self, task_id: int) -> Response:
        return self.api.delete(f"/api/tasks/{task_id}")

    def reset_test_data(self) -> Response:
        return self.api.post("/api/test/reset")

    def seed_test_data(self) -> Response:
        return self.api.post("/api/test/seed")

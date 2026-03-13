from __future__ import annotations

from typing import Any

import requests
from requests import Response, Session


class CallTheApi:
    """
    Ability wrapper around requests.Session.
    Keeps HTTP transport details out of Actor/Tasks.
    """

    def __init__(
        self,
        base_url: str,
        session: Session | None = None,
        timeout_seconds: float = 10,
    ):
        """Store API endpoint context and HTTP session state."""
        self.base_url = base_url.rstrip("/")
        self.session = session or requests.Session()
        self.timeout_seconds = timeout_seconds

    @staticmethod
    def at(
        base_url: str,
        session: Session | None = None,
        timeout_seconds: float = 10,
    ) -> CallTheApi:
        """Factory for readability in actor fixture setup."""
        return CallTheApi(base_url, session=session, timeout_seconds=timeout_seconds)

    def close(self) -> None:
        """Close underlying HTTP session."""
        self.session.close()

    def request(self, method: str, path: str, **kwargs: Any) -> Response:
        """Dispatch an HTTP request against ability base URL."""
        # Apply a safe default timeout unless the caller explicitly overrides it.
        if "timeout" not in kwargs:
            kwargs["timeout"] = self.timeout_seconds
        return self.session.request(
            method=method.upper(),
            url=self._url(path),
            **kwargs,
        )

    def get(self, path: str, **kwargs: Any) -> Response:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> Response:
        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs: Any) -> Response:
        return self.request("PUT", path, **kwargs)

    def patch(self, path: str, **kwargs: Any) -> Response:
        return self.request("PATCH", path, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> Response:
        return self.request("DELETE", path, **kwargs)

    def _url(self, path: str) -> str:
        # Allow full URLs for edge cases (e.g., cross-service calls in a single test).
        if path.startswith(("http://", "https://")):
            return path
        return f"{self.base_url}/{path.lstrip('/')}"

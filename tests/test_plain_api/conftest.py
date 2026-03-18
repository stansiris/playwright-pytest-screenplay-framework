from collections.abc import Generator

import pytest
from playwright.sync_api import APIRequestContext, Playwright

from examples.taskhub.app.seed import (
    DEFAULT_PASSWORD,
    DEFAULT_USERNAME,
    SECONDARY_PASSWORD,
    SECONDARY_USERNAME,
)


def pytest_configure(config) -> None:
    """Default base_url for test_plain_api suite — overridable via --base-url on CLI."""
    if not getattr(config.option, "base_url", None):
        config.option.base_url = "http://127.0.0.1:5001"


@pytest.fixture(scope="session")
def api(playwright: Playwright, base_url: str) -> Generator[APIRequestContext, None, None]:
    """Standalone APIRequestContext — no browser, no cookie sharing."""
    ctx = playwright.request.new_context(base_url=base_url)
    yield ctx
    ctx.dispose()


def _make_api_auth_context(
    playwright: Playwright, base_url: str, username: str, password: str
) -> Generator[APIRequestContext, None, None]:
    ctx = playwright.request.new_context(base_url=base_url)
    response = ctx.post("/api/login", data={"username": username, "password": password})
    assert response.ok, f"Login failed with status {response.status}: {response.text()}"
    yield ctx
    ctx.dispose()


@pytest.fixture
def api_auth_admin(playwright: Playwright, base_url: str) -> Generator[APIRequestContext, None, None]:
    """APIRequestContext with admin credentials — no browser, no cookie sharing."""
    yield from _make_api_auth_context(playwright, base_url, DEFAULT_USERNAME, DEFAULT_PASSWORD)


@pytest.fixture
def api_auth_guest(playwright: Playwright, base_url: str) -> Generator[APIRequestContext, None, None]:
    """APIRequestContext with guest credentials — no browser, no cookie sharing."""
    yield from _make_api_auth_context(playwright, base_url, SECONDARY_USERNAME, SECONDARY_PASSWORD)

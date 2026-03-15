from collections.abc import Generator

import pytest
from playwright.sync_api import APIRequestContext, BrowserContext, Playwright

from examples.taskhub.automation.tasks.login import LoginToTaskHub
from examples.taskhub.automation.tasks.open_taskhub import OpenTaskHub
from screenplay_core.abilities.browse_the_web import BrowseTheWeb
from screenplay_core.core.actor import Actor

TASKHUB_URL = "http://127.0.0.1:5001"


@pytest.fixture
def taskhub_browser_context(browser: BrowserContext) -> Generator[BrowserContext, None, None]:
    """Override the default base_url from pyproject.toml so that UI/API interactions
    target TaskHub, not the globally configured app (e.g. saucedemo).
    """
    context = browser.new_context(base_url=TASKHUB_URL)
    yield context
    context.close()


@pytest.fixture(scope="session")
def api(playwright: Playwright) -> Generator[APIRequestContext, None, None]:
    """Create a Playwright APIRequestContext for making API calls to TaskHub."""
    ctx = playwright.request.new_context(base_url=TASKHUB_URL)
    yield ctx
    ctx.dispose()


@pytest.fixture(autouse=True)
def reset_data(api: APIRequestContext) -> None:
    """Reset TaskHub data before each test by calling the API endpoint."""
    api.post("/api/test/reset")


@pytest.fixture
def auth_api(playwright: Playwright) -> Generator[APIRequestContext, None, None]:
    """Create an authenticated APIRequestContext for making API calls to TaskHub."""
    ctx = playwright.request.new_context(base_url=TASKHUB_URL)
    ctx.post("/api/auth/login", data={"username": "admin", "password": "admin123"})
    yield ctx
    ctx.dispose()


@pytest.fixture
def logged_in_taskhub_customer(taskhub_browser_context: BrowserContext) -> Actor:
    """Provide an Actor logged in to TaskHub via the UI.
    Uses taskhub_browser_context so page.request shares the session cookie.
    """
    page = taskhub_browser_context.new_page()
    customer = Actor("Logged In TaskHub Customer").can(
        BrowseTheWeb.using(page, base_url=TASKHUB_URL + "/login")
    )
    customer.attempts_to(
        OpenTaskHub(),
        LoginToTaskHub.with_credentials("admin", "admin123"),
    )
    return customer

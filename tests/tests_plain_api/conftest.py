from collections.abc import Generator

import pytest
from playwright.sync_api import APIRequestContext, BrowserContext, Playwright

from examples.taskhub.automation.tasks.login import LoginToTaskHub
from examples.taskhub.automation.tasks.open_taskhub import OpenTaskHub
from screenplay_core.abilities.browse_the_web import BrowseTheWeb
from screenplay_core.core.actor import Actor


@pytest.fixture(scope="session")
def base_url(pytestconfig) -> str:
    """Read --base-url from CLI and normalise to no trailing slash."""
    return pytestconfig.getoption("base_url").rstrip("/")


@pytest.fixture
def taskhub_browser_context(  # noqa: E501
    browser: BrowserContext, base_url: str
) -> Generator[BrowserContext, None, None]:
    """Create a BrowserContext with base_url set to TaskHub.
    Passed via --base-url on the CLI so page.request uses relative paths.
    """
    context = browser.new_context(base_url=base_url)
    yield context
    context.close()


@pytest.fixture(scope="session")
def api(playwright: Playwright, base_url: str) -> Generator[APIRequestContext, None, None]:
    """Standalone APIRequestContext — no browser, no cookie sharing."""
    ctx = playwright.request.new_context(base_url=base_url)
    yield ctx
    ctx.dispose()


# @pytest.fixture(autouse=True)
# def reset_data(api: APIRequestContext) -> None:
#     """Reset TaskHub data before each test by calling the API endpoint."""
#     api.post("/api/test/reset")


@pytest.fixture
def auth_api(playwright: Playwright, base_url: str) -> Generator[APIRequestContext, None, None]:
    """Authenticated standalone APIRequestContext — logs in via API."""
    ctx = playwright.request.new_context(base_url=base_url)
    ctx.post("/api/auth/login", data={"username": "admin", "password": "admin123"})
    yield ctx
    ctx.dispose()


@pytest.fixture
def logged_in_taskhub_customer(taskhub_browser_context: BrowserContext) -> Actor:
    """Provide an Actor logged in to TaskHub via the UI.
    Uses taskhub_browser_context so page.request shares the session cookie.
    """
    page = taskhub_browser_context.new_page()
    customer = Actor("Logged In TaskHub Customer").can(BrowseTheWeb.using(page))
    customer.attempts_to(
        OpenTaskHub(),
        LoginToTaskHub.with_credentials("admin", "admin123"),
    )
    return customer


@pytest.fixture
def taskhub_page_context(taskhub_browser_context: BrowserContext):
    """Provide a Playwright page context for TaskHub with the base URL set."""
    page = taskhub_browser_context.new_page()
    yield page
    page.close()

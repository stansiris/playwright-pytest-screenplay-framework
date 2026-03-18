import pytest

from screenplay_core.core.actor import Actor
from screenplay_core.playwright.browse_the_web import BrowseTheWeb


@pytest.fixture(scope="session")
def base_url(pytestconfig) -> str:
    url = pytestconfig.getoption("base_url", default=None) or "https://www.saucedemo.com/"
    return url.rstrip("/") + "/"


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict, base_url: str) -> dict:
    """Inject the saucedemo base_url into every BrowserContext for this suite."""
    return {**browser_context_args, "base_url": base_url}


@pytest.fixture
def customer(page, base_url):
    return Actor("Customer").can(
        BrowseTheWeb.using(
            page,
            base_url=base_url,
        )
    )

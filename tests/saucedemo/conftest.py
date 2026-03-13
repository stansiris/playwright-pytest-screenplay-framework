import pytest

from screenplay_core.abilities.browse_the_web import BrowseTheWeb
from screenplay_core.core.actor import Actor


@pytest.fixture(scope="session")
def base_url(pytestconfig) -> str:
    return pytestconfig.getoption("base_url").rstrip("/") + "/"


@pytest.fixture
def customer(page, base_url):
    return Actor("Customer").can(
        BrowseTheWeb.using(
            page,
            base_url=base_url,
        )
    )

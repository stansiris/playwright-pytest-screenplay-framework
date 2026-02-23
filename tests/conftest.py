import pytest

from screenplay.abilities.browse_the_web import BrowseTheWeb
from screenplay.core.actor import Actor

pytest_plugins = [
    "tests.steps.common_steps",
    "tests.steps.golden_path_steps",
    "tests.steps.login_page_steps",
]


@pytest.fixture
def customer(page):
    return Actor("Customer").can(BrowseTheWeb.using(page))

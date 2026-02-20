import pytest

from screenplay.abilities.browse_the_web import BrowseTheWeb
from screenplay.core.actor import Actor


@pytest.fixture
def customer(page):
    return Actor("Customer").can(BrowseTheWeb.using(page))

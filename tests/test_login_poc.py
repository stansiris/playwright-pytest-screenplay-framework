import pytest

from screenplay.abilities.browse_the_web import BrowseTheWeb
from screenplay.core.actor import Actor
from screenplay.interactions.navigate_to import NavigateTo
from screenplay.questions.text_of import TextOf
from screenplay.ui.saucedemo import SauceDemo


@pytest.mark.skip
def test_login_success(page):
    stan = Actor("Stan").can(BrowseTheWeb.using(page))
    stan.attempts_to(NavigateTo(SauceDemo.URL))
    assert stan.asks_for(TextOf(SauceDemo.LOGIN_BUTTON)) == "Login"

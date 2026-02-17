from screenplay.actor import Actor
from screenplay.abilities.browse_the_web import BrowseTheWeb
from screenplay.tasks.login import Login
from screenplay.questions.is_visible import IsVisible
from screenplay.ui.saucedemo import SauceDemo


def test_login_success(page):
    stan = Actor("Stan").can(BrowseTheWeb.using(page))

    stan.attempts_to(
        Login.with_credentials("standard_user", "secret_sauce")
    )

    assert stan.asks_for(IsVisible(SauceDemo.INVENTORY_CONTAINER))

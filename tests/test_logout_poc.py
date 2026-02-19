from screenplay.abilities.browse_the_web import BrowseTheWeb
from screenplay.core.actor import Actor
from screenplay.interactions.wait_until_visible import WaitUntilVisible
from screenplay.questions.is_visible import IsVisible
from screenplay.questions.text_of import TextOf
from screenplay.tasks.login import Login
from screenplay.tasks.logout import Logout
from screenplay.ui.saucedemo import SauceDemo


# @pytest.mark.skip
def test_logout_success(page):
    stan = Actor("Stan").can(BrowseTheWeb.using(page))

    stan.attempts_to(
        Login.with_credentials("standard_user", "secret_sauce"),
        Logout(),
        WaitUntilVisible.for_(SauceDemo.LOGIN_BUTTON),
    )

    assert stan.asks_for(IsVisible(SauceDemo.LOGIN_BUTTON))
    assert stan.asks_for(TextOf(SauceDemo.LOGIN_BUTTON)) == "Login"

from screenplay.abilities.browse_the_web import BrowseTheWeb
from screenplay.core.question import Question
from screenplay.ui.saucedemo import SauceDemo


class OnLoginPage(Question):
    """Question: whether the browser is on the SauceDemo login page."""

    def answered_by(self, actor) -> bool:
        url = actor.ability_to(BrowseTheWeb).page.url.rstrip("/")
        login_url = SauceDemo.URL.rstrip("/")
        return url == login_url and SauceDemo.LOGIN_BUTTON.resolve_for(actor).is_visible()

    def __repr__(self) -> str:
        return "OnLoginPage()"

from examples.saucedemo.ui.pages.login_page import LoginPage
from screenplay_core.playwright.browse_the_web import BrowseTheWeb
from screenplay_core.core.actor import Actor
from screenplay_core.core.question import Question


class OnLoginPage(Question):
    """Question: whether the browser is on the SauceDemo login page."""

    def answered_by(self, actor: Actor) -> bool:
        browse = actor.ability_to(BrowseTheWeb)
        if not browse.base_url:
            return False

        url = browse.page.url.rstrip("/")
        login_url = browse.base_url.rstrip("/")
        return url == login_url and LoginPage.LOGIN_BUTTON.resolve_for(actor).is_visible()

    def __repr__(self) -> str:
        return "OnLoginPage()"

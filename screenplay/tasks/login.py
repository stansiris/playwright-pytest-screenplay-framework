from screenplay.core.task import Task
from screenplay.interactions.click import Click
from screenplay.interactions.fill import Fill
from screenplay.interactions.navigate_to import NavigateTo
from screenplay.ui.saucedemo import SauceDemo


class Login(Task):
    """Task: log into SauceDemo."""

    def __repr__(self) -> str:
        return f"Login(username='{self.username}')"

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def perform_as(self, actor):
        actor.attempts_to(
            NavigateTo(SauceDemo.URL),
            Fill(SauceDemo.LOGIN_USERNAME, self.username),
            Fill(SauceDemo.LOGIN_PASSWORD, self.password),
            Click(SauceDemo.LOGIN_BUTTON),
        )

    @staticmethod
    def with_credentials(username: str, password: str):
        return Login(username, password)

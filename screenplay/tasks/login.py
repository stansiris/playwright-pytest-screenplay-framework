from screenplay.interactions.navigate_to import NavigateTo
from screenplay.interactions.fill import Fill
from screenplay.interactions.click import Click
from screenplay.ui.saucedemo import SauceDemo


class Login:
    """Task: log into SauceDemo."""

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def perform_as(self, actor):
        actor.attempts_to(
            NavigateTo(SauceDemo.URL),
            Fill(SauceDemo.USERNAME, self.username),
            Fill(SauceDemo.PASSWORD, self.password),
            Click(SauceDemo.LOGIN_BUTTON),
        )

    @staticmethod
    def with_credentials(username: str, password: str):
        # Nice Screenplay-ish factory method
        return Login(username, password)

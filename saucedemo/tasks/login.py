from saucedemo.tasks.click_login import ClickLogin
from saucedemo.ui.saucedemo import SauceDemo
from screenplay_core.core.task import Task
from screenplay_core.interactions.fill import Fill


class Login(Task):
    """Task: log into SauceDemo."""

    def __repr__(self) -> str:
        return f"Login(username='{self.username}')"

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def perform_as(self, actor) -> None:
        actor.attempts_to(
            Fill(SauceDemo.LOGIN_USERNAME, self.username),
            Fill(SauceDemo.LOGIN_PASSWORD, self.password),
            ClickLogin(),
        )

    @classmethod
    def with_credentials(cls, username: str, password: str) -> "Login":
        return cls(username, password)

    @classmethod
    def with_username_only(cls, username: str) -> "Login":
        return cls(username=username, password="")

    @classmethod
    def with_password_only(cls, password: str) -> "Login":
        return cls(username="", password=password)

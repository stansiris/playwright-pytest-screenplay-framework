from saucedemo.tasks.click_login import ClickLogin
from saucedemo.tasks.enter_password import EnterPassword
from saucedemo.tasks.enter_username import EnterUsername
from saucedemo.tasks.open_saucedemo import OpenSauceDemo
from screenplay_core.core.task import Task


class Login(Task):
    """Task: log into SauceDemo."""

    def __repr__(self) -> str:
        return f"Login(username='{self.username}')"

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def perform_as(self, actor) -> None:
        actor.attempts_to(
            OpenSauceDemo.app(),
            EnterUsername.as_(self.username),
            EnterPassword.as_(self.password),
            ClickLogin(),
        )

    @classmethod
    def with_credentials(cls, username: str, password: str) -> "Login":
        return cls(username, password)



from saucedemo.tasks.continue_checkout import ContinueCheckout
from saucedemo.tasks.enter_checkout_information import EnterCheckoutInformation
from screenplay_core.core.actor import Actor
from screenplay_core.core.task import Task


class ProvideCheckoutInformation(Task):
    """Task: fill checkout customer details and continue."""

    def __init__(self, first_name: str, last_name: str, postal_code: str):
        self.first_name = first_name
        self.last_name = last_name
        self.postal_code = postal_code

    def __repr__(self) -> str:
        return (
            "ProvideCheckoutInformation("
            f"first_name='{self.first_name}', "
            f"last_name='{self.last_name}', "
            f"postal_code='{self.postal_code}')"
        )

    def perform_as(self, actor: Actor) -> None:
        actor.attempts_to(
            EnterCheckoutInformation.as_customer(
                first_name=self.first_name,
                last_name=self.last_name,
                postal_code=self.postal_code,
            ),
            ContinueCheckout(),
        )

    @classmethod
    def as_customer(
        cls, first_name: str, last_name: str, postal_code: str
    ) -> "ProvideCheckoutInformation":
        return cls(first_name, last_name, postal_code)

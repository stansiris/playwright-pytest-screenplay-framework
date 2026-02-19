from screenplay.core.interaction import Interaction
from screenplay.core.target import Target


class WaitUntilVisible(Interaction):
    """Interaction: wait until a target is visible."""

    def __init__(self, target: Target, timeout_ms: int = 5000):
        self.target = target
        self.timeout_ms = timeout_ms

    def perform_as(self, actor) -> None:
        self.target.resolve_for(actor).wait_for(state="visible", timeout=self.timeout_ms)

    @staticmethod
    def for_(target: Target, timeout_ms: int = 5000) -> "WaitUntilVisible":
        # DSL-ish helper: WaitUntilVisible.for_(SauceDemo.LOGIN_BUTTON)
        return WaitUntilVisible(target, timeout_ms)

    def __repr__(self) -> str:
        return (
            f"WaitUntilVisible(target='{self.target.description}', "
            f"timeout_ms={self.timeout_ms})"
        )
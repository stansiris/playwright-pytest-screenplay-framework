from screenplay.core.interaction import Interaction
from screenplay.core.target import Target


class WaitUntilHidden(Interaction):
    """Interaction: wait until a target is hidden from the user."""

    def __init__(self, target: Target, timeout_ms: int = 5000):
        self.target = target
        self.timeout_ms = timeout_ms

    def perform_as(self, actor) -> None:
        self.target.resolve_for(actor).wait_for(state="hidden", timeout=self.timeout_ms)

    @staticmethod
    def for_(target: Target, timeout_ms: int = 5000) -> "WaitUntilHidden":
        # DSL-ish helper: WaitUntilHidden.for_(SomePage.SPINNER)
        return WaitUntilHidden(target, timeout_ms)

    def __repr__(self) -> str:
        return (
            f"WaitUntilHidden(target='{self.target.description}', "
            f"timeout_ms={self.timeout_ms})"
        )

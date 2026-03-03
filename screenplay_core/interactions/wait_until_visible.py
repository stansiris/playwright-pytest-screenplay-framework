from screenplay_core.core.actor import Actor
from screenplay_core.core.interaction import Interaction
from screenplay_core.core.target import Target
from screenplay_core.interactions._timeouts import resolve_timeout_ms, validate_timeout_ms


class WaitUntilVisible(Interaction):
    """Interaction: wait until a target is visible."""

    def __init__(self, target: Target, timeout_ms: int | None = None):
        self.target = target
        self.timeout_ms = validate_timeout_ms(timeout_ms) if timeout_ms is not None else None

    def perform_as(self, actor: Actor) -> None:
        self.target.resolve_for(actor).wait_for(
            state="visible",
            timeout=resolve_timeout_ms(actor, self.timeout_ms),
        )

    @staticmethod
    def for_(target: Target, timeout_ms: int | None = None) -> "WaitUntilVisible":
        # DSL-ish helper: WaitUntilVisible.for_(SauceDemo.LOGIN_BUTTON)
        return WaitUntilVisible(target, timeout_ms)

    def __repr__(self) -> str:
        return (
            f"WaitUntilVisible(target='{self.target.description}', "
            f"timeout_ms={self.timeout_ms if self.timeout_ms is not None else 'default'})"
        )

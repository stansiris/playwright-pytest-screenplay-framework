import os

from screenplay_core.core.actor import Actor
from screenplay_core.core.interaction import Interaction
from screenplay_core.core.target import Target

DEFAULT_TIMEOUT_MS = 5000


def _default_timeout_ms_from_env() -> int:
    raw = os.getenv("SCREENPLAY_DEFAULT_TIMEOUT_MS")
    if raw is None:
        # Compatibility for existing project-level setting.
        raw = os.getenv("DEFAULT_TIMEOUT_MS")
    if raw is None:
        return DEFAULT_TIMEOUT_MS
    try:
        value = int(raw.strip())
    except ValueError as exc:
        raise ValueError(
            "Invalid default timeout. Set SCREENPLAY_DEFAULT_TIMEOUT_MS "
            "(or DEFAULT_TIMEOUT_MS) to an integer >= 1."
        ) from exc
    if value < 1:
        raise ValueError(
            "Invalid default timeout. Set SCREENPLAY_DEFAULT_TIMEOUT_MS "
            "(or DEFAULT_TIMEOUT_MS) to an integer >= 1."
        )
    return value


class WaitUntilVisible(Interaction):
    """Interaction: wait until a target is visible."""

    def __init__(self, target: Target, timeout_ms: int | None = None):
        self.target = target
        self.timeout_ms = _default_timeout_ms_from_env() if timeout_ms is None else timeout_ms

    def perform_as(self, actor: Actor) -> None:
        self.target.resolve_for(actor).wait_for(state="visible", timeout=self.timeout_ms)

    @staticmethod
    def for_(target: Target, timeout_ms: int | None = None) -> "WaitUntilVisible":
        # DSL-ish helper: WaitUntilVisible.for_(SauceDemo.LOGIN_BUTTON)
        return WaitUntilVisible(target, timeout_ms)

    def __repr__(self) -> str:
        return (
            f"WaitUntilVisible(target='{self.target.description}', "
            f"timeout_ms={self.timeout_ms})"
        )

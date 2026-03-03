from typing import TYPE_CHECKING

from screenplay_core.abilities.browse_the_web import BrowseTheWeb

if TYPE_CHECKING:
    from screenplay_core.core.actor import Actor

DEFAULT_TIMEOUT_MS = 5000


def validate_timeout_ms(timeout_ms: int) -> int:
    if timeout_ms < 1:
        raise ValueError("Timeout must be an integer >= 1.")
    return timeout_ms


def resolve_timeout_ms(actor: "Actor", timeout_ms: int | None) -> int:
    if timeout_ms is not None:
        return validate_timeout_ms(timeout_ms)

    browse = actor.ability_to(BrowseTheWeb)
    default_timeout_ms = getattr(browse, "default_timeout_ms", DEFAULT_TIMEOUT_MS)
    return validate_timeout_ms(default_timeout_ms)

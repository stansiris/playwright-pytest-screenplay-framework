import pytest

from screenplay_core.core.actor import Actor, AmbiguousAbilityError
from screenplay_core.core.task import Task
from screenplay_core.playwright.ensure import Ensure
from screenplay_core.playwright.interactions.click import Click
from screenplay_core.playwright.target import Target


class NoOpTask(Task):
    def perform_as(self, actor) -> None:  # noqa: ANN001
        return None


class _BaseAbility:
    pass


class _DerivedAbility(_BaseAbility):
    pass


class _AnotherDerivedAbility(_BaseAbility):
    pass


def _dummy_target() -> Target:
    return Target("dummy", lambda page: page)


def test_attempts_to_rejects_direct_interaction() -> None:
    """Verify that passing a raw Interaction to attempts_to() raises TypeError."""
    actor = Actor("Customer")

    with pytest.raises(TypeError, match="accepts Task/Consequence only"):
        actor.attempts_to(Click(_dummy_target()))


def test_attempts_to_accepts_task() -> None:
    """Verify that a valid Task is accepted by attempts_to() without error."""
    actor = Actor("Customer")
    actor.attempts_to(NoOpTask())


def test_attempts_to_accepts_ensure_consequence() -> None:
    """Verify Ensure consequence is accepted by attempts_to() and fails only on missing ability."""
    actor = Actor("Customer")

    with pytest.raises(Exception, match="does not have ability BrowseTheWeb"):
        actor.attempts_to(Ensure.that(_dummy_target()).to_be_visible())


def test_ability_to_resolves_exact_class() -> None:
    """Verify ability_to() returns the exact registered ability when queried by its own class."""
    actor = Actor("Customer")
    ability = _DerivedAbility()
    actor.can(ability)

    assert actor.ability_to(_DerivedAbility) is ability


def test_ability_to_resolves_base_class_via_isinstance() -> None:
    """Verify ability_to() resolves a derived ability when queried by its base class."""
    actor = Actor("Customer")
    ability = _DerivedAbility()
    actor.can(ability)

    assert actor.ability_to(_BaseAbility) is ability


def test_ability_to_raises_on_ambiguous_base_class_lookup() -> None:
    """Verify ability_to() raises AmbiguousAbilityError when two abilities share a base class."""
    actor = Actor("Customer")
    first = _DerivedAbility()
    second = _AnotherDerivedAbility()
    actor.can(first).can(second)

    with pytest.raises(AmbiguousAbilityError, match="multiple abilities compatible"):
        actor.ability_to(_BaseAbility)


def test_ability_to_prefers_exact_lookup_when_base_contract_is_ambiguous() -> None:
    """Verify exact class lookup takes precedence over ambiguous base-class resolution."""
    actor = Actor("Customer")
    first = _DerivedAbility()
    second = _AnotherDerivedAbility()
    actor.can(first).can(second)

    assert actor.ability_to(_DerivedAbility) is first

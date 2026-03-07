import pytest

from screenplay_core.consequences.ensure import Ensure
from screenplay_core.core.actor import Actor
from screenplay_core.core.target import Target
from screenplay_core.core.task import Task
from screenplay_core.interactions.click import Click


class NoOpTask(Task):
    def perform_as(self, actor) -> None:  # noqa: ANN001
        return None


def _dummy_target() -> Target:
    return Target("dummy", lambda page: page)


def test_attempts_to_rejects_direct_interaction() -> None:
    actor = Actor("Customer")

    with pytest.raises(TypeError, match="accepts Task/Consequence only"):
        actor.attempts_to(Click(_dummy_target()))


def test_attempts_to_accepts_task() -> None:
    actor = Actor("Customer")
    actor.attempts_to(NoOpTask())


def test_attempts_to_accepts_ensure_consequence() -> None:
    actor = Actor("Customer")

    with pytest.raises(Exception, match="does not have ability BrowseTheWeb"):
        actor.attempts_to(Ensure.that(_dummy_target()).to_be_visible())

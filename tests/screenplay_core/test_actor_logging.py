import logging

import pytest
from screenplay_core.core.actor import Actor
from screenplay_core.core.question import Question
from screenplay_core.core.task import Task
from screenplay_core.playwright.ensure import Ensure
from screenplay_core.playwright.interactions.click import Click
from screenplay_core.playwright.target import Target


class NoOpTask(Task):
    def perform_as(self, actor) -> None:  # noqa: ANN001
        return None


class FailingTask(Task):
    def perform_as(self, actor) -> None:  # noqa: ANN001
        raise RuntimeError("boom")


class StaticQuestion(Question):
    def answered_by(self, actor):  # noqa: ANN001
        return "ready"


class FailingQuestion(Question):
    def answered_by(self, actor):  # noqa: ANN001
        raise RuntimeError("no answer")


def _dummy_target() -> Target:
    return Target("Error message", lambda page: page)


def test_actor_logs_activity_start_and_end(caplog) -> None:
    """Verify activity logs stay simple and readable."""
    actor = Actor("Customer")

    with caplog.at_level(logging.INFO):
        actor.attempts_to(NoOpTask())

    assert "Customer starts NoOpTask()" in caplog.text
    assert "Customer ends NoOpTask()" in caplog.text


def test_actor_logs_activity_failure(caplog) -> None:
    """Verify failed activities log duration and the exception message."""
    actor = Actor("Customer")

    with caplog.at_level(logging.INFO):
        with pytest.raises(RuntimeError, match="boom"):
            actor.attempts_to(FailingTask())

    assert "Customer starts FailingTask()" in caplog.text
    assert "Customer failed FailingTask() after" in caplog.text
    assert ": boom" in caplog.text


def test_actor_logs_interaction_using_repr(caplog) -> None:
    """Verify interactions use their object repr in the log output."""
    actor = Actor("Customer")

    with caplog.at_level(logging.INFO):
        with pytest.raises(Exception, match="does not have ability BrowseTheWeb"):
            actor._attempts_to_interactions(Click(_dummy_target()))

    assert "Customer starts Click(target='Error message')" in caplog.text
    assert "Customer failed Click(target='Error message') after" in caplog.text


def test_actor_logs_ensure_using_readable_repr(caplog) -> None:
    """Verify Ensure logs use the framework's default repr output."""
    actor = Actor("Customer")

    with caplog.at_level(logging.INFO):
        with pytest.raises(Exception, match="does not have ability BrowseTheWeb"):
            actor.attempts_to(Ensure.that(_dummy_target()).to_have_text("Epic sadface"))

    assert (
        "Customer starts Ensure(target='Error message', assertion='to_have_text', "
        "args=('Epic sadface',))"
    ) in caplog.text


def test_actor_logs_question_start_and_answer(caplog) -> None:
    """Verify question logs use asks/got phrasing and preserve the answer."""
    actor = Actor("Customer")

    with caplog.at_level(logging.INFO):
        answer = actor.asks_for(StaticQuestion())

    assert answer == "ready"
    assert "Customer asks StaticQuestion()" in caplog.text
    assert "Customer got StaticQuestion() -> 'ready'" in caplog.text


def test_actor_logs_question_failure(caplog) -> None:
    """Verify failed questions log the question name and exception."""
    actor = Actor("Customer")

    with caplog.at_level(logging.INFO):
        with pytest.raises(RuntimeError, match="no answer"):
            actor.asks_for(FailingQuestion())

    assert "Customer asks FailingQuestion()" in caplog.text
    assert "Customer failed FailingQuestion() after" in caplog.text
    assert ": no answer" in caplog.text

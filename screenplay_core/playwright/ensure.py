"""
Screenplay-style assertion wrapper around Playwright's expect() API.

This module implements a thin DSL that allows Playwright locator assertions
to be used as Screenplay Consequences.

Example:

    actor.attempts_to(
        Ensure.that(LoginPage.ERROR_MESSAGE).to_be_visible()
    )

Design overview
---------------

Playwright assertions normally look like:

    expect(locator).to_be_visible()

In the Screenplay pattern, test behavior is expressed through activities
executed by an Actor. Assertions therefore need to be represented as
Screenplay objects that the actor can perform.

This module bridges the two models by dynamically forwarding Playwright
assertion methods into Screenplay Consequences.

Flow of execution:

    Ensure.that(Target).to_be_visible()
        ↓
    _EnsureTargetBuilder.__getattr__()
        ↓
    _EnsureCall created
        ↓
    actor.attempts_to(...)
        ↓
    _EnsureCall.perform_as(actor)
        ↓
    expect(locator).to_be_visible()

This design has several advantages:

• keeps Playwright assertions fully available
• avoids writing wrappers for every assertion method
• preserves Screenplay semantics (Actor performs Consequences)
• keeps the DSL clean and expressive

Type casting to LocatorAssertions is used to enable IDE auto-completion
for Playwright assertion methods while still using dynamic forwarding
internally.
"""

from __future__ import annotations

# typing utilities used for type hints and IDE support
from typing import Any, cast

# Playwright assertion factory and assertion interface
from playwright.sync_api import LocatorAssertions, expect

# Screenplay core abstractions
from screenplay_core.core.actor import Actor
from screenplay_core.core.consequence import Consequence
from screenplay_core.playwright.target import Target


class Ensure:
    """
    Entry point for Screenplay-style assertions.

    Example usage in tests:

        actor.attempts_to(
            Ensure.that(LoginPage.ERROR_MESSAGE).to_be_visible()
        )

    The `that()` method returns an object that *behaves like*
    Playwright's LocatorAssertions for IDE auto-completion, but
    actually produces a Screenplay `Consequence` that the actor
    can execute.
    """

    @staticmethod
    def that(target: Target) -> LocatorAssertions:
        """
        Start building an assertion against a Target.

        We return a `_EnsureTargetBuilder`, but cast it to
        `LocatorAssertions` so IDEs can offer auto-completion
        for Playwright assertion methods like:

            to_be_visible()
            to_have_text()
            to_have_count()

        At runtime the builder dynamically forwards the call.
        """
        return cast(LocatorAssertions, _EnsureTargetBuilder(target))


class _EnsureTargetBuilder:
    """
    Internal helper that dynamically forwards Playwright assertion
    method calls into Screenplay `Consequence` objects.

    This class implements a dynamic DSL:

        Ensure.that(Target).to_be_visible()

    `to_be_visible` is not actually defined here — Python will call
    `__getattr__` to handle it dynamically.
    """

    def __init__(self, target: Target):
        # Target represents a UI element abstraction
        self.target = target

    def __repr__(self) -> str:
        return f"Ensure.that('{self.target.description}')"

    def __getattr__(self, method_name: str):
        """
        Called by Python when an attribute does not exist.

        Example:

            Ensure.that(Target).to_be_visible()

        Python tries to find `to_be_visible` on this object.
        Since it does not exist, Python calls:

            __getattr__("to_be_visible")

        We then return a wrapper that converts this into a
        Screenplay Consequence.
        """

        def wrapper(*args: Any, **kwargs: Any) -> Consequence:
            """
            The wrapper captures the assertion name and arguments
            and converts them into a `_EnsureCall`.

            Example:

                Ensure.that(Target).to_have_text("Products")

            becomes:

                _EnsureCall(
                    target=Target,
                    method_name="to_have_text",
                    args=("Products",),
                    kwargs={}
                )
            """
            return _EnsureCall(self.target, method_name, args, kwargs)

        return wrapper


class _EnsureCall(Consequence):
    """
    Concrete Screenplay Consequence representing a Playwright assertion.

    The actor executes this object when `attempts_to()` runs.

    Example:

        actor.attempts_to(
            Ensure.that(Target).to_be_visible()
        )

    During execution this will call:

        expect(locator).to_be_visible()
    """

    def __init__(
        self,
        target: Target,
        method_name: str,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
    ):
        self.target = target
        self.method_name = method_name
        self.args = args
        self.kwargs = kwargs

    def perform_as(self, actor: Actor) -> None:
        """
        Execute the assertion in the context of the actor.

        Steps performed here:

        1. Resolve the Target into a Playwright Locator
        2. Create a Playwright assertion object using expect(locator)
        3. Look up the requested assertion method dynamically
        4. Execute the assertion
        """

        # Convert Target abstraction into a Playwright Locator
        locator = self.target.resolve_for(actor)

        # Playwright assertion factory
        assertion = expect(locator)

        # Look up the assertion method dynamically
        method = getattr(assertion, self.method_name, None)

        if method is None:
            raise AttributeError(
                f"Playwright expect(locator) has no assertion '{self.method_name}'"
            )

        # Execute the assertion
        method(*self.args, **self.kwargs)

    def __repr__(self) -> str:
        """
        String representation used for debugging and test logs.

        Example output:

            Ensure(target='inventory container', assertion='to_be_visible')
        """

        parts = [
            f"target='{self.target.description}'",
            f"assertion='{self.method_name}'",
        ]

        if self.args:
            parts.append(f"args={self.args!r}")

        if self.kwargs:
            parts.append(f"kwargs={self.kwargs!r}")

        return f"Ensure({', '.join(parts)})"

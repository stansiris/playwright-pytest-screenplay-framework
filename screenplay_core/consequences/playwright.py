from playwright.sync_api import expect

from screenplay_core.core.consequence import Consequence
from screenplay_core.core.target import Target


class ExpectTarget(Consequence):
    def __init__(self, target: Target, assertion: str, *args, **kwargs):
        self.target = target
        self.assertion = assertion
        self.args = args
        self.kwargs = kwargs

    def check_as(self, actor) -> None:
        locator_assert = expect(self.target.resolve_for(actor))
        getattr(locator_assert, self.assertion)(*self.args, **self.kwargs)

    def __repr__(self) -> str:
        return (
            f"ExpectTarget(target='{self.target.description}', "
            f"assertion='{self.assertion}', args={self.args}, kwargs={self.kwargs})"
        )


def expect_target(target: Target, assertion: str, *args, **kwargs) -> Consequence:
    return ExpectTarget(target, assertion, *args, **kwargs)

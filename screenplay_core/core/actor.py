import logging
import time

from playwright.sync_api import LocatorAssertions, expect

from screenplay_core.core.activity import Activity
from screenplay_core.core.question import Question
from screenplay_core.core.target import Target

logger = logging.getLogger(__name__)


class Actor:
    def __init__(self, name: str):
        self.name = name
        self._abilities = {}

    def can(self, ability) -> "Actor":
        self._abilities[ability.__class__] = ability
        return self

    def ability_to(self, ability_class):
        if ability_class not in self._abilities:
            raise Exception(f"{self.name} does not have ability {ability_class.__name__}.")
        return self._abilities[ability_class]

    def attempts_to(self, *activities: Activity) -> None:
        for activity in activities:
            activity_name = activity.__class__.__name__
            logger.info("%s performs %s %s", self.name, activity_name, _safe_repr(activity))

            start = time.perf_counter()
            try:
                activity.perform_as(self)
            except Exception:
                logger.exception(
                    "%s FAILED %s after %.0f ms",
                    self.name,
                    activity_name,
                    _elapsed_ms(start),
                )
                raise

            logger.info("%s DONE %s (%.0f ms)", self.name, activity_name, _elapsed_ms(start))

    def asks_for(self, question: Question):
        q_name = question.__class__.__name__
        logger.info("%s asks %s %s", self.name, q_name, _safe_repr(question))
        start = time.perf_counter()
        try:
            answer = question.answered_by(self)
        except Exception:
            logger.exception("%s FAILED %s after %.0f ms", self.name, q_name, _elapsed_ms(start))
            raise

        logger.info("%s got %s -> %r (%.0f ms)", self.name, q_name, answer, _elapsed_ms(start))
        return answer

    def expect(self, target: Target) -> LocatorAssertions:
        return expect(target.resolve_for(self))


def _safe_repr(obj) -> str:
    try:
        return repr(obj)
    except Exception:
        return f"<{obj.__class__.__name__}>"


def _elapsed_ms(start: float) -> float:
    return (time.perf_counter() - start) * 1000

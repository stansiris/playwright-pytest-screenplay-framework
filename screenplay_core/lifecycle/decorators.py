import inspect
import logging
import time
from functools import wraps

from screenplay_core.core.activity import Activity
from screenplay_core.core.question import Question
from screenplay_core.core.task import Task

logger = logging.getLogger(__name__)


def log_screenplay_step(func):
    """Log Screenplay Activity/Question execution around an Actor method call."""
    signature = inspect.signature(func, eval_str=False)

    @wraps(func)
    def wrapper(*args, **kwargs):
        bound = signature.bind_partial(*args, **kwargs)
        arguments = list(bound.arguments.values())
        if len(arguments) < 2:
            return func(*args, **kwargs)

        self = arguments[0]
        screenplay_obj = arguments[1]
        if not isinstance(screenplay_obj, (Activity, Question)):
            return func(*args, **kwargs)

        label = _describe_screenplay_object(screenplay_obj)
        start = time.perf_counter()

        if isinstance(screenplay_obj, Question):
            logger.info("%s asks %s", self.name, label)
        elif isinstance(screenplay_obj, Task):
            logger.info("%s performs %s", self.name, label)
        else:
            logger.info("%s starts %s", self.name, label)

        try:
            result = func(*args, **kwargs)
        except Exception as exc:
            logger.exception(
                "%s failed %s after %.0f ms: %s",
                self.name, label,
                _elapsed_ms(start),
                exc)
            raise

        if isinstance(screenplay_obj, Question):
            logger.info("%s got %s (%.0f ms)", self.name, label, _elapsed_ms(start))
        elif isinstance(screenplay_obj, Task):
            logger.info("%s performed %s (%.0f ms)", self.name, label, _elapsed_ms(start))
        else:
            logger.info("%s ends %s (%.0f ms)", self.name, label, _elapsed_ms(start))

        return result

    return wrapper


def _describe_screenplay_object(obj) -> str:
    """Return a human-readable description without leaking default object reprs."""
    if type(obj).__repr__ is object.__repr__:
        return obj.__class__.__name__

    try:
        return repr(obj)
    except Exception:
        return obj.__class__.__name__


def _elapsed_ms(start: float) -> float:
    """Compute elapsed milliseconds from a perf_counter start value."""
    return (time.perf_counter() - start) * 1000

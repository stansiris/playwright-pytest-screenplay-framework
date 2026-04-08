import inspect
from functools import wraps
import logging
import time

from screenplay_core.core.activity import Activity
from screenplay_core.core.question import Question

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
        is_question = isinstance(screenplay_obj, Question)
        start = time.perf_counter()

        logger.info("%s: %s %s %s", screenplay_obj.__class__.__base__.__name__, self.name, "asks" if is_question else "starts", label)
        try:
            result = func(*args, **kwargs)
        except Exception as exc:
            logger.error(
                "%s failed %s after %.0f ms: %s",
                self.name,
                label,
                _elapsed_ms(start),
                exc,
            )
            raise

        if is_question:
            logger.info("%s got %s -> %r (%.0f ms)", self.name, label, result, _elapsed_ms(start))
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

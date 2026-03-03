from screenplay_core.core.activity import Activity


class Task(Activity):
    """Base class for higher-level actions composed of interactions."""

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

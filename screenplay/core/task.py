class Task:
    """Base class for higher-level actions composed of interactions."""

    def perform_as(self, actor):
        raise NotImplementedError("Tasks must implement perform_as(actor).")

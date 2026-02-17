class Interaction:
    """Base class for low-level actions."""

    def perform_as(self, actor):
        raise NotImplementedError("Interactions must implement perform_as(actor).")

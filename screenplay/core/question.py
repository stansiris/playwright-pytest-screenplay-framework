class Question:
    """Base class for queries about the system under test."""

    def answered_by(self, actor):
        raise NotImplementedError("Questions must implement answered_by(actor).")

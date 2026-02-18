from screenplay.core.interaction import Interaction
from screenplay.core.target import Target


class Click(Interaction):

    def __init__(self, target: Target):
        self.target = target

    def perform_as(self, actor):
        self.target.resolve_for(actor).click()

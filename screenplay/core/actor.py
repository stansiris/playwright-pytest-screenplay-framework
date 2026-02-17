class Actor:

    def __init__(self, name: str):
        self.name = name
        self._abilities = {}

    def can(self, ability):
        self._abilities[ability.__class__] = ability
        return self

    def ability_to(self, ability_class):
        if ability_class not in self._abilities:
            raise Exception(
                f"{self.name} does not have ability {ability_class.__name__}."
            )
        return self._abilities[ability_class]

    def attempts_to(self, *activities):
        for activity in activities:
            activity.perform_as(self)

    def asks_for(self, question):
        return question.answered_by(self)

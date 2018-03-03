from . import models, base

class Event(base.BaseLogic):

    def _to_dict(self):
        d = {
            "value": self.value,
        }
        return d


class DebitEvent(Event, models.DebitEventModel, models.Base):
    pass

class CreditEvent(Event, models.CreditEventModel, models.Base):
    pass

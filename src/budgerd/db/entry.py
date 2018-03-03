from . import models, base
from . import event

class Entry(models.EntryModel, models.Base, base.BaseLogic):

    def basic_dict(self):
        d = {
            "date": self.date.isoformat(),
            "description": self.description,
            "denomination": "euro",
        }
        return d

    def _to_dict(self):
        d = self.basic_dict()
        d["debits"] = [d.to_dict() for d in self.debits]
        d["credits"] = [c.to_dict() for c in self.credits]
        return d

    def add_events(self, events):
        credits = [e for e in events if isinstance(e, event.DebitEvent)]
        credit_sum = sum([e.value for e in credits])
        debits = [e for e in events if isinstance(e, event.CreditEvent)]
        debit_sum = sum([e.value for e in debits])

        if credit_sum != debit_sum:
            raise ValueError("Credits not equal to Debits")

        for e in credits:
            self.credits.append(e)

        for e in debits:
            self.debits.append(e)

#from models import Base, AccountModel
from . import models, base

ASSETS_ACCOUNT_TYPE = "assets"
EXPENSES_ACCOUNT_TYPE = "expenses"
LIABILITIES_ACCOUNT_TYPE = "liabilities"
EQUITIES_ACCOUNT_TYPE = "equities"
REVENUES_ACCOUNT_TYPE = "revenues"

ACCOUNT_TYPES = [
    ASSETS_ACCOUNT_TYPE,
    EXPENSES_ACCOUNT_TYPE,
    LIABILITIES_ACCOUNT_TYPE,
    EQUITIES_ACCOUNT_TYPE,
    REVENUES_ACCOUNT_TYPE,
]

DEBITED_TYPES = [
    ASSETS_ACCOUNT_TYPE,
    EXPENSES_ACCOUNT_TYPE,
]

class Account(models.AccountModel, models.Base, base.BaseLogic):

    def _summarize_entry(self, entry):
        summary = entry.basic_dict()
        debits = [d.value for d in entry.debits if d.account == self]
        debits_sum = sum(debits)
        credits = [c.value for c in entry.credits if c.account == self]
        credits_sum = sum(credits)
        if self.type in ["assets", "expenses"]:
            value = debits_sum - credits_sum
        else:
            value = credits_sum - debits_sum
        summary["value"] = value
        return summary

    def _to_dict(self, summarized=True):
        if summarized:
            entries = [self._summarize_entry(e) for e in self.entries]
        else:
            entries = [e.to_dict() for e in self.entries]
        d = {
            "name": self.name,
            "type": self.type,
            "entries": entries,
        }
        return d

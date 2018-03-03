from . import models, base

class User(models.UserModel, models.Base, base.BaseLogic):

    def _to_dict(self):
        d = {
            "username": self.name,
        }
        return d

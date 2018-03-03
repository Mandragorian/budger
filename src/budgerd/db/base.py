import uuid

from sqlalchemy import Column

from . import types

class BaseModel(object):
    uuid = Column(types.GUID(), default=lambda: str(uuid.uuid4()))

class BaseLogic(object):

    def to_dict(self, *args, **kwargs):
        d = {
            "uuid": self.uuid,
        }
        d.update(self._to_dict(*args, **kwargs))
        return d

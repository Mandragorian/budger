from sqlalchemy import create_engine
from . import models
from .entry import Entry
from .event import DebitEvent, CreditEvent
from .user import User
from .account import Account

engine = create_engine('sqlite:///sqlalchemy_example.db')
models.Base.metadata.create_all(engine)

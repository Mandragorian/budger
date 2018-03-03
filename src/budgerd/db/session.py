from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from . import models


def get_session(db_str):
    engine = create_engine(db_str)
    models.Base.metadata.bind = engine
    DBSession = sessionmaker()
    DBSession.bind = engine
    session = DBSession()
    return session

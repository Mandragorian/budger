import os
import sys
import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Table
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import relationship

from . import base

Base = declarative_base()


entry_account_association = Table('entry_account_assoc', Base.metadata,
    Column('account_id', Integer, ForeignKey('account.id')),
    Column('entry_id', Integer, ForeignKey('entry.id'))
)


class AccountingEventModel(base.BaseModel):

    id = Column(Integer, primary_key=True)
    value = Column(Integer, default=0)

    @declared_attr
    def entry_id(self):
        return Column(Integer, ForeignKey("entry.id"))

    @declared_attr
    def account_id(self):
        return Column(Integer, ForeignKey("account.id"))


class DebitEventModel(AccountingEventModel):
    __tablename__ = "debit_event"

    #account = relationship("Account", secondary=debit_account_association,
    #                       backref="debits")
    @declared_attr
    def entry(self):
        return relationship("Entry", back_populates="debits")

    @declared_attr
    def account(self):
        return relationship("Account", back_populates="debits")


class CreditEventModel(AccountingEventModel):
    __tablename__ = "credit_event"

    #account = relationship("Account", secondary=credit_account_association,
    #                       backref="credits")

    @declared_attr
    def entry(self):
        return relationship("Entry", back_populates="credits")

    @declared_attr
    def account(self):
        return relationship("Account", back_populates="credits")


class AccountModel(base.BaseModel):
    __tablename__ = 'account'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    type = Column(String(25), nullable=False)

    @declared_attr
    def user_id(self):
        return Column(Integer, ForeignKey("user.id"))

    @declared_attr
    def debits(self):
        return relationship("DebitEvent", back_populates="account")

    @declared_attr
    def credits(self):
        return relationship("CreditEvent", back_populates="account")


class EntryModel(base.BaseModel):
    __tablename__ = 'entry'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.datetime.now)
    description = Column(String(250))

    @declared_attr
    def debits(self):
        return relationship("DebitEvent", back_populates="entry")

    @declared_attr
    def credits(self):
        return relationship("CreditEvent", back_populates="entry")

    @declared_attr
    def accounts(self):
        return relationship("Account", secondary=entry_account_association,
                           backref="entries")


class UserModel(base.BaseModel):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)

    @declared_attr
    def accounts(self):
        return relationship("Account", backref="user")


if __name__ == "__main__":
    # Create an engine that stores data in the local directory's
    # sqlalchemy_example.db file.
    engine = create_engine('sqlite:///sqlalchemy_example.db')

    # Create all tables in the engine. This is equivalent to "Create Table"
    # statements in raw SQL.
    Base.metadata.create_all(engine)

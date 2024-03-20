from sqlalchemy import Column, Integer, Unicode, UnicodeText, String

from database import Base

class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    username = Column(Unicode(20))
    balance = Column(Integer, nullable=True)

    def __init__(self, username, balance=0):
        self.username = username
        self.balance = balance


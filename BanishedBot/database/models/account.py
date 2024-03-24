from sqlalchemy import Column, Integer, Unicode, UnicodeText, String

from BanishedBot.database import Base
from BanishedBot.database import Session

from sqlalchemy.future import select


class Account(Base):
    __tablename__ = 'accounts'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    username = Column(Unicode(20))
    balance = Column(Integer, nullable=True)

    def __init__(self, username, balance=0):
        self.username = username
        self.balance = balance

    @classmethod
    async def get_all(cls, **kw):
        async with Session() as db:
            statement = select(Account)
            result = await db.execute(statement)
            return result
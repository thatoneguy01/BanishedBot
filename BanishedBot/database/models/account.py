from sqlalchemy import Column, Integer, Unicode, UnicodeText, String

from BanishedBot.database import Base
from BanishedBot.database import Session

from sqlalchemy.future import select
from sqlalchemy.orm import Session as saSession


class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True)
    username = Column(Unicode(20), nullable=False)
    balance = Column(Integer, nullable=False)

    def __init__(self, username, balance=0):
        self.username = username
        self.balance = balance

    @classmethod
    async def get_all(cls, **kw):
        db: saSession
        async with Session() as db:
            statement = select(Account)
            result = await db.execute(statement)
            list_result = [r[0] for r in result.all()]
            return list_result

    async def update(self, new_balance):
        db: saSession
        async with Session() as db:
            self.balance = new_balance
            await db.flush()
            await db.commit()

    @classmethod
    async def create(cls, username, balance):
        db: saSession
        async with Session() as db:
            db.add(Account(username, balance))
            await db.flush()
            await db.commit()

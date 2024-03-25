from sqlalchemy import Column, Integer, Unicode, UnicodeText, String

from BanishedBot.database import Base
from BanishedBot.database import Session

from sqlalchemy.future import select


class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    username = Column(Unicode(20), nullable=False)
    balance = Column(Integer, nullable=False)

    def __init__(self, username, balance=0):
        self.username = username
        self.balance = balance

    @classmethod
    async def get_all(cls, **kw):
        async with Session() as db:
            statement = select(Account)
            result = await db.execute(statement)
            return result
        
    async def update(self, new_balance):
        async with Session() as db:
            self.balance = new_balance
            print(f"session.dirty: {str(db.dirty)}")
            await db.flush()
            await db.commit()

    @classmethod
    async def create(cls, username, balance):
        async with Session() as db:
            db.add(Account(username, balance))
            await db.flush()
            await db.commit()
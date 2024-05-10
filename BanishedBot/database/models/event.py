from BanishedBot.database import Base
from BanishedBot.database import Session

from sqlalchemy import Column, Integer, UnicodeText, Boolean, DateTime
from sqlalchemy import select, delete
from sqlalchemy.orm import Session as saSession


class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(UnicodeText, nullable=False)
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    do_remind = Column(Boolean, default=False)

    def __init__(self, name, start_time=None, end_time=None, do_remind=False):
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.do_remind = do_remind

    @classmethod
    async def event_by_name(cls, name):
        db: saSession
        async with Session() as db:
            q = select(Event).where(Event.name == name)
            result = await db.execute(q)
            res = result.first()
            if res is not None:
                return res[0]
            else:
                return None

    @classmethod
    async def create(cls, name, start_time=None, end_time=None, do_remind=False):
        db: saSession
        async with Session() as db:
            e = Event(name, start_time, end_time, do_remind)
            db.add(e)
            await db.flush()
            await db.commit()

    @classmethod
    async def remove(cls, name):
        db: saSession
        async with Session() as db:
            q = delete(Event).where(Event.name == name)
            await db.execute(q)

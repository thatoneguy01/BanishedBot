from BanishedBot.database import Base
from BanishedBot.database import Session

from sqlalchemy import Column, Unicode, UnicodeText, Boolean, Date
from sqlalchemy import select, delete

class Event(Base):
    __tablename__ = 'events'
    id = Column(Unicode(24), primary_key=True)
    name = Column(UnicodeText, nullable=False)
    start_time = Column(Date, nullable=True)
    end_time = Column(Date, nullable=True)
    do_remind = Column(Boolean, default=False)

    def __init__(self, name, start_time=None, end_time=None, do_remind=False):
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.do_remind = do_remind
    
    @classmethod
    async def event_by_name(cls, name):
        async with Session() as db:
            q = select(Event).where(name=name)
            res = await db.execute(q).all()
            if len(res) > 0:
                return res[0][0]
            else:
                return None
            
    @classmethod
    async def create(cls, name, start_time=None, end_time=None, do_remind=False):
        async with Session() as db:
            Event(name, start_time, end_time, do_remind)
            db.flush()
            db.commit()

    @classmethod
    async def remove(cls, name):
        async with Session() as db:
            q = delete(Event).where(name=name)
            await db.execute(q)
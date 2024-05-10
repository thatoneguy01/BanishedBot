import json, random, datetime, time

from sqlalchemy import Column, Unicode, UnicodeText, Date
from sqlalchemy import update, select
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import Session as saSession

from BanishedBot.database import Base
from BanishedBot.database import Session
from BanishedBot.constant import SRC_DIR
from BanishedBot.utils import Json


class Trivia(Base):
    __tablename__ = 'trivia'
    id = Column(Unicode(24), primary_key=True)
    category = Column(Unicode(20), nullable=False)
    correct_answer = Column(UnicodeText, nullable=False)
    all_answers = Column(Json, nullable=False)
    question = Column(UnicodeText, nullable=False)
    tags = Column(Json, nullable=False)
    difficulty = Column(Unicode(6), nullable=False)
    used = Column(Date, nullable=True)

    def __init__(self, id_str, category, correct_answer, all_answers, question, tags, difficulty, used = False):
        self.id = id_str
        self.category = category
        self.correct_answer = correct_answer
        self.all_answers = all_answers
        self.question = question
        self.tags = tags
        self.difficulty = difficulty
        self.used = used

    @classmethod
    def from_json(clsm, tq):
        t = Trivia(id_str=tq["id"],
                    category=tq["category"],
                    correct_answer=tq["correctAnswer"],
                    all_answers=tq["incorrectAnswers"]+[tq["correctAnswer"]],
                    question=tq["question"]["text"],
                    tags=tq["tags"],
                    difficulty=tq["difficulty"])
        return t
    
    @classmethod
    async def get_current(cls):
        db: saSession
        async with Session() as db:
            query = select(Trivia).where(Trivia.used==datetime.date.fromtimestamp(time.time()-3*60*60))
            result = await db.execute(query)
            row = result.first()
            if row is None:
                return await Trivia.get_unused_or_reset()
            else:
                return row[0]
            
    @classmethod
    async def reset_used(cls, db: saSession):
        q = update(Trivia).values(used=None)
        await db.execute(q)
        db.flush()
        db.commit()
    
    @classmethod
    async def get_unused_or_reset(cls):
        db: saSession
        async with Session() as db:
            unused_q = select(Trivia).where(Trivia.used==None).order_by(func.random()).limit(5)
            result = await db.execute(unused_q)
            unused_rows = result.all()
            if len(unused_rows)==0:
                Trivia.reset_used(db)
                result = await db.execute(unused_q)
                unused_rows = result.all()
            q = [o[0] for o in unused_rows][0]
            q.used = datetime.date.today()
            await db.flush()
            await db.commit()
            return q
    
    async def load_initial():
        db: saSession
        async with Session() as db:
            with open(f"{SRC_DIR}questions.json") as f:
                trivia_json = json.load(f)
            for tq in trivia_json:
                t = Trivia(id_str=tq["id"],
                            category=tq["category"],
                            correct_answer=tq["correctAnswer"],
                            all_answers=tq["incorrectAnswers"]+[tq["correctAnswer"]],
                            question=tq["question"]["text"],
                            tags=tq["tags"],
                            difficulty=tq["difficulty"])
                db.add(t)
            await db.flush()
            await db.commit()
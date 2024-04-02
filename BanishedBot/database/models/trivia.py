import json

from sqlalchemy import Column, Unicode, UnicodeText, Boolean

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
    used = Column(Boolean, nullable=False)

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
    
    async def load_initial():
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
from sqlalchemy import Column, Unicode
from sqlalchemy import ForeignKey
from sqlalchemy.future import select

from BanishedBot.database import Base
from BanishedBot.database import Session
from BanishedBot.constant import SRC_DIR
from BanishedBot.utils import Json
from trivia import Trivia

class TriviaStat(Base):
    __tablename__ = 'trivia_stat'
    question_id = Column(Unicode(24), ForeignKey(Trivia.id), primary_key=True)
    correct_answer = Column(Json, server_default=[], nullable=False)
    incorrect_answer = Column(Json, server_default=[], nullable=False)
    no_answer = Column(Json, server_default=[], nullable=False)

    def __init__(self, question_id, correct_answer=[], incorrect_answer=[], no_answer=[]):
        self.question_id = question_id
        self.correct_answer = correct_answer
        self.incorrect_answer = incorrect_answer
        self.no_answer = no_answer

    async def store_stats(self, question_id, correct=None, incorrect=None):
        async with Session() as db:
            s = select(TriviaStat).where(question_id=question_id)
            ts = db.execute(s).first()[0]
            if correct:
                ts.correct_answer.append(correct)
                ts.no_answer.remove(incorrect)
            ts.incorrect_answer.append(incorrect)
            ts.no_answer.remove(incorrect)

from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.quiz import Quiz


class QuizRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list(self) -> Sequence[Quiz]:
        stmt = select(Quiz)
        return self.session.scalars(stmt).all()

    def get(self, quiz_id: int) -> Quiz | None:
        return self.session.get(Quiz, quiz_id)

    def create(self, quiz: Quiz) -> Quiz:
        self.session.add(quiz)
        self.session.commit()
        self.session.refresh(quiz)
        return quiz

    def save(self, quiz: Quiz) -> Quiz:
        self.session.commit()
        self.session.refresh(quiz)
        return quiz

    def delete(self, quiz: Quiz) -> None:
        self.session.delete(quiz)
        self.session.commit()

from sqlalchemy import Boolean, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Quiz(Base):
    __tablename__ = "quizzes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_published: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    teacher_id: Mapped[int] = mapped_column(Integer, nullable=False)
    subject_id: Mapped[int | None] = mapped_column(Integer, nullable=True)

    @property
    def owner_id(self) -> int:
        """Псевдоним для teacher_id (владелец квиза)."""
        return self.teacher_id

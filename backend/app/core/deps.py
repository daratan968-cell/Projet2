from collections.abc import Callable, Generator

from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import SessionLocal
from app.models.user import User as UserModel
from app.repositories.quiz_repository import QuizRepository
from app.schemas.user import User
from app.services.quiz_service import QuizService


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_quiz_service(db: Session = Depends(get_db)) -> QuizService:
    repo = QuizRepository(db)
    return QuizService(repo)


def get_current_user(db: Session = Depends(get_db)) -> User:
    stmt = select(UserModel).where(UserModel.email == settings.demo_user_email)
    user_model = db.scalar(stmt)
    if user_model is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Демо-пайдаланушы табылмады: {settings.demo_user_email}",
        )
    return User.model_validate(user_model)


def require_role(*roles: str) -> Callable[[User], User]:
    def role_checker(user: User = Depends(get_current_user)) -> User:
        if user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Бұл әрекетке құқығыңыз жоқ. Қажетті рөл: {', '.join(roles)}",
            )
        return user

    return role_checker

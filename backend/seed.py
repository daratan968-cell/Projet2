import sys
from pathlib import Path

# Добавляем путь к backend в sys.path
backend_dir = Path(__file__).resolve().parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from sqlalchemy import select

from app.core.database import SessionLocal, engine
from app.models import Base
from app.models.quiz import Quiz
from app.models.user import User


def seed_data() -> None:
    print("Создание таблиц базы данных...")
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as session:
        # Проверяем и создаем демо-пользователей
        demo_users_data = [
            {
                "email": "teacher@demo.kz",
                "full_name": "Демо Оқытушы",
                "role": "teacher",
            },
            {
                "email": "student@demo.kz",
                "full_name": "Демо Студент",
                "role": "student",
            },
            {
                "email": "admin@demo.kz",
                "full_name": "Демо Әкімші",
                "role": "admin",
            },
        ]

        users_by_email: dict[str, User] = {}
        for user_data in demo_users_data:
            stmt = select(User).where(User.email == user_data["email"])
            existing_user = session.scalar(stmt)
            if existing_user is None:
                user = User(
                    email=user_data["email"],
                    full_name=user_data["full_name"],
                    role=user_data["role"],
                )
                session.add(user)
                session.flush()
                users_by_email[user.email] = user
                print(f"Создан пользователь: {user.email} (роль: {user.role})")
            else:
                users_by_email[existing_user.email] = existing_user
                print(f"Пользователь уже существует: {existing_user.email}")

        # Проверяем и создаем хотя бы один объект Quiz
        teacher = users_by_email["teacher@demo.kz"]
        stmt_quiz = select(Quiz).where(Quiz.teacher_id == teacher.id)
        existing_quiz = session.scalar(stmt_quiz)

        if existing_quiz is None:
            quiz = Quiz(
                title="Python негіздері бойынша демо-тест",
                description="Студенттерге арналған бастапқы тест",
                is_published=True,
                teacher_id=teacher.id,
            )
            session.add(quiz)
            session.commit()
            print(f"Создан демо-тест: '{quiz.title}' (ID: {quiz.id})")
        else:
            session.commit()
            print(f"Демо-тест уже существует: '{existing_quiz.title}' (ID: {existing_quiz.id})")

    print("Seed-данные успешно добавлены!")


if __name__ == "__main__":
    seed_data()

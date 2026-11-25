import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.deps import get_current_user, get_db
from app.main import app
from app.models import Base
from app.models.quiz import Quiz
from app.models.user import User

# Тестовая in-memory база данных SQLite
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=engine)
    with TestingSessionLocal() as session:
        # Добавляем тестовых пользователей
        teacher = User(id=1, email="teacher@demo.kz", full_name="Демо Оқытушы", role="teacher")
        student = User(id=2, email="student@demo.kz", full_name="Демо Студент", role="student")
        session.add_all([teacher, student])

        # Добавляем начальный квиз
        quiz = Quiz(
            id=1,
            title="Бастапқы тест",
            description="Тест сипаттамасы",
            is_published=True,
            teacher_id=1,
        )
        session.add(quiz)
        session.commit()

    yield

    Base.metadata.drop_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_list_quizzes():
    response = client.get("/api/quizzes")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["title"] == "Бастапқы тест"


def test_create_quiz_as_teacher():
    payload = {
        "title": "Жаңа тест тақырыбы",
        "description": "Жаңа тесттің толық сипаттамасы",
        "subject_id": None,
    }
    response = client.post("/api/quizzes", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["teacher_id"] == 1
    assert data["is_published"] is False


def test_create_quiz_forbidden_for_student():
    # Переопределяем пользователя на студента
    from app.schemas.user import User as UserSchema

    app.dependency_overrides[get_current_user] = lambda: UserSchema(
        id=2, email="student@demo.kz", full_name="Демо Студент", role="student"
    )

    payload = {
        "title": "Студент құрғысы келген тест",
        "description": "Студент құра алмайды",
    }
    response = client.post("/api/quizzes", json=payload)
    assert response.status_code == 403

    # Возвращаем стандартную зависимость
    del app.dependency_overrides[get_current_user]


def test_get_quiz_by_id():
    response = client.get("/api/quizzes/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Бастапқы тест"


def test_get_quiz_not_found():
    response = client.get("/api/quizzes/999")
    assert response.status_code == 404


def test_update_quiz():
    payload = {
        "title": "Жаңартылған тест тақырыбы",
        "is_published": True,
    }
    response = client.patch("/api/quizzes/1", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Жаңартылған тест тақырыбы"
    assert data["is_published"] is True


def test_delete_quiz():
    response = client.delete("/api/quizzes/1")
    assert response.status_code == 204

    # Проверяем, что тест удален
    get_res = client.get("/api/quizzes/1")
    assert get_res.status_code == 404

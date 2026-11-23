from app.core.exceptions import ForbiddenError, NotFoundError
from app.models.quiz import Quiz
from app.repositories.quiz_repository import QuizRepository
from app.schemas.quiz import QuizCreate, QuizForTeacher, QuizRead, QuizUpdate
from app.schemas.user import User


class QuizService:
    def __init__(self, repo: QuizRepository) -> None:
        self.repo = repo

    def _get(self, quiz_id: int) -> Quiz:
        quiz = self.repo.get(quiz_id)
        if quiz is None:
            raise NotFoundError(f"Тест табылмады: id={quiz_id}")
        return quiz

    def _get_own(self, quiz_id: int, user: User) -> Quiz:
        quiz = self._get(quiz_id)
        if quiz.owner_id != user.id and user.role != "admin":
            raise ForbiddenError("Бұл тест сіздікі емес")
        return quiz

    def list_quizzes(self) -> list[QuizRead]:
        quizzes = self.repo.list()
        return [QuizRead.model_validate(q) for q in quizzes]

    def get_quiz(self, quiz_id: int) -> QuizRead:
        quiz = self._get(quiz_id)
        return QuizRead.model_validate(quiz)

    def create_quiz(self, data: QuizCreate, user: User) -> QuizForTeacher:
        quiz = Quiz(
            title=data.title,
            description=data.description,
            subject_id=data.subject_id,
            teacher_id=user.id,
            is_published=False,
        )
        saved = self.repo.create(quiz)
        return QuizForTeacher.model_validate(saved)

    def update_quiz(
        self, quiz_id: int, data: QuizUpdate, user: User
    ) -> QuizForTeacher:
        quiz = self._get_own(quiz_id, user)
        changes = data.model_dump(exclude_unset=True, exclude_none=True)
        for field, value in changes.items():
            setattr(quiz, field, value)
        return QuizForTeacher.model_validate(self.repo.save(quiz))

    def delete_quiz(self, quiz_id: int, user: User) -> None:
        quiz = self._get_own(quiz_id, user)
        self.repo.delete(quiz)

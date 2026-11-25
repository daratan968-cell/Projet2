from fastapi import APIRouter, Depends, status

from app.core.deps import get_current_user, get_quiz_service, require_role
from app.schemas.quiz import QuizCreate, QuizForTeacher, QuizRead, QuizUpdate
from app.schemas.user import User
from app.services.quiz_service import QuizService

router = APIRouter(prefix="/api/quizzes", tags=["quizzes"])


@router.get(
    "",
    response_model=list[QuizRead],
    status_code=status.HTTP_200_OK,
    summary="Получить список всех тестов",
)
def list_quizzes(
    service: QuizService = Depends(get_quiz_service),
) -> list[QuizRead]:
    return service.list_quizzes()


@router.post(
    "",
    response_model=QuizForTeacher,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новый тест",
)
def create_quiz(
    data: QuizCreate,
    service: QuizService = Depends(get_quiz_service),
    current_user: User = Depends(require_role("teacher", "admin")),
) -> QuizForTeacher:
    return service.create_quiz(data=data, user=current_user)


@router.get(
    "/{quiz_id}",
    response_model=QuizRead,
    status_code=status.HTTP_200_OK,
    summary="Получить тест по ID",
)
def get_quiz(
    quiz_id: int,
    service: QuizService = Depends(get_quiz_service),
) -> QuizRead:
    return service.get_quiz(quiz_id=quiz_id)


@router.patch(
    "/{quiz_id}",
    response_model=QuizForTeacher,
    status_code=status.HTTP_200_OK,
    summary="Обновить тест по ID",
)
def update_quiz(
    quiz_id: int,
    data: QuizUpdate,
    service: QuizService = Depends(get_quiz_service),
    current_user: User = Depends(get_current_user),
) -> QuizForTeacher:
    return service.update_quiz(quiz_id=quiz_id, data=data, user=current_user)


@router.delete(
    "/{quiz_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить тест по ID",
)
def delete_quiz(
    quiz_id: int,
    service: QuizService = Depends(get_quiz_service),
    current_user: User = Depends(get_current_user),
) -> None:
    service.delete_quiz(quiz_id=quiz_id, user=current_user)

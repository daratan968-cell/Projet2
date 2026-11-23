from pydantic import BaseModel, ConfigDict, Field


class QuizCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=200, description="Название теста")
    description: str | None = Field(default=None, max_length=1000, description="Описание теста")
    subject_id: int | None = Field(default=None, description="ID предмета")


class QuizUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=200)
    description: str | None = Field(default=None, max_length=1000)
    is_published: bool | None = None
    subject_id: int | None = None


class QuizRead(BaseModel):
    id: int
    title: str
    description: str | None = None
    is_published: bool
    teacher_id: int
    subject_id: int | None = None

    model_config = ConfigDict(from_attributes=True)

from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    id: int
    email: str = ""
    full_name: str = ""
    role: str = "teacher"  # student | teacher | admin

    model_config = ConfigDict(from_attributes=True)

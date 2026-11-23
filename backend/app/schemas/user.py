from pydantic import BaseModel


class User(BaseModel):
    id: int
    email: str = ""
    full_name: str = ""
    role: str = "teacher"  # student | teacher | admin

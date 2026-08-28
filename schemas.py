from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class Task(BaseModel):
    task: str
    deadline: datetime | None = None


class UpdateTask(BaseModel):
    task: str | None = None
    deadline: datetime | None = None


class TaskResponse(BaseModel):
    id: int
    task: str
    deadline: datetime | None
    is_done: bool
    user_id: int

    model_config = {'from_attributes': True}


class RegisterUser(BaseModel):
    email: EmailStr
    username: str
    password: str = Field(min_length=8)


class LoginUser(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)

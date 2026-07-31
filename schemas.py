from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

class Task(BaseModel):
    task: str 
    deadline: datetime | None

class RegisterUser(BaseModel):
    email: EmailStr 
    username: str
    password: str = Field(min_length=8)

class LoginUser(BaseModel):
    email: EmailStr 
    password: str = Field(min_length=8)
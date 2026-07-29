from pydantic import BaseModel, EmailStr, Field


class RegisterUser(BaseModel):
    email: EmailStr 
    username: str
    password: str = Field(min_length=8)

class LoginUser(BaseModel):
    email: EmailStr 
    password: str = Field(min_length=8)
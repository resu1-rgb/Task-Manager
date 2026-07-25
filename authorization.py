from typing import Annotated

from authx import AuthX, AuthXConfig
from database import get_db
from fastapi import APIRouter, Depends, HTTPException
from models import Users
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

router = APIRouter()

config = AuthXConfig(
    JWT_SECRET_KEY="secret_key_very_long_and_secure_for_testing_only",
    JWT_TOKEN_LOCATION=["headers"],
    JWT_ACCESS_COOKIE_NAME="my_accsess_token",
)

authx = AuthX(config=config)
class UsersLoginScheme(BaseModel):
    email: EmailStr
    username: str
    password: str = Field(min_length=8)


@router.post("/register")
async def register(
    user: UsersLoginScheme,
    db: Annotated[Session, Depends(get_db)],
):
    db_user = Users(email=user.email, username=user.username, password=user.password)
    db.add(db_user)
    db.commit()
    return {"Database Added"}


@router.post("/login")
async def login(
    cred: UsersLoginScheme,
    db: Annotated[Session, Depends(get_db)],
):
    db_email = (
        db.query(Users)
        .filter(Users.email == cred.email, Users.password == cred.password)
        .first()
    )
    if db_email:
        token = authx.create_access_token(uid=cred.username)
        return {"token": token}
    raise HTTPException(status_code=401, detail="Incorrect password or username")

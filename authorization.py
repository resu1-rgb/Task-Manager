from typing import Annotated

from authx import AuthX, AuthXConfig
from database import get_db
from fastapi import APIRouter, Depends, HTTPException
from models import Users
from pwdlib import PasswordHash
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

password_hash = PasswordHash.recommended()
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
    db_user = Users(
        email=user.email,
        username=user.username,
        hash_password=password_hash.hash(user.password),
    )
    db.add(db_user)
    db.commit()
    return {"Database Added"}


@router.post("/login")
async def login(
    user: UsersLoginScheme,
    db: Annotated[Session, Depends(get_db)],
):
    db_user = (
        db.query(Users)
        .filter(Users.email == user.email).first())
    if db_user and password_hash.verify(user.password, db_user.hash_password):
        token = authx.create_access_token(uid=str(db_user.id))
        return {"token": token}
    raise HTTPException(status_code=401, detail="Incorrect password or username")

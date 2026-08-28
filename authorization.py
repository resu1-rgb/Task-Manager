from typing import Annotated
import os

from authx import AuthX, AuthXConfig
from database import get_db
from fastapi import APIRouter, Depends, HTTPException
from models import Users
from pwdlib import PasswordHash
from schemas import LoginUser, RegisterUser
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

password_hash = PasswordHash.recommended()
router = APIRouter()

config = AuthXConfig(
    JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY"),
    JWT_TOKEN_LOCATION=["headers"],
)

authx = AuthX(config=config)

@router.post("/register")
async def register(
    user: RegisterUser,
    db: Annotated[Session, Depends(get_db)],
):
    db_user = Users(
        email=user.email,
        username=user.username,
        hash_password=password_hash.hash(user.password),
    )
    db.add(db_user)

    try:
        db.commit()
        return {"message": "User registered successfully"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email or username already exists")


@router.post("/login")
async def login(
    user: LoginUser,
    db: Annotated[Session, Depends(get_db)],
):
    db_user = (
        db.query(Users)
        .filter(Users.email == user.email).first())
    if db_user and password_hash.verify(user.password, db_user.hash_password):
        token = authx.create_access_token(uid=str(db_user.id))
        return {"token": token}
    raise HTTPException(status_code=401, detail="Incorrect password or username")

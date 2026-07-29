from datetime import datetime

from database import Base
from fastapi import APIRouter
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

router = APIRouter()

class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    hash_password: Mapped[str] = mapped_column(nullable=False)


class Tasks(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    task: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    deadline: Mapped[str | None] = mapped_column(nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

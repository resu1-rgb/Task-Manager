from datetime import datetime
from typing import Annotated, Any

import uvicorn
from authorization import authx
from authorization import router as auth
from database import Base, engine, get_db
from fastapi import Depends, FastAPI, HTTPException
from models import Tasks, Users
from pydantic import BaseModel
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)

app = FastAPI()


class Task(BaseModel):
    task: str 
    deadline: datetime | None

app.include_router(auth)

@app.post("/add_tasks")
async def add_tasks(
    main: Task,
    db: Annotated[Session, Depends(get_db)],
    payload: Annotated[Any, Depends(authx.access_token_required)],
):
    username = payload.sub
    user = db.query(Users).filter(Users.username == username).first()
    deadline_str = main.deadline.strftime("%d-%m-%Y %H:%M") if main.deadline else None
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db_task = Tasks(task=main.task, deadline=deadline_str, user_id=user.id)
    db.add(db_task)
    db.commit()
    return {"message": "Task added"}


@app.get("/read_tasks_deadline")
async def read_tasks(
    db: Annotated[Session, Depends(get_db)],
    payload: Annotated[Any, Depends(authx.access_token_required)],
):
    username = payload.sub
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    currnet_tasks = db.query(Tasks).filter(Tasks.user_id == user.id).all()
    return currnet_tasks


@app.delete("/del_tasks/{user_id}")
async def delete_tasks(
    user_id: int,
    db: Annotated[Session, Depends(get_db)],
    payload: Annotated[Any, Depends(authx.access_token_required)],
):
    username = payload.sub
    user = db.query(Users).filter(Users.username == username).first()
    if user:
        del_tasks = db.query(Tasks).filter(Tasks.id == user_id).first()
        if not del_tasks:
            raise HTTPException(status_code=404, detail="Not found")
        db.delete(del_tasks)
        db.commit()
        return {"message": "Task deleted"}
    raise HTTPException(status_code=404, detail="User not found")


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, log_level="info", reload=True)

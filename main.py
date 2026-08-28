from typing import Annotated

import uvicorn
from authorization import authx, router as auth
from database import Base, engine, get_db
from fastapi import Depends, FastAPI, HTTPException
from models import Tasks, Users
from sqlalchemy.orm import Session
from schemas import Task, UpdateTask, TaskResponse

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth)

def get_current_user(
    db: Annotated[Session, Depends(get_db)],
    payload=Depends(authx.access_token_required)
):
    user = db.query(Users).filter(Users.id == int(payload.sub)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/add_tasks")
async def add_tasks(
    task: Task,
    db: Annotated[Session, Depends(get_db)],
    current_user: Users = Depends(get_current_user),
):
    db_task = Tasks(task=task.task, deadline=task.deadline, user_id=current_user.id)
    db.add(db_task)
    db.commit()
    return {"message": "Task added"}


@app.get("/read_tasks")
async def read_tasks(
    db: Annotated[Session, Depends(get_db)],
    current_user: Users = Depends(get_current_user),
):
    return db.query(Tasks).filter(Tasks.user_id == current_user.id).all()


@app.get("/read_tasks/{task_id}")
async def read_task_by_id(
    task_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Users = Depends(get_current_user),
):
    task = db.query(Tasks).filter(Tasks.id == task_id, Tasks.user_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.patch("/tasks/{task_id}/done")
async def mark_task_done(
    task_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Users = Depends(get_current_user),
):
    task = db.query(Tasks).filter(Tasks.id == task_id, Tasks.user_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.is_done = not task.is_done
    db.commit()
    return {"message": "Task updated", "is_done": task.is_done}


@app.patch("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    data: UpdateTask,
    db: Annotated[Session, Depends(get_db)],
    current_user: Users = Depends(get_current_user),
):
    task = db.query(Tasks).filter(Tasks.id == task_id, Tasks.user_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if data.task is not None:
        task.task = data.task
    if data.deadline is not None:
        task.deadline = data.deadline
    db.commit()
    return task


@app.delete("/del_tasks/{task_id}")
async def delete_task(
    task_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Users = Depends(get_current_user),
):
    task = db.query(Tasks).filter(Tasks.id == task_id, Tasks.user_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}


@app.get("/task_search")
async def task_search(
    q: str,
    db: Annotated[Session, Depends(get_db)],
    current_user: Users = Depends(get_current_user),
):
    return db.query(Tasks).filter(Tasks.task.ilike(f"%{q}%"), Tasks.user_id == current_user.id).all()


@app.get("/task_sort")
async def task_sort(
    db: Annotated[Session, Depends(get_db)],
    current_user: Users = Depends(get_current_user),
):
    return db.query(Tasks).filter(Tasks.user_id == current_user.id).order_by(Tasks.created_at).all()


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, log_level="info", reload=True)

from typing import Annotated

import uvicorn
from authorization import authx
from authorization import router as auth
from database import Base, engine, get_db
from fastapi import Depends, FastAPI, HTTPException
from models import Tasks, Users
from sqlalchemy.orm import Session
from schemas import Task

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth)

@app.post("/add_tasks")
async def add_tasks(
    main: Task,
    db: Annotated[Session, Depends(get_db)],
    payload: Annotated[Session, Depends(authx.access_token_required)],
):
    user_id = int(payload.sub)
    user = db.query(Users).filter(Users.id == user_id).first()
    deadline_str = main.deadline.strftime("%d-%m-%Y %H:%M") if main.deadline else None
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db_task = Tasks(task=main.task, deadline=deadline_str, user_id=user.id)
    db.add(db_task)
    db.commit()
    return {"message": "Task added"}


@app.get("/read_tasks")
async def read_tasks(
    db: Annotated[Session, Depends(get_db)],
    payload: Annotated[Session, Depends(authx.access_token_required)],
):
    user_id = int(payload.sub)
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    current_tasks = db.query(Tasks).filter(Tasks.user_id == user.id).all()
    return current_tasks


@app.delete("/del_tasks/{task_id}")
async def delete_tasks(
    task_id: int,
    db: Annotated[Session, Depends(get_db)],
    payload: Annotated [Session, Depends(authx.access_token_required)],
):
    user_id = int(payload.sub)
    user = db.query(Users).filter(Users.id == user_id).first()
    if user:
        del_tasks = db.query(Tasks).filter(Tasks.id == task_id, Tasks.user_id == user.id).first()
        if not del_tasks:
            raise HTTPException(status_code=404, detail="Not found")
        db.delete(del_tasks)
        db.commit()
        return {"message": "Task deleted"}
    raise HTTPException(status_code=404, detail="User not found")

@app.get('/read_tasks/{task_id}')
async def read_tasks(
    task_id: int,
    db: Annotated[Session, Depends(get_db)],
    payload: Annotated [Session, Depends(authx.access_token_required)]
):
    user_id = int(payload.sub)
    user = db.query(Users).filter(Users.id == user_id).first()
    if user:
        get_id = db.query(Tasks).filter(Tasks.id == task_id, Tasks.user_id == user.id).first()
        if not get_id:
          raise HTTPException(status_code=404, detail="Not found")
        return {'message': get_id}
    raise HTTPException(status_code=404, detail="User not found")

@app.get('/task_search')
async def task_search(
    q: str, 
    db: Annotated[Session, Depends(get_db)],
    payload: Annotated [Session, Depends(authx.access_token_required)]
):
    user_id = int(payload.sub)
    user = db.query(Users).filter(Users.id == user_id).first()
    if user:
        result = db.query(Tasks).filter(Tasks.task.ilike(f"%{q}%"), Tasks.user_id == user.id).all()
        return result
    raise HTTPException(status_code=404, detail='Task not found')

@app.get('/task_sort')
async def task_sort(
    db: Annotated[Session, Depends(get_db)],
    payload: Annotated [Session, Depends(authx.access_token_required)]
):
    user_id = int(payload.sub)
    user = db.query(Users).filter(Users.id == user_id).first()
    if user:
        result = db.query(Tasks).filter(Tasks.user_id == user.id).order_by(Tasks.created_at).all()
        return result
    raise HTTPException(status_code=404, detail="User not found")

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, log_level="info", reload=True)
    
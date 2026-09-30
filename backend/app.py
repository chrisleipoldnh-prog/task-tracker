from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import engine, get_db, test_connection
from models import Base, Task
from schemas import TaskCreate, TaskUpdate

app = FastAPI()

# Create database tables if they do not already exist
Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {"message": "Task Tracker API"}


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "connection": test_connection()
    }


# CREATE
@app.post("/tasks")
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db)
):
    new_task = Task(
        title=task.title
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


# READ ALL
@app.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.scalars(select(Task)).all()
    return tasks


# READ ONE
@app.get("/tasks/{task_id}")
def get_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = db.get(Task, task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


# UPDATE
@app.patch("/tasks/{task_id}")
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db)
):
    task = db.get(Task, task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if task_update.title is not None:
        task.title = task_update.title

    if task_update.completed is not None:
        task.completed = task_update.completed

    db.commit()
    db.refresh(task)

    return task


# DELETE
@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = db.get(Task, task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()

    return {"message": "Task deleted"}
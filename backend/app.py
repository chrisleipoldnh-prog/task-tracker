from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class TaskCreate(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None

class Task(BaseModel):
    id: int
    title: str
    completed: bool = False

tasks: list[Task] = []
next_id = 1


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/tasks")
def list_tasks() -> list[Task]:
    return tasks


@app.post("/tasks", status_code=201)
def create_task(body: TaskCreate) -> Task:
    global next_id
    title = body.title.strip()
    if not title:
        raise HTTPException(status_code=400, detail="title is required")

    task = Task(id=next_id, title=title)
    next_id += 1
    tasks.append(task)
    return task


@app.patch("/tasks/{task_id}")
def update_task(task_id: int, body: TaskUpdate) -> Task:
    task = next((item for item in tasks if item.id == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="task not found")

    if body.title is not None:
        title = body.title.strip()
        if not title:
            raise HTTPException(status_code=400, detail="title is required")
        task.title = title
    if body.completed is not None:
        task.completed = body.completed
    return task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    task = next((item for item in tasks if item.id == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="task not found")
    tasks.remove(task)
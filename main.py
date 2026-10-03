from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field


app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=400,
        content={"error": "Invalid request body"}
    )


tasks = [
    {"id": 1, "title": "Learn Python", "done": False},
    {"id": 2, "title": "Learn FastAPI", "done": False},
    {"id": 3, "title": "Build Task API", "done": False}
]


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1)


class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None


@app.get(
    "/",
    description="Get basic information about the Task API"
)
def read_root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get(
    "/health",
    description="Check if the API is running"
)
def health_check():
    return {
        "status": "ok"
    }


@app.get(
    "/tasks",
    description="Get all tasks"
)
def get_tasks():
    return tasks


@app.get(
    "/tasks/{task_id}",
    description="Get a single task by ID"
)
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )


@app.post(
    "/tasks",
    status_code=201,
    description="Create a new task"
)
def create_task(task: TaskCreate):
    new_id = max([t["id"] for t in tasks], default=0) + 1

    new_task = {
        "id": new_id,
        "title": task.title,
        "done": False
    }

    tasks.append(new_task)

    return new_task


@app.put(
    "/tasks/{task_id}",
    description="Update an existing task"
)
def update_task(task_id: int, task_update: TaskUpdate):
    for task in tasks:
        if task["id"] == task_id:

            if task_update.title is not None:
                if task_update.title == "":
                    raise HTTPException(
                        status_code=400,
                        detail="Title cannot be empty"
                    )
                task["title"] = task_update.title

            if task_update.done is not None:
                task["done"] = task_update.done

            return task

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )


@app.delete(
    "/tasks/{task_id}",
    status_code=204,
    description="Delete a task by ID"
)
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )
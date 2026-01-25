import fastapi
from pydantic import BaseModel, Field
from typing import Any
from asyncio import PriorityQueue
from enum import Enum
from datetime import datetime, timedelta
import asyncio
import uvicorn
from random import randint
import uuid

class TaskResponse(BaseModel):
    payload: Any
    priority: int = Field(ge=0)

class Status(str, Enum):
    pending="pending"
    running="running"
    success="success"
    failed="failed"

class Task:
    id: uuid.UUID
    payload: Any
    priority: int
    status: Status = Status.pending
    result: Any = None
    error: Any = None
    retries_count: int = 0
    next_retry_at: datetime = None
    created_at: datetime
    updated_at: datetime


    def __init__(self, id, payload, priority, created_at):
        self.id = id
        self.payload = payload
        self.priority = priority
        self.created_at = created_at
        self.updated_at = created_at

    def __lt__(self, other):
        return self.priority > other.priority \
            or self.priority == other.priority and self.created_at < other.created_at

app = fastapi.FastAPI()
queue = PriorityQueue()
tasks = {}
lock = None

async def update_task(task_id: uuid.UUID, task: Task):
    async with lock:
        tasks[task_id] = task

async def do_task(task: Task, semaphore: asyncio.Semaphore, base_delay: int, max_retries: int):
    try:
        for retry_attempt in range(max_retries):
            if task.status == Status.success:
                break
            
            if retry_attempt > 0 and task.status == Status.failed:
                delay = base_delay * (2 ** (retry_attempt))
                task.next_retry_at = datetime.now() + timedelta(seconds=delay)
                await update_task(task.id, task)
                await asyncio.sleep(delay)

            task.status = Status.running
            task.retries_count = retry_attempt
            task.updated_at = datetime.now()
            await update_task(task.id, task)
            
            await asyncio.sleep(1)
            
            if randint(0, 1) == 1:
                task.status = Status.success
                task.result = {"super_chisla": [777, 666]}
                task.error = None
            else:
                task.status = Status.failed
                task.error = {"bad_chisla": [1, 2, 3]}
            
            task.updated_at = datetime.now()
            await update_task(task.id, task)
            
            if task.status == Status.success:
                break
    finally:
        semaphore.release()

async def do_tasks(max_workers: int, base_delay: int, max_retries: int):
    semaphore = asyncio.Semaphore(max_workers)
    while True:
        await semaphore.acquire()
        task = await queue.get()
        asyncio.create_task(do_task(task, semaphore, base_delay, max_retries))

@app.post("/task")
async def task(request: TaskResponse):
    payload = request.payload
    priority = request.priority

    task_id = uuid.uuid4()
    new_task = Task(task_id, payload, priority, datetime.now())
    await update_task(task_id, new_task)
    await queue.put(new_task)

    return {"task_id": str(task_id)}

@app.get("/task/{task_id}")
async def get_task(task_id: str):
    task_uuid = uuid.UUID(task_id)
    
    async with lock:
        task = tasks.get(task_uuid)
    
    if not task:
        raise fastapi.HTTPException(status_code=429, details="Too Many Requests")
    
    return {
        "id": str(task.id),
        "payload": task.payload,
        "priority": task.priority,
        "status": task.status,
        "result": task.result,
        "error": task.error,
        "retries_count": task.retries_count,
        "next_retry_at": task.next_retry_at.isoformat() if task.next_retry_at else None,
        "created_at": task.created_at.isoformat(),
        "updated_at": task.updated_at.isoformat()
    }


async def main(max_workers: int, base_delay: int, max_retries: int):
    global lock
    lock = asyncio.Lock()
    asyncio.create_task(do_tasks(max_workers, base_delay, max_retries))
    
    config = uvicorn.Config(app, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)
    await server.serve()

asyncio.run(main(10, 1, 5))
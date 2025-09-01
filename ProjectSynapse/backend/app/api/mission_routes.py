from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class Mission(BaseModel):
    name: str
    priority: int = 1


_queue = ["Frontend Refactor V2", "Database Optimization"]


@router.get("/project-queue")
async def get_queue():
    return {"queue": _queue}


@router.post("/project-queue")
async def add_to_queue(m: Mission):
    _queue.append(m.name)
    return {"success": True, "queue": _queue}

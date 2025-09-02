from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class Mission(BaseModel):
    name: str
    priority: int = 1


class CrewMission(BaseModel):
    description: str
    agents_count: int = 2


_queue = ["Frontend Refactor V2", "Database Optimization"]


@router.get("/project-queue")
async def get_queue():
    return {"queue": _queue}


@router.post("/project-queue")
async def add_to_queue(m: Mission):
    _queue.append(m.name)
    return {"success": True, "queue": _queue}


@router.post("/crew-mission")
async def run_crew_mission(cm: CrewMission):
    # Simplified version without CrewAI dependencies
    # This simulates a crew mission for now
    import asyncio
    import random

    # Simulate processing time
    await asyncio.sleep(1)

    # Generate a mock result
    mock_results = [
        f"✅ Mission '{cm.description}' completed successfully!",
        f"🚀 Crew of {cm.agents_count} agents deployed for: {cm.description}",
        f"📊 Analysis complete for mission: {cm.description}",
        f"⚡ Task execution finished for: {cm.description}"
    ]

    result = random.choice(mock_results)

    return {
        "result": result,
        "mission": cm.description,
        "agents_used": cm.agents_count,
        "status": "completed",
        "timestamp": asyncio.get_event_loop().time()
    }


# Backwards-compatible aliases (older frontends may use the slash style)
@router.get("/project/queue")
async def get_queue_slash():
    return await get_queue()


@router.post("/project/queue")
async def add_to_queue_slash(m: Mission):
    return await add_to_queue(m)

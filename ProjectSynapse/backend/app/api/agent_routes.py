from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
import random

router = APIRouter()


class Agent(BaseModel):
    id: str
    name: str
    type: str
    status: str
    task: str
    progress: int
    cpu: float
    memory: float


_agents = [
    Agent(
        id="dev-01",
        name="Dev-Agent 01",
        type="dev",
        status="CODING",
        task="Implement API logic",
        progress=60,
        cpu=25.0,
        memory=30.0,
    ),
    Agent(
        id="ux-01",
        name="UX-Agent",
        type="ux",
        status="DESIGNING",
        task="Design UI components",
        progress=80,
        cpu=12.0,
        memory=18.0,
    ),
    Agent(
        id="meta-01",
        name="Meta-Agent",
        type="ops",
        status="ANALYZING",
        task="Monitor cluster performance",
        progress=100,
        cpu=15.0,
        memory=20.0,
    ),
]


@router.get("/agents")
async def get_agents():
    # update dynamic metrics for demo
    for a in _agents:
        a.cpu = round(random.uniform(5, 30), 1)
        a.memory = round(random.uniform(10, 40), 1)
    return _agents


@router.get("/system-logs")
async def get_system_logs():
    return [{"time": datetime.now().strftime("%H:%M:%S"), "message": "Synapse Prime Core is online."}]

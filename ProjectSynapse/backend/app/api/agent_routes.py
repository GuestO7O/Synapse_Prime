from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
import random
from typing import Optional, Dict
from app.services.evolution_marketplace import marketplace

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


class FeedbackRequest(BaseModel):
    agent_id: str
    score: float
    trait_updates: Optional[Dict[str, float]]


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
    message = "Synapse Prime Core is online."
    return [{"time": datetime.now().strftime("%H:%M:%S"), "message": message}]


@router.post("/evolution/feedback")
async def submit_agent_feedback(feedback: FeedbackRequest):
    result = marketplace.submit_feedback(
        feedback.agent_id,
        feedback.score,
        feedback.trait_updates
    )
    if result:
        return {"success": True, "agent": result}
    return {"success": False, "message": "Agent not found"}


@router.get("/evolution/top-agents")
async def get_top_evolved_agents(limit: int = 10):
    top_agents = marketplace.get_top_agents(limit)
    return {"top_agents": [agent.dict() for agent in top_agents]}


@router.get("/evolution/agent/{agent_id}")
async def get_agent_evolution_stats(agent_id: str):
    agent = marketplace.get_agent_stats(agent_id)
    if agent:
        return {"agent": agent.dict()}
    return {"error": "Agent not found"}


@router.post("/evolution/register/{agent_id}")
async def register_agent_for_evolution(agent_id: str):
    agent = marketplace.register_agent(agent_id)
    return {"agent": agent.dict()}


@router.get("/evolution/leaderboard")
async def get_evolution_leaderboard(limit: int = 10):
    leaderboard = marketplace.get_evolution_leaderboard(limit)
    return {"leaderboard": leaderboard}


@router.get("/evolution/stats")
async def get_evolution_stats():
    stats = marketplace.get_evolution_stats()
    return {"stats": stats}


# Backwards-compatible alias
@router.get("/system/logs")
async def get_system_logs_slash():
    return await get_system_logs()

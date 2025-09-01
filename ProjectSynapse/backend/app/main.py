from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from os import getenv
from app.api import agent_routes, mission_routes

load_dotenv()

app = FastAPI(
    title="Project Synapse - Core V3 (Groq)",
    version="3.0.0"
)

# Configureer CORS: lees `FRONTEND_ORIGIN` uit .env of gebruik localhost dev default
frontend_origin = getenv("FRONTEND_ORIGIN", "http://127.0.0.1:5173")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_origin],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(agent_routes.router, prefix="/api/v1", tags=["Agents"])
app.include_router(mission_routes.router, prefix="/api/v1", tags=["Missions"])


@app.get("/")
async def root():
    return {"status": "Project Synapse Core (Groq Edition) is online en operationeel."}

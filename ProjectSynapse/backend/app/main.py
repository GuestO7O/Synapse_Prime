from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from os import getenv
from app.api import agent_routes, mission_routes

load_dotenv()

app = FastAPI(
    title="Project Synapse - Core V3 (Groq)",
    version="3.0.0",
)

# Configureer CORS: lees `FRONTEND_ORIGIN` uit .env of gebruik Vite default (5173)
frontend_origin = getenv("FRONTEND_ORIGIN", "http://127.0.0.1:5173")

# Ondersteun veelgebruikte lokale origins + file (null) origin voor statische HTML
allowed_origins = [
    frontend_origin,
    "http://127.0.0.1:8080",  # HTTP server for frontend testing
    "http://127.0.0.1:8003",
    "http://127.0.0.1:8002",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "http://localhost:5173",
    "null",  # file:// origin wordt door browsers als 'null' gestuurd
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(agent_routes.router, prefix="/api/v1", tags=["Agents"])
app.include_router(mission_routes.router, prefix="/api/v1", tags=["Missions"])


@app.get("/")
async def root():
    return {"status": "Project Synapse Core (Groq Edition) is online en operationeel."}

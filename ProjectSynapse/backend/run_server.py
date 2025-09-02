#!/usr/bin/env python3
"""
Full server starter for Project Synapse with all API routes
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from os import getenv
import uvicorn

# Import our API routes
from app.api import agent_routes, mission_routes

load_dotenv()

app = FastAPI(
    title="Project Synapse - Core V3 (Groq)",
    version="3.0.0"
)

# Configure CORS for all origins (including file:// for local frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include all API routes
app.include_router(agent_routes.router, prefix="/api/v1", tags=["Agents"])
app.include_router(mission_routes.router, prefix="/api/v1", tags=["Missions"])

@app.get("/")
async def root():
    return {"status": "Project Synapse Core (Groq Edition) is online en operationeel."}

if __name__ == "__main__":
    print("🚀 Starting Project Synapse Backend with full API...")
    print("📡 Server URL: http://127.0.0.1:8002")
    print("🔄 CORS enabled for all origins")
    print("🤖 AI Agent routes loaded")
    print("✅ Ready to accept connections...")
    uvicorn.run(app, host="127.0.0.1", port=8002, log_level='info')

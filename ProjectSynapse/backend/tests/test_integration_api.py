"""Integration tests for ProjectSynapse backend API endpoints."""
import sys
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from fastapi.testclient import TestClient  # noqa: E402
from app.main import app  # noqa: E402

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "status" in response.json()


def test_agents_endpoint():
    response = client.get("/api/v1/agents")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_system_logs_endpoint():
    response = client.get("/api/v1/system-logs")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_project_queue_get():
    response = client.get("/api/v1/project-queue")
    assert response.status_code == 200
    data = response.json()
    assert "queue" in data
    assert isinstance(data["queue"], list)


def test_project_queue_post_valid():
    payload = {"name": "Test Mission", "priority": 1}
    response = client.post("/api/v1/project-queue", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "queue" in data


def test_project_queue_post_invalid():
    payload = {"name": "Test", "priority": "high"}  # invalid priority type
    response = client.post("/api/v1/project-queue", json=payload)
    assert response.status_code == 422


def test_backward_compatible_aliases():
    # Test /system/logs
    response = client.get("/api/v1/system/logs")
    assert response.status_code == 200

    # Test /project/queue
    response = client.get("/api/v1/project/queue")
    assert response.status_code == 200

    payload = {"name": "Alias Test", "priority": 2}
    response = client.post("/api/v1/project/queue", json=payload)
    assert response.status_code == 200

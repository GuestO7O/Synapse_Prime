"""Lightweight Python client for the Project Synapse HTTP API.

This client is intentionally minimal and dependency-light (uses `requests`).
It's designed for interactive use and for integration in small scripts.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional
import requests


class SynapseClient:
    def __init__(self, base_url: str = "http://localhost:5001", timeout: int = 10):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.timeout = timeout

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def get_agents(self) -> List[Any]:
        """GET /api/v1/agents -> list"""
        r = self.session.get(self._url("/api/v1/agents"), timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def get_system_logs(self) -> List[Any]:
        """GET /api/v1/system-logs -> list"""
        r = self.session.get(self._url("/api/v1/system-logs"), timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def get_queue(self) -> List[Any]:
        """GET /api/v1/project-queue -> list"""
        r = self.session.get(self._url("/api/v1/project-queue"), timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def add_to_queue(self, mission: Dict[str, Any]) -> Dict[str, Any]:
        """POST /api/v1/project-queue with a Mission object

        Mission shape (from OpenAPI): {"name": str, "priority": int}
        """
        r = self.session.post(self._url("/api/v1/project-queue"), json=mission, timeout=self.timeout)
        r.raise_for_status()
        return r.json()


__all__ = ["SynapseClient"]

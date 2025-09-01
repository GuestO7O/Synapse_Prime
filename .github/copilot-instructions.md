# Synapse_Prime – AI agent working notes

Purpose: give AI coding agents the minimum, repo-specific context to be productive fast. Keep answers concrete and aligned with these conventions.

## Architecture snapshot
- Backend: FastAPI app in `ProjectSynapse/backend/app`.
  - Entry: `app/main.py` creates `FastAPI(title=..., version=...)`, configures CORS from `FRONTEND_ORIGIN` (default `http://127.0.0.1:5173`), and includes routers:
    - `app.api.agent_routes` → mounted at `/api/v1` provides `/agents`, `/system-logs` (plus alias `/system/logs`).
    - `app.api.mission_routes` → mounted at `/api/v1` provides `/project-queue` (GET/POST) and backward-compatible aliases `/project/queue` (GET/POST).
  - Validation: custom `RequestValidationError` handler returns `{message, detail, body}` with HTTP 422.
- Frontend: static demo pages in `ProjectSynapse/frontend/` using fetch to the API (see `dashboard.html`, `main.js`).
- Clients:
  - Hand-written minimal client: `clients/python/synapse_client.py` (requests-based).
  - Generated typed client from OpenAPI: `clients/generated/python-client/project_synapse_core_v3_groq_client/`.
- Scripts: `scripts/export_openapi.py` loads `app.main:app` without mutating global `sys.path` and writes `docs/external/openapi.json`.
- Tests: `ProjectSynapse/backend/tests/` include import checks, OpenAPI export test, TestClient integration tests for queue endpoints, and a generated-client import test.


## Dev workflows (do these by default)
- Python env: use the backend venv at `ProjectSynapse/backend/venv/` for running tests and scripts.
- Run tests (from backend): `python -m pytest -q`.
- Lint/type check (local venv): `ruff check .` and `mypy .` (CI also runs both).
- Export OpenAPI (from repo root):
  - `ProjectSynapse/backend/venv/Scripts/python.exe scripts/export_openapi.py --backend-dir ProjectSynapse/backend --out docs/external/openapi.json`
- Live smoke test (backend): run uvicorn `-m uvicorn app.main:app --host 127.0.0.1 --port 8000` and GET `/`.

## Conventions & patterns
- Routers mount at `/api/v1`. Prefer hyphen style paths (e.g., `/system-logs`, `/project-queue`); slash-style aliases exist for backward compatibility.
- Pydantic models live alongside routes (e.g., `Mission` in `mission_routes.py`); keep payloads aligned with these models (`{"name": str, "priority": int}` for POST queue).
- When importing the backend app outside the package (scripts/tests), use the pattern from `scripts/export_openapi.py`: synthesize an `app` package via `importlib.util` and set `__path__`.
- Generated client lives under `clients/generated/python-client`; tests add that folder to `sys.path` to import the package during CI (see `test_generated_client_import.py`). For mypy, the import is annotated with `# type: ignore[import]`.
- Validation errors return structured JSON via the global exception handler in `main.py`. Prefer returning clear, minimal payloads from endpoints.

## CI/CD
- Workflows:
  - `.github/workflows/ci.yml`: installs backend deps, runs pytest, exports OpenAPI, uploads artifact.
  - `.github/workflows/lint.yml`: runs `ruff` and `mypy`.
- Keep generated artifacts out of git unless explicitly intended. Logs like `ProjectSynapse/backend/uvicorn.*.log` are ignored via `.gitignore`.

## Examples to follow
- New endpoint pattern:
  - Create `ProjectSynapse/backend/app/api/<feature>_routes.py`:
    ```python
    from fastapi import APIRouter
    from pydantic import BaseModel

    router = APIRouter()

    class Item(BaseModel):
        id: str

    @router.get("/items")
    async def list_items():
        return []

    @router.post("/items")
    async def create_item(i: Item):
        return {"ok": True, "id": i.id}
    ```
  - Register in `app/main.py`: `app.include_router(feature_routes.router, prefix="/api/v1", tags=["Feature"])`.
- Test new endpoint with FastAPI TestClient in `ProjectSynapse/backend/tests/` (see `test_integration_api.py`).

## Gotchas
- Tests that import the generated client must add `clients/generated/python-client` to `sys.path` at runtime.
- If you see 422 on POSTs, payload shape likely mismatches the Pydantic model (e.g., use `{name, priority}` for queue).
- CORS: set `FRONTEND_ORIGIN` in `.env` if your dev frontend origin differs from default.

If any of these conventions seem missing or out of date, propose an edit with a small diff touching the exact files noted above.


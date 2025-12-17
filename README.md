# Synapse_Prime

Een AI-agent werkruimte gebouwd met FastAPI backend, statische frontend, en gegenereerde Python clients.

## Overzicht

Synapse_Prime is een project voor het beheren van AI-agents, missies, en system logs via een REST API. Het omvat:

- **Backend**: FastAPI app met endpoints voor agents, missies, en logs.
- **Frontend**: Eenvoudige HTML/JS demo voor API interactie.
- **Clients**: Handgeschreven en OpenAPI-gegenereerde Python clients.
- **Scripts**: Hulpmiddelen voor OpenAPI export en debugging.

## Installatie

1. Clone de repo.
2. Maak een venv: `python -m venv .venv`
3. Activeer: `& .\.venv\Scripts\Activate.ps1`
4. Installeer deps: `pip install -r ProjectSynapse/backend/requirements.txt`
5. Installeer tools: `pip install ruff mypy`

## Gebruik

### Backend starten

```powershell
& ".\.venv\Scripts\python.exe" -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### Frontend openen

Open `ProjectSynapse/frontend/index.html` in browser.

### Tests draaien

```powershell
& ".\.venv\Scripts\python.exe" -m pytest ProjectSynapse/backend/tests/
```

### Lint en typecheck

```powershell
& ".\.venv\Scripts\python.exe" -m ruff check .
& ".\.venv\Scripts\python.exe" -m mypy ProjectSynapse/backend
```

### OpenAPI exporteren

```powershell
& ".\.venv\Scripts\python.exe" scripts/export_openapi.py --backend-dir ProjectSynapse/backend --out docs/external/openapi.json
```

## API Endpoints

- `GET /`: Status check.
- `GET /api/v1/agents`: Lijst van agents.
- `GET /api/v1/system-logs`: System logs (alias: `/api/v1/system/logs`).
- `GET /api/v1/project-queue`: Missie queue (alias: `/api/v1/project/queue`).
- `POST /api/v1/project-queue`: Voeg missie toe (JSON: `{"name": str, "priority": int}`).

## Debugging

Gebruik `python tools/ai_debugger.py --diagnose --fix` voor automatische checks en fixes.

## CI/CD

GitHub Actions draait tests, lint, en OpenAPI export op pushes/PRs naar main.

## Bijdragen

- Volg de conventions in `.github/copilot-instructions.md`.
- Voeg tests toe voor nieuwe features.
- Update README bij veranderingen.

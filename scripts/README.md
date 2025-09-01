scripts/export_openapi.py - usage

This folder contains utility scripts for the ProjectSynapse workspace.

export_openapi.py
- Purpose: import the backend FastAPI application and write its OpenAPI
  specification to `docs/external/openapi.json`.
- Basic usage (from workspace root):

```powershell
# use the backend venv python to ensure dependencies are available
& "ProjectSynapse\backend\venv\Scripts\python.exe" \
  "scripts\export_openapi.py" --backend-dir ProjectSynapse/backend --out docs/external/openapi.json
```

- The script exposes a programmatic API: `export_openapi(backend_dir, out)` so it
  can be invoked by tests or CI workflows without mutating global sys.path.

Notes
- If you run the script with an interpreter that doesn't have FastAPI installed
  the script will log an error and exit with code 1. Use the backend virtualenv
  interpreter for best results.

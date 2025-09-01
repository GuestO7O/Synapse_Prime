FastAPI full-stack template — relevant API snippets

Source: fastapi/full-stack-fastapi-template (README + backend/app/main.py excerpt)

Key patterns to reuse

1) Controlled OpenAPI URL and operationId generation

```python
from fastapi import FastAPI
from fastapi.routing import APIRoute

def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)

# include routers under a version prefix
app.include_router(api_router, prefix=settings.API_V1_STR)
```

Why use it
- Pin `openapi_url` to a stable path (e.g. `/api/v1/openapi.json`) so CI or client generators can fetch it.
- `generate_unique_id_function` gives predictable operationIds for generated clients.

2) CORS + middleware setup pattern

```python
from starlette.middleware.cors import CORSMiddleware
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
```

3) How to export OpenAPI as a file

- Add a small script that imports your `app` and writes `app.openapi()` to JSON. See `scripts/export_openapi.py` (created in this repo) which writes to `docs/external/openapi.json`.

Reuse notes
- Copy `custom_generate_unique_id` and `openapi_url` into your `app/main.py` to control docs and client generation.
- Add the export script to CI to commit updated `openapi.json` when routes change.

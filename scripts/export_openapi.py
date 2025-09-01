#!/usr/bin/env python3
"""Export FastAPI app.openapi() to docs/external/openapi.json

Place this file at scripts/export_openapi.py and run from workspace root:
python ./scripts/export_openapi.py
"""
from pathlib import Path
import sys
import json
import logging
import importlib.util
import types

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

root = Path(__file__).resolve().parents[1]


def _load_app_from_backend(backend_dir: Path):
    """Load the FastAPI app from backend/app/main.py without mutating global sys.path.

    This creates a synthetic package module `app` with __path__ pointed at
    backend/app so internal package imports continue to work.
    """
    app_pkg_dir = backend_dir / "app"
    main_py = app_pkg_dir / "main.py"
    if not main_py.exists():
        raise FileNotFoundError(f"Cannot find backend app main.py at {main_py}")

    # Create a package module for `app`
    pkg = types.ModuleType("app")
    pkg.__path__ = [str(app_pkg_dir)]
    sys.modules["app"] = pkg

    # Load app.main as module
    spec = importlib.util.spec_from_file_location("app.main", str(main_py))
    module = importlib.util.module_from_spec(spec)
    sys.modules["app.main"] = module
    spec.loader.exec_module(module)
    if not hasattr(module, "app"):
        raise RuntimeError("Loaded module does not expose 'app' attribute")
    return getattr(module, "app")


def export_openapi(backend_dir: str | Path | None = None, out: str | Path | None = None):
    root = Path(__file__).resolve().parents[1]
    backend = Path(backend_dir) if backend_dir else root / "ProjectSynapse" / "backend"
    out_path = Path(out) if out else root / "docs" / "external" / "openapi.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        app = _load_app_from_backend(backend)
    except Exception:
        logging.exception("ERROR importing FastAPI app")
        raise SystemExit(1)

    openapi = app.openapi()
    out_path.write_text(json.dumps(openapi, indent=2), encoding="utf-8")
    logging.info("Wrote OpenAPI JSON to: %s", out_path)
    return out_path


def main(argv=None):
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("--backend-dir", help="Path to ProjectSynapse/backend")
    p.add_argument("--out", help="Output OpenAPI JSON path")
    ns = p.parse_args(argv)
    return export_openapi(backend_dir=ns.backend_dir, out=ns.out)


if __name__ == "__main__":
    main()

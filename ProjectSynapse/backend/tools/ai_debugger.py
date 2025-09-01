"""AI Debugger - a lightweight diagnostic and autopatcher for ProjectSynapse backend.

This script runs a set of deterministic checks, applies low-risk fixes, and records
actions in a simple state file so future runs can prioritise recurrent issues.

Usage:
  python tools\ai_debugger.py --diagnose          # just run checks and print report
  python tools\ai_debugger.py --fix               # apply safe, automated fixes
  python tools\ai_debugger.py --diagnose --fix --report

Notes:
- This is NOT an autonomous learning agent. It only records fixes and increments
  counters (a tiny heuristic) to track repeated issues. Review any changes before
  committing to version control.
"""
from __future__ import annotations
import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
import logging
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BACKEND = ROOT / "backend"
STATE_FILE = BACKEND / ".ai_debugger_state.json"


def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_state(state: dict):
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def check_requirements(path: Path) -> list:
    issues = []
    if not path.exists():
        issues.append(("missing_file", str(path)))
        return issues
    text = path.read_text(encoding="utf-8")
    if "```" in text:
        issues.append(("codeblock_markers", "Found code block fences in requirements.txt"))
    if re.search(r"python\s+-m\s+venv", text):
        issues.append(("shell_command", "Found a shell command in requirements.txt (e.g. python -m venv)"))
    return issues


def fix_requirements(path: Path) -> list:
    fixes = []
    text = path.read_text(encoding="utf-8")
    # Remove triple-backticks and any leading language tag lines
    new_lines = []
    for line in text.splitlines():
        if line.strip().startswith("```"):
            continue
        # drop common shell invocations that don't belong in requirements
        if re.match(r"^\s*python\s+-m\s+venv\b", line):
            fixes.append("removed_venv_line")
            continue
        new_lines.append(line)
    # avoid single-letter variable names for linters and readability
    cleaned = "\n".join([ln.rstrip() for ln in new_lines if ln.strip() != ""]) + "\n"
    if cleaned != text:
        path.write_text(cleaned, encoding="utf-8")
        fixes.append("cleaned_requirements")
    return fixes


def check_api_folder(folder: Path) -> list:
    issues = []
    if not folder.exists():
        issues.append(("missing_api_folder", str(folder)))
        return issues
    py_files = list(folder.glob("*.py"))
    if len(py_files) == 0:
        issues.append(("empty_api_folder", "No .py files in api folder"))
    return issues


def add_api_stub(folder: Path) -> bool:
    folder.mkdir(parents=True, exist_ok=True)
    stub = folder / "__init__.py"
    if not stub.exists():
        stub.write_text("# api package\n", encoding="utf-8")
    sample = folder / "health_routes.py"
    if not sample.exists():
        sample.write_text(
            "from fastapi import APIRouter\nrouter = APIRouter()\n@router.get('/health')\nasync def health():\n    return {'status':'ok'}\n",
            encoding="utf-8",
        )
        return True
    return False


def import_check(venv_python: Path, module: str) -> tuple:
    """Try to import module using venv python; return (ok, output)."""
    try:
        cmd = [str(venv_python), "-c", f"import {module}; print('OK')"]
        p = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=15,
        )
        ok = "OK" in p.stdout
        return ok, (p.stdout + p.stderr).strip()
    except Exception as e:
        return False, str(e)


def http_check(url: str) -> tuple:
    try:
        import urllib.request

        with urllib.request.urlopen(url, timeout=5) as r:
            b = r.read()
            text = b.decode("utf-8", errors="replace")
            return True, text
    except Exception as e:
        return False, str(e)


def short_report(report: dict):
    lines = []
    lines.append(f"Report generated: {datetime.now(timezone.utc).isoformat().replace('+00:00','Z')}")
    for k, v in report.items():
        lines.append(f"- {k}: {v}")
    return "\n".join(lines)


def main(args):
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
    state = load_state()
    state.setdefault("fix_counts", {})
    report: dict = {"timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00','Z')}

    # 1) requirements check
    req = BACKEND / "requirements.txt"
    r_issues = check_requirements(req)
    report["requirements_issues"] = r_issues
    if args.fix and r_issues:
        fixes = fix_requirements(req)
        for f in fixes:
            state["fix_counts"][f] = state["fix_counts"].get(f, 0) + 1
        report["requirements_fixes"] = fixes

    # 2) api folder check
    api_folder = BACKEND / "app" / "api"
    api_issues = check_api_folder(api_folder)
    report["api_issues"] = api_issues
    if args.fix and any(i[0] in ("empty_api_folder", "missing_api_folder") for i in api_issues):
        changed = add_api_stub(api_folder)
        if changed:
            state["fix_counts"]["add_api_stub"] = state["fix_counts"].get("add_api_stub", 0) + 1
            if "api_fixes" not in report:
                report["api_fixes"] = []
            report["api_fixes"].append("added health_routes stub")

    # 3) venv and import checks
    venv_py = BACKEND / "venv" / "Scripts" / "python.exe"
    # If a dedicated venv for the project exists, use it. Otherwise fall back to
    # the currently running Python executable (useful when using conda or system
    # environments). This makes the checker more robust on developer machines.
    if venv_py.exists():
        python_to_use = venv_py
        report["venv_missing"] = False
    else:
        python_to_use = Path(sys.executable)
        report["venv_missing"] = True
        report["used_python_fallback"] = str(python_to_use)

    ok_fastapi, out_fastapi = import_check(python_to_use, "fastapi")
    report["fastapi_import_ok"] = ok_fastapi
    report["fastapi_import_out"] = out_fastapi

    # 4) run simple HTTP checks against local server if requested
    if args.check_http:
        urls = ["http://127.0.0.1:5001/", "http://127.0.0.1:5001/api/v1/agents"]
        http_results = {}
        for u in urls:
            ok, out = http_check(u)
            http_results[u] = {"ok": ok, "out": out}
        report["http_checks"] = http_results

    # 5) Persist state and print report
    state["last_run"] = datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
    save_state(state)

    if args.report:
        logging.info("%s", short_report(report))
    else:
        logging.info(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="AI Debugger for ProjectSynapse backend")
    p.add_argument("--diagnose", action="store_true")
    p.add_argument("--fix", action="store_true")
    p.add_argument("--report", action="store_true")
    p.add_argument("--check-http", action="store_true", help="Try simple HTTP checks against localhost:5001")
    ns = p.parse_args()
    if not (ns.diagnose or ns.fix):
        ns.diagnose = True
    main(ns)

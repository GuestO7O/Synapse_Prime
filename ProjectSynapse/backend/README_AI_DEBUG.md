ProjectSynapse backend - AI Debugger

Usage
-----
From the `backend` folder, within the project virtualenv, run:

```powershell
# diagnose only
python tools\ai_debugger.py --diagnose --report

# diagnose and apply safe fixes
python tools\ai_debugger.py --diagnose --fix --report --check-http
```

What it does
------------
- Runs deterministic checks (requirements formatting, missing api files, venv import checks).
- Applies low-risk fixes (clean `requirements.txt`, create a minimal `app/api/health_routes.py`).
- Saves a small `.ai_debugger_state.json` with counters so repeated fixes are visible on subsequent runs.

Security note
-------------
This script makes automated, low-risk changes only. Review changes before committing. Do not run with `--fix` on production servers without review.

Permission hints
----------------
- If you see permission errors while creating files or venv activation, consider running the PowerShell commands to set ExecutionPolicy for your user and grant file permissions to your account (see main README).

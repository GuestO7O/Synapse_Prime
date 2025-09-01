"""Prototype controlled self-improvement helper.

This script runs the `ai_debugger`, collects suggested fixes, and prepares a local
git branch with the changes and a draft PR message (file). It DOES NOT push or
open a PR automatically - that requires explicit user confirmation.

Usage:
    python tools/self_improve.py --dry-run   # show proposed actions
    python tools/self_improve.py --apply     # create branch and commit changes locally

Note: requires `git` to be available and repository to be clean or user to confirm.
"""
import json
import subprocess
from pathlib import Path
import sys
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"


def run_debugger():
    p = subprocess.run([sys.executable, str(TOOLS / "ai_debugger.py"), "--diagnose", "--report"], capture_output=True, text=True)
    try:
        return json.loads(p.stdout)
    except Exception:
        return {"raw": p.stdout, "err": p.stderr}


def git(cmd, check=True):
    return subprocess.run(["git"] + cmd, cwd=ROOT, check=check)


def main(apply=False):
    report = run_debugger()
    logging.info("Debugger report:\n%s", json.dumps(report, indent=2, ensure_ascii=False))
    # For demo, we'll consider only requirements fixes and api stubs
    # Check git status
    st = subprocess.run(["git","status","--porcelain"], cwd=ROOT, capture_output=True, text=True)
    if st.stdout.strip() != "":
        logging.warning("Repository not clean. Commit or stash changes before apply.")
        return
    if not apply:
        logging.info("Dry-run complete. To apply changes run with --apply")
        return
    branch = "ai/self-improve-" + subprocess.run(["date","+%s"], capture_output=True, text=True).stdout.strip()
    git(["checkout","-b",branch])
    git(["add","-A"])
    git(["commit","-m","Apply safe fixes from ai_debugger"])
    pr_file = ROOT / "SELF_IMPROVE_PR.md"
    pr_file.write_text("# Proposed AI fixes\n\nSee attached changes prepared by ai_debugger. Review before push.")
    logging.info("Prepared branch %s and local commit. See %s", branch, pr_file)


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--apply", action="store_true")
    args = p.parse_args()
    main(apply=args.apply)

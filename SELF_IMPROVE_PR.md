# Proposed AI Improvements

This commit contains the following improvements prepared by the automated assistant:

- Fix test import path in `backend/tests/test_imports.py` (robust dirname-based sys.path prepend)
- Refactor `scripts/export_openapi.py` to provide `export_openapi()` API, avoid global sys.path mutations, add logging
- Replace prints with structured logging in `backend/tools/ai_debugger.py` and `backend/tools/self_improve.py`
- Add unit test `backend/tests/test_export_openapi.py` that validates OpenAPI export
- Add CI workflow `.github/workflows/ci.yml` to run backend tests and export OpenAPI
- Add `scripts/README.md` with usage notes

Review notes
- All changes are low-risk and covered by tests. CI workflow will run the tests and export OpenAPI as an artifact.
- No automatic push or PR creation performed. To push: create remote and run `git push -u origin feature/ai-improvements`.

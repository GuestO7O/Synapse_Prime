def test_import_app():
    import sys
    from pathlib import Path

    """Sanity import test for the backend FastAPI app.

    This test ensures the `app` package is importable when running tests
    from the repository root or via test runners. It prepends the project
    backend directory to `sys.path` in a robust way.
    """

    # Ensure the backend package directory is on sys.path regardless of CWD
    backend_dir = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(backend_dir))
    from app import main
    assert hasattr(main, 'app')

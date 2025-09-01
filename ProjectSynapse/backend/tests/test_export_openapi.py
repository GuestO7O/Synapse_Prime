def test_export_openapi(tmp_path):
    from pathlib import Path
    import importlib.util

    repo_root = Path(__file__).resolve().parents[3]
    scripts_main = repo_root / "scripts" / "export_openapi.py"
    spec = importlib.util.spec_from_file_location("export_openapi", str(scripts_main))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    backend_dir = repo_root / "ProjectSynapse" / "backend"
    out_file = tmp_path / "openapi.json"
    res = mod.export_openapi(backend_dir=backend_dir, out=out_file)
    assert Path(res).exists()
    text = Path(res).read_text(encoding="utf-8")
    assert 'openapi' in text

import sys
from pathlib import Path

# Ensure generated client package directory is on sys.path so it can be imported
ROOT = Path(__file__).resolve().parents[3]
GEN_CLIENT_DIR = ROOT / "clients" / "generated" / "python-client"
if str(GEN_CLIENT_DIR) not in sys.path:
    sys.path.insert(0, str(GEN_CLIENT_DIR))


def test_generated_client_import():
    import project_synapse_core_v3_groq_client as gen  # type: ignore[import]

    # instantiate the client with a dummy base_url
    c = gen.Client(base_url="http://localhost")
    assert c._base_url == "http://localhost"

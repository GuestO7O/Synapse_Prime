Synapse Python client

A tiny, requests-based client for the Synapse Prime backend. Intended for quick scripts and interactive use.

Install:

```powershell
pip install requests
```

Usage:

```python
from clients.python.synapse_client import SynapseClient

c = SynapseClient(base_url="http://localhost:5001")
print(c.get_agents())
```

Notes:
- This client is intentionally minimal. For production use generate a typed client from `docs/external/openapi.json` or use more robust HTTP handling and retries.

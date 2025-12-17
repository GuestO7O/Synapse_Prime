# ProjectSynapse Frontend

Quick start:

- Open `index.html` in your browser.
- The frontend auto-detects the backend on these ports (in order): 8002, 8003, 8000.
- To force a specific base URL, copy `config.example.js` to `config.js` and set:

```html
window.SYNAPSE_API_BASE = 'http://127.0.0.1:8002/api/v1'
```

Notes:

- Hard refresh (Ctrl+F5) after changes to pick up the latest JS.
- Debug console logs show the detected API base and request status.

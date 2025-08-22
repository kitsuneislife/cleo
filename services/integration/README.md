# Integration Adapter

Minimal HTTP adapter (FastAPI) that forwards bot observations to `control` via gRPC.

Usage (development):

```powershell
#.venv\Scripts\Activate.ps1
#python services\integration\adapter.py
```

Environment variables:
- `CONTROL_HOST`, `CONTROL_PORT` — where control gRPC is reachable (defaults to localhost:50061)
- `ADAPTER_PORT` — port to expose HTTP adapter (default 8001)
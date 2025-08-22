# Adapter (services/integration)

This small HTTP adapter accepts bot observations and forwards them to the Control gRPC service.

Endpoints
- POST /observe
  - Body: JSON with { "agent_id": string?, "state": string }
  - `state` is expected to be a base64-encoded bytes blob containing the observation payload (adapter accepts raw utf-8 as fallback).
  - Adapter decodes the state and calls Control.RequestDecision with a `DecisionRequest` proto message.

- GET /health
  - Returns diagnostic JSON with keys: `status`, `proto_imported`, `control_connectivity_ok`, `control_error`, `import_error`.
  - Designed to be permissive for development so compose can start dependent services while Control finishes booting.

Environment variables
- ADAPTER_PORT (default: 8001)
- CONTROL_HOST (default: control)
- CONTROL_PORT (default: 50061)
- ADAPTER_CONTROL_RETRIES (default: 5)
- ADAPTER_CONTROL_BACKOFF_BASE (default: 0.5)  # seconds
- ADAPTER_CONTROL_TIMEOUT (default: 4)  # seconds per attempt

Running locally
- Using Docker Compose (recommended for development):

  docker compose up --build

  This will start `adapter`, `control`, `worldmodel`, and the example `mineflayer-bot` if present.

- To run the adapter directly (for debugging):

  python -m services.integration.adapter

Testing
- The project contains an E2E pytest at `tests/e2e/test_mine_block.py` that runs a mineflayer bot and validates the adapter logs for the `mined_block` marker.

Notes
- The adapter will log the decoded `state` payload (useful for E2E detection). Retry behavior when contacting Control can be tuned via env vars above.
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
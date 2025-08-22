"""HTTP adapter that accepts bot observations and forwards to Control gRPC.

Endpoint: POST /observe
Body: { "agent_id": str, "state": base64 or raw string (sent as bytes) }

This adapter is intentionally minimal for POC.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import grpc
import base64

try:
    from proto import control_pb2_grpc, control_pb2
except Exception:
    control_pb2 = None
    control_pb2_grpc = None

app = FastAPI()


class ObserveReq(BaseModel):
    agent_id: str
    state: str  # base64 encoded


def _get_control_stub():
    host = os.environ.get('CONTROL_HOST', 'localhost')
    port = int(os.environ.get('CONTROL_PORT', '50061'))
    channel = grpc.insecure_channel(f"{host}:{port}")
    return control_pb2_grpc.ControlServiceStub(channel)


@app.post('/observe')
def observe(req: ObserveReq):
    if not control_pb2_grpc:
        raise HTTPException(status_code=500, detail='control proto not available')
    try:
        state_bytes = base64.b64decode(req.state)
    except Exception:
        # accept raw utf-8 string as fallback
        state_bytes = req.state.encode('utf-8')
    stub = _get_control_stub()
    grpc_req = control_pb2.DecisionRequest(agent_id=req.agent_id, state=state_bytes)
    try:
        resp = stub.RequestDecision(grpc_req, timeout=3)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f'control error: {e}')
    # Return first operator if any
    if len(resp.operators) > 0:
        op = resp.operators[0]
        return { 'operator_id': op.id, 'description': op.description, 'utility': op.utility }
    return { 'operator_id': None }


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=int(os.environ.get('ADAPTER_PORT', '8001')))

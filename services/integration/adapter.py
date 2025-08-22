"""HTTP adapter that accepts bot observations and forwards to Control gRPC.

Endpoint: POST /observe
Body: { "agent_id": str, "state": base64 or raw string (sent as bytes) }

This adapter is intentionally minimal for POC.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import logging
import os
import grpc
import base64

control_pb2 = None
control_pb2_grpc = None
_import_error = None
try:
    # Preferred: package import when running as a package
    from proto import control_pb2_grpc, control_pb2
    control_pb2 = control_pb2
    control_pb2_grpc = control_pb2_grpc
except Exception as e1:
    _import_error = e1
    try:
        # Fallback: direct module import (in case generated stubs are top-level)
        import control_pb2 as control_pb2
        import control_pb2_grpc as control_pb2_grpc
    except Exception as e2:
        # Save the last exception for diagnostics
        _import_error = e2
        control_pb2 = None
        control_pb2_grpc = None
        # Log the import failure; adapter startup may continue and return 500s until fixed
        logging.getLogger('cleo.adapter').exception('failed to import generated proto stubs')

app = FastAPI()


class ObserveReq(BaseModel):
    agent_id: Optional[str] = None
    state: str  # base64 encoded


logger = logging.getLogger('cleo.adapter')
logging.basicConfig(level=logging.INFO)


def _get_control_stub():
    host = os.environ.get('CONTROL_HOST', 'localhost')
    port = int(os.environ.get('CONTROL_PORT', '50061'))
    channel = grpc.insecure_channel(f"{host}:{port}")
    return control_pb2_grpc.ControlServiceStub(channel)


@app.post('/observe')
def observe(req: ObserveReq):
    if not control_pb2_grpc:
        logger.error('control proto import failed; proto package not available')
        raise HTTPException(status_code=500, detail='control proto not available')
    try:
        state_bytes = base64.b64decode(req.state)
    except Exception:
        # accept raw utf-8 string as fallback
        state_bytes = req.state.encode('utf-8')
    # Log the decoded state for observability in E2E tests (may contain markers like 'mined_block')
    try:
        try:
            state_str = state_bytes.decode('utf-8')
        except Exception:
            state_str = str(state_bytes)
        logger.info('observe payload: %s', state_str)
    except Exception:
        logger.exception('failed to log observe payload')
    stub = _get_control_stub()
    grpc_req = control_pb2.DecisionRequest(agent_id=req.agent_id, state=state_bytes)
    # Retry with exponential backoff for transient control connectivity issues
    # configurable via env to allow test/local tuning
    max_attempts = int(os.environ.get('ADAPTER_CONTROL_RETRIES', '5'))
    base_delay = float(os.environ.get('ADAPTER_CONTROL_BACKOFF_BASE', '0.5'))
    per_attempt_timeout = float(os.environ.get('ADAPTER_CONTROL_TIMEOUT', '4'))
    import random
    resp = None
    last_exc = None
    for attempt in range(1, max_attempts + 1):
        try:
            # per-attempt timeout configurable
            resp = stub.RequestDecision(grpc_req, timeout=per_attempt_timeout)
            last_exc = None
            break
        except Exception as e:
            last_exc = e
            logger.warning('control call attempt %d/%d failed: %s', attempt, max_attempts, e)
            # brief backoff with jitter before retrying
            if attempt < max_attempts:
                try:
                    # exponential backoff with full jitter
                    exp = base_delay * (2 ** (attempt - 1))
                    jitter = random.uniform(0, exp)
                    delay = exp + jitter
                    logger.info('retrying control call after %.2fs (exp=%.2f jitter=%.2f)', delay, exp, jitter)
                    import time

                    time.sleep(delay)
                except Exception:
                    # ignore sleep errors and continue
                    pass
    if last_exc is not None and resp is None:
        logger.exception('control call failed after %d attempts', max_attempts)
        raise HTTPException(status_code=502, detail=f'control error: {last_exc}')
    # Return first operator if any
    if len(resp.operators) > 0:
        op = resp.operators[0]
        return { 'operator_id': op.id, 'description': op.description, 'utility': op.utility }
    return { 'operator_id': None }


@app.get('/health')
def health():
    """Simple health endpoint used by Docker / orchestrators.

    Returns 200 when adapter is healthy. The JSON body contains diagnostic
    hints about proto import and ability to contact the control service.
    """
    proto_ok = control_pb2 is not None and control_pb2_grpc is not None
    control_ok = False
    control_err = None
    if proto_ok:
        try:
            # attempt a non-blocking connectivity check; ignore failures for readiness
            stub = _get_control_stub()
            try:
                # Some stubs don't expose _channel; guard that access
                channel = getattr(stub, '_channel', None)
                if channel is not None:
                    # ask the channel for connectivity state (non-blocking)
                    channel.check_connectivity_state(False)
                    control_ok = True
            except Exception:
                # don't fail readiness because control may still be booting
                control_ok = False
        except Exception as e:
            control_err = str(e)

    # Permissive readiness: if proto stubs are imported we return overall OK so
    # compose/containers will start dependent services even if control is still
    # finishing startup. Detailed diagnostics are provided in the body.
    overall_status = 'ok' if proto_ok else 'bad'
    return {
        'status': overall_status,
        'proto_imported': bool(proto_ok),
        'control_connectivity_ok': bool(control_ok),
        'control_error': control_err,
        'import_error': str(_import_error) if _import_error is not None else None,
    }


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=int(os.environ.get('ADAPTER_PORT', '8001')))

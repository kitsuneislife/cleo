"""Servidor gRPC mínimo para o Control Service (ciclo de decisão MVP).
Gere os stubs com:
python -m grpc_tools.protoc -I../../proto --python_out=. --grpc_python_out=. ../../proto/control.proto
"""
import logging
import os
from concurrent import futures
import grpc

try:
    from proto import control_pb2_grpc, control_pb2
except Exception:
    control_pb2 = None
    control_pb2_grpc = None

# import decision utility and storage
from services.control.decision import rank_operators
from services.control.store import DecisionStore

# try to import worldmodel stubs
try:
    from proto import worldmodel_pb2_grpc, worldmodel_pb2
except Exception:
    worldmodel_pb2 = None
    worldmodel_pb2_grpc = None

# instantiate a process-local store (file-based by default)
store = DecisionStore()

class ControlServicer(control_pb2_grpc.ControlServiceServicer if control_pb2_grpc else object):
    def RequestDecision(self, request, context):
        logging.info(f"Decision request from {request.agent_id}")
        # Optionally call worldmodel to get prediction
        if worldmodel_pb2_grpc:
            try:
                wm_host = os.environ.get('WORLD_MODEL_HOST', 'localhost')
                wm_port = int(os.environ.get('WORLD_MODEL_PORT', '50063'))
                channel = grpc.insecure_channel(f"{wm_host}:{wm_port}")
                wm_stub = worldmodel_pb2_grpc.WorldModelStub(channel)
                wm_req = worldmodel_pb2.PredictRequest(agent_id=request.agent_id, state=request.state)
                _ = wm_stub.Predict(wm_req, timeout=2)
            except Exception:
                logging.warning('WorldModel call failed or unavailable')
        # Use rank_operators to produce candidates
        ops = rank_operators(request.state, agent_id=request.agent_id, store=store)
        # persist the decision candidates for future biasing
        try:
            store.save_decision(request.agent_id, request.state, ops)
        except Exception:
            logging.warning('Failed to save decision to store')
        if control_pb2:
            resp = control_pb2.DecisionResponse()
            for o in ops:
                op = resp.operators.add()
                op.id = o['id']
                op.description = o['description']
                op.utility = o['utility']
            return resp
        return None

    def ApplyAction(self, request, context):
        logging.info(f"Apply action {request.operator_id}")
        if control_pb2:
            return control_pb2.ActionAck(ok=True, message="applied")
        return None

def serve(port=50061):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    if control_pb2_grpc:
        control_pb2_grpc.add_ControlServiceServicer_to_server(ControlServicer(), server)
    server.add_insecure_port(f'[::]:%d' % port)
    server.start()
    logging.info(f"Control server listening on {port}")
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    serve()

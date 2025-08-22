"""Stub minimal do Execution service para testes.
"""
import logging
from concurrent import futures
import grpc

try:
    from proto import control_pb2_grpc, control_pb2
except Exception:
    control_pb2 = None
    control_pb2_grpc = None

class ExecutionServicer(control_pb2_grpc.ControlServiceServicer if control_pb2_grpc else object):
    # Not implementing ControlService; provide ApplyAction-like endpoint via Control proto for simplicity
    def ApplyAction(self, request, context):
        logging.info(f"Execution apply action: {request.operator_id}")
        if control_pb2:
            # record action for tests/inspection
            try:
                if not hasattr(self, '_actions'):
                    self._actions = []
                self._actions.append((request.operator_id, request.params))
            except Exception:
                logging.exception('Failed to record action')
            return control_pb2.ActionAck(ok=True, message="executed")
        return None

    def GetActions(self, request, context):
        # helper RPC for tests to inspect recorded actions (not part of original proto)
        class _Resp:
            def __init__(self, actions):
                self.actions = actions

        actions = getattr(self, '_actions', [])
        # return a minimal representation
        return _Resp(actions)


def serve(port=50064):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    if control_pb2_grpc:
        control_pb2_grpc.add_ControlServiceServicer_to_server(ExecutionServicer(), server)
    bound = False
    for addr in (f"[::]:{port}", f"127.0.0.1:{port}", f"0.0.0.0:{port}"):
        try:
            server.add_insecure_port(addr)
            bound = True
            logging.info(f"Bound Execution server to {addr}")
            break
        except Exception:
            logging.debug(f"Failed to bind Execution server to {addr}")

    if not bound:
        logging.warning(f"Execution server could not bind to any address for port {port}; not starting server")
        return
    server.start()
    logging.info(f"Execution server listening on {port}")
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    serve()

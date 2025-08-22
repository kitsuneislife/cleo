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
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    logging.info(f"Execution server listening on {port}")
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    serve()

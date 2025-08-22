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
            return control_pb2.ActionAck(ok=True, message="executed")
        return None


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

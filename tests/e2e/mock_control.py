"""Minimal mock Control gRPC server used by E2E tests.

This server implements RequestDecision and always returns a single operator so
the adapter receives a positive DecisionResponse during tests and won't fail
with 502 during startup races.
"""
import logging
import time
from concurrent import futures
import grpc

try:
    from proto import control_pb2_grpc, control_pb2
except Exception:
    import control_pb2_grpc, control_pb2


class MockControl(control_pb2_grpc.ControlServiceServicer):
    def RequestDecision(self, request, context):
        logging.info('MockControl: RequestDecision from %s', request.agent_id)
        resp = control_pb2.DecisionResponse()
        op = resp.operators.add()
        op.id = 'mock-op-1'
        op.description = 'mock operator'
        op.utility = 1.0
        return resp


def serve(port=50061, stop_event=None):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    control_pb2_grpc.add_ControlServiceServicer_to_server(MockControl(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    logging.info('MockControl listening on %d', port)
    try:
        while stop_event is None or not stop_event.is_set():
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass
    server.stop(0)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    serve()

"""Servidor gRPC mínimo para o Perception Service.
Este stub usa o arquivo `proto/service.proto`. Gere os stubs com `python -m grpc_tools.protoc -I../../proto --python_out=. --grpc_python_out=. ../../proto/service.proto`.
"""
import logging
from concurrent import futures
import grpc

# Import dos módulos gerados (assuma que foram gerados no mesmo pacote)
try:
    from proto import service_pb2_grpc, service_pb2
except Exception:
    # Placeholder para evitar crash se não gerado ainda
    service_pb2 = None
    service_pb2_grpc = None

class PerceptionServicer(service_pb2_grpc.PerceptionServiceServicer if service_pb2_grpc else object):
    def SendObservation(self, request, context):
        logging.info(f"Received observation from {request.source_id} at {request.timestamp}")
        return service_pb2.Ack(ok=True, message="received") if service_pb2 else None

def serve(port=50051):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    if service_pb2_grpc:
        service_pb2_grpc.add_PerceptionServiceServicer_to_server(PerceptionServicer(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    logging.info(f"Perception server listening on {port}")
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    serve()

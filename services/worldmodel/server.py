"""Stub minimal do WorldModel service para testes de integração.
Registra chamadas em `calls` para verificações em testes.
"""
import logging
from concurrent import futures
import grpc

try:
    from proto import worldmodel_pb2_grpc, worldmodel_pb2
except Exception:
    worldmodel_pb2 = None
    worldmodel_pb2_grpc = None

from services.worldmodel.model import make_default_model

_MODEL = make_default_model()

calls = []

class WorldModelServicer(worldmodel_pb2_grpc.WorldModelServicer if worldmodel_pb2_grpc else object):
    def Predict(self, request, context):
        logging.info(f"Predict called by {request.agent_id}")
        calls.append((request.agent_id, request.state))
        # Use toy model for deterministic prediction
        if worldmodel_pb2:
            pred = _MODEL.predict(request.state)
            return worldmodel_pb2.PredictResponse(prediction=pred)
        return None


def serve(port=50063):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    if worldmodel_pb2_grpc:
        worldmodel_pb2_grpc.add_WorldModelServicer_to_server(WorldModelServicer(), server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    logging.info(f"WorldModel server listening on {port}")
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    serve()

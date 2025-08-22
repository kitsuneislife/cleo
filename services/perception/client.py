"""Client de exemplo para o Perception Service.
"""
import logging
import time
import grpc

try:
    from proto import service_pb2, service_pb2_grpc
except Exception:
    service_pb2 = None
    service_pb2_grpc = None


def send_example(host='localhost', port=50051):
    if not service_pb2 or not service_pb2_grpc:
        print('Stubs não gerados; gere com grpc_tools.protoc antes de rodar.')
        return
    channel = grpc.insecure_channel(f"{host}:{port}")
    stub = service_pb2_grpc.PerceptionServiceStub(channel)
    obs = service_pb2.Observation(source_id='example', timestamp=int(time.time()), payload=b'{}')
    resp = stub.SendObservation(obs)
    print('Ack:', resp.ok, resp.message)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    send_example()

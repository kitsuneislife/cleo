"""Client exemplo para Control Service (MVP).
"""
import grpc
import time

try:
    from proto import control_pb2, control_pb2_grpc
except Exception:
    control_pb2 = None
    control_pb2_grpc = None


def request_decision(host='localhost', port=50061):
    if not control_pb2 or not control_pb2_grpc:
        print('Stubs não gerados; gere com grpc_tools.protoc antes de rodar.')
        return
    channel = grpc.insecure_channel(f"{host}:{port}")
    stub = control_pb2_grpc.ControlServiceStub(channel)
    req = control_pb2.DecisionRequest(agent_id='test', timestamp=int(time.time()), state=b'{}')
    resp = stub.RequestDecision(req)
    print('Received', resp)

import sys
from pathlib import Path
repo_root = str(Path(__file__).resolve().parents[1])
if repo_root not in sys.path:
	sys.path.insert(0, repo_root)

import grpc
from proto import control_pb2, control_pb2_grpc

channel = grpc.insecure_channel('localhost:50061')
stub = control_pb2_grpc.ControlServiceStub(channel)
req = control_pb2.DecisionRequest(agent_id='test', state=b'hello')
resp = stub.RequestDecision(req, timeout=5)
print('operators:', [(o.id, o.description, o.utility) for o in resp.operators])

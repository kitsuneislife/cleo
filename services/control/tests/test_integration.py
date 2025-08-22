import threading
import time

from services.control import server as control_server
from services.worldmodel import server as wm_server
from services.execution import server as exec_server

import grpc
from proto import control_pb2_grpc, control_pb2


def start_servers():
    # use high ports to reduce risk of collisions on developer machines
    import os
    os.environ['WORLD_MODEL_HOST'] = 'localhost'
    os.environ['WORLD_MODEL_PORT'] = '55163'
    threading.Thread(target=wm_server.serve, kwargs={"port":55163}, daemon=True).start()
    threading.Thread(target=exec_server.serve, kwargs={"port":55164}, daemon=True).start()
    threading.Thread(target=control_server.serve, kwargs={"port":55161}, daemon=True).start()


def test_control_worldmodel_integration():
    start_servers()
    time.sleep(2)
    # Call control RequestDecision
    channel = grpc.insecure_channel('localhost:55161')
    stub = control_pb2_grpc.ControlServiceStub(channel)
    req = control_pb2.DecisionRequest(agent_id='int_test', timestamp=int(time.time()), state=b'{}')
    resp = stub.RequestDecision(req)
    # Expect a DecisionResponse with operators
    assert hasattr(resp, 'operators')
    assert len(resp.operators) >= 1
    # Check worldmodel recorded the call
    assert len(wm_server.calls) >= 1

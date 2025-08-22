import threading
import time
import grpc
from proto import control_pb2_grpc, control_pb2

from services.control import server as control_server
from services.worldmodel import server as wm_server
from services.execution import server as exec_server


def test_full_flow_runs():
    threading.Thread(target=wm_server.serve, kwargs={"port":55163}, daemon=True).start()
    threading.Thread(target=exec_server.serve, kwargs={"port":55164}, daemon=True).start()
    threading.Thread(target=control_server.serve, kwargs={"port":55161}, daemon=True).start()
    time.sleep(1)
    channel = grpc.insecure_channel('localhost:55161')
    stub = control_pb2_grpc.ControlServiceStub(channel)
    req = control_pb2.DecisionRequest(agent_id='agent_full', timestamp=int(time.time()), state=b'{}')
    resp = stub.RequestDecision(req)
    assert len(resp.operators) >= 1
    # call apply action
    action_req = control_pb2.ActionRequest(operator_id=resp.operators[0].id, params=b'{}')
    ack = stub.ApplyAction(action_req)
    assert ack.ok

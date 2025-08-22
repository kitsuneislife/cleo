import threading
import time
import grpc

try:
    from proto import worldmodel_pb2_grpc, worldmodel_pb2
except Exception:
    worldmodel_pb2 = None
    worldmodel_pb2_grpc = None


def _start_wm():
    # start the stub server on a high port to avoid collisions in CI
    import services.worldmodel.server as wm

    wm.serve(port=55163)


def test_worldmodel_predict_smoke():
    t = threading.Thread(target=_start_wm, daemon=True)
    t.start()
    time.sleep(0.2)
    channel = grpc.insecure_channel('localhost:55163')
    stub = worldmodel_pb2_grpc.WorldModelStub(channel)
    req = worldmodel_pb2.PredictRequest(agent_id='test', state=b'test')
    resp = stub.Predict(req, timeout=2)
    assert resp.prediction == b'fake_pred'

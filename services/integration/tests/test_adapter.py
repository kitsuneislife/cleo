from fastapi.testclient import TestClient

import services.integration.adapter as adapter


class _FakeOp:
    def __init__(self, id='op1', description='do something', utility=1.0):
        self.id = id
        self.description = description
        self.utility = utility


class _FakeResp:
    def __init__(self, ops):
        self.operators = ops


class _FakeStub:
    def RequestDecision(self, req, timeout=None):
        return _FakeResp([_FakeOp()])


def test_adapter_observe_monkeypatch(monkeypatch):
    # monkeypatch stub factory
    monkeypatch.setattr(adapter, '_get_control_stub', lambda: _FakeStub())
    client = TestClient(adapter.app)
    resp = client.post('/observe', json={'agent_id': 'a1', 'state': 'aGVsbG8='})
    assert resp.status_code == 200
    j = resp.json()
    assert j['operator_id'] == 'op1'

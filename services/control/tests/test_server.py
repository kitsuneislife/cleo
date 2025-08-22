from services.control.server import ControlService

def test_control_decision_loop():
    svc = ControlService()
    res = svc.decision_loop({'state': 'dummy'})
    assert isinstance(res, dict)
    assert 'action' in res
    assert res['action'] == 'noop'

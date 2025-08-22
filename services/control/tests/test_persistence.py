from services.control.store import DecisionStore


def test_store_save_and_get():
    store = DecisionStore(db_path=':memory:')
    ops = [{"id": "op_move", "description": "move", "utility": 0.9}]
    store.save_decision('agent1', b'{}', ops)
    recent = store.get_recent('agent1')
    assert isinstance(recent, list)
    assert len(recent) == 1
    assert recent[0][0]['id'] == 'op_move'
    store.close()

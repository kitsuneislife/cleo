from services.aiid.store import record_incident, read_incidents
import uuid

def test_record_and_read_incident(tmp_path, monkeypatch):
    # Redirect AIID_FILE to tmp_path
    import services.aiid.store as s
    monkeypatch.setattr(s, 'AIID_FILE', tmp_path / 'aiid.jsonl')
    incident = {'id': str(uuid.uuid4()), 'timestamp': '2025-01-01T00:00:00Z', 'service': 'test', 'level': 'ERROR', 'context': {}}
    assert record_incident(incident)
    incs = read_incidents()
    assert len(incs) == 1
    assert incs[0]['service'] == 'test'

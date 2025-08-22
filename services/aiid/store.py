"""Simple AIID store: append-only JSONL for incidents (local file backend).
"""
import json
from pathlib import Path

AIID_FILE = Path('artifacts/aiid.jsonl')
AIID_FILE.parent.mkdir(parents=True, exist_ok=True)

def record_incident(incident: dict):
    with AIID_FILE.open('a', encoding='utf-8') as f:
        f.write(json.dumps(incident, ensure_ascii=False) + '\n')
    return True

def read_incidents():
    if not AIID_FILE.exists():
        return []
    with AIID_FILE.open('r', encoding='utf-8') as f:
        return [json.loads(l) for l in f if l.strip()]

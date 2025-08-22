import sqlite3
import json
import time
from typing import List, Dict, Any

class DecisionStore:
    def __init__(self, db_path: str = None):
        # default DB inside services/control
        self.db_path = db_path or './services/control/control.db'
        self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._ensure_table()

    def _ensure_table(self):
        cur = self._conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS decisions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_id TEXT,
                ts INTEGER,
                state BLOB,
                operators TEXT
            )
        ''')
        self._conn.commit()

    def save_decision(self, agent_id: str, state: bytes, operators: List[Dict[str, Any]]):
        cur = self._conn.cursor()
        cur.execute('INSERT INTO decisions (agent_id, ts, state, operators) VALUES (?, ?, ?, ?)',
                    (agent_id, int(time.time()), state, json.dumps(operators)))
        self._conn.commit()

    def get_recent(self, agent_id: str, limit: int = 10):
        cur = self._conn.cursor()
        cur.execute('SELECT operators FROM decisions WHERE agent_id = ? ORDER BY ts DESC LIMIT ?', (agent_id, limit))
        rows = cur.fetchall()
        result = []
        for (ops_json,) in rows:
            try:
                result.append(json.loads(ops_json))
            except Exception:
                continue
        return result

    def close(self):
        try:
            self._conn.close()
        except Exception:
            pass

"""Verify presence of key code items and run quick tests where applicable."""
import os
from pathlib import Path
import subprocess

FILES = [
    'services/control/server.py',
    'services/control/tests/test_server.py',
    'services/htn/planner.py',
    'services/goap/planner.py',
    'proto/planning.proto',
    'services/icm/icm.py',
    'services/aiid/store.py',
    'services/memory/interface.py'
]

if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    missing = []
    for f in FILES:
        p = root / f
        if not p.exists():
            missing.append(f)
    print('Missing files:', missing)
    print('Running pytest (quick run)...')
    subprocess.run([os.path.join(root, '.venv', 'Scripts', 'python.exe'), '-m', 'pytest', '-q'])

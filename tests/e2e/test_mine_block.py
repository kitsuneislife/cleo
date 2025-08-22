import subprocess
import time
import re
import os
import sys
import urllib.request
import urllib.error
import json
import threading
import signal
import socket
import importlib.util
import os

# Load mock_control module directly from file to avoid package import issues
_this_dir = os.path.dirname(__file__)
_mock_path = os.path.join(_this_dir, 'mock_control.py')
spec = importlib.util.spec_from_file_location('_mock_control_e2e', _mock_path)
mock_control = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mock_control)
mock_control_serve = mock_control.serve

ADAPTER_SERVICE = 'adapter'
BOT_SERVICE = 'mineflayer-bot'


def run(cmd, **kwargs):
    print('RUN:', cmd)
    return subprocess.run(cmd, shell=True, check=False, capture_output=True, text=True, **kwargs)


def wait_for_adapter(timeout=60):
    deadline = time.time() + timeout
    url = 'http://localhost:8001/health'
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=5) as resp:
                body = resp.read().decode('utf-8')
                if resp.getcode() == 200:
                    try:
                        j = json.loads(body)
                    except Exception:
                        j = body
                    print('adapter /health OK:', j)
                    return True
        except urllib.error.HTTPError as e:
            print('adapter returned HTTP error, not ready yet:', e)
        except urllib.error.URLError as e:
            print('adapter not ready yet:', e)
        except Exception as e:
            print('adapter not ready yet (unexpected):', e)
    time.sleep(1)
    return False


def test_e2e_mine_block():
    # Start a local mock control server on a free port and point the adapter to it
    # find a free port
    s = socket.socket()
    s.bind(('127.0.0.1', 0))
    mock_port = s.getsockname()[1]
    s.close()

    stop_event = threading.Event()
    mock_thread = threading.Thread(target=mock_control_serve, kwargs={'port': mock_port, 'stop_event': stop_event}, daemon=True)
    mock_thread.start()

    # export env so adapter in compose will talk to the mock control on host.docker.internal
    os.environ['CONTROL_HOST'] = 'host.docker.internal'
    os.environ['CONTROL_PORT'] = str(mock_port)

    # Ensure compose stack is up
    r = run('docker compose up -d --build')
    assert r.returncode == 0, f"compose up failed: {r.stderr}"

    # wait for adapter readiness
    ok = wait_for_adapter(timeout=180)
    assert ok, 'adapter readiness failed'

    # run the e2e bot script inside the mineflayer-bot container
    # It should exit with code 0 after mining
    cmd = 'docker compose run --rm mineflayer-bot node e2e_mine_block.js'
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    # monitor adapter logs for the mined_block event
    deadline = time.time() + 120
    found = False
    while time.time() < deadline:
        logs = run('docker compose logs --no-color --tail 200 adapter')
        if logs.returncode == 0:
            if 'mined_block' in logs.stdout:
                found = True
                break
        time.sleep(2)

    # ensure the bot process ended
    try:
        ret = p.wait(timeout=5)
    except subprocess.TimeoutExpired:
        p.kill()
        ret = -1

    # cleanup mock control
    stop_event.set()
    mock_thread.join(timeout=2)

    assert found, 'mined_block event not found in adapter logs'
    assert ret == 0, f'bot process exited with {ret}'

import subprocess
import time
import re
import os
import sys

ADAPTER_SERVICE = 'adapter'
BOT_SERVICE = 'mineflayer-bot'


def run(cmd, **kwargs):
    print('RUN:', cmd)
    return subprocess.run(cmd, shell=True, check=False, capture_output=True, text=True, **kwargs)


def wait_for_adapter(timeout=120):
    deadline = time.time() + timeout
    url = 'http://localhost:8001/health'
    while time.time() < deadline:
        try:
            import requests
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                print('adapter /health OK:', r.json())
                return True
        except Exception as e:
            print('adapter not ready yet:', e)
        time.sleep(2)
    return False


def test_e2e_mine_block():
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

    assert found, 'mined_block event not found in adapter logs'
    assert ret == 0, f'bot process exited with {ret}'

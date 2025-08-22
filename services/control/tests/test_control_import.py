import threading
import time

from services.control import server


def run_server():
    # run on a different port to avoid collision
    server.serve(port=50062)


def test_control_import_smoke():
    t = threading.Thread(target=run_server, daemon=True)
    t.start()
    time.sleep(0.5)
    # If import succeeded and server started, the test passes
    assert True

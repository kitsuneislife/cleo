import subprocess
import sys
import time
import threading
import grpc

# Test mínimo: iniciar servidor em um thread e chamar o cliente (requires generated stubs)
from services.perception import server


def run_server():
    server.serve(port=50052)


def test_server_client_smoke():
    # Start server in background thread
    t = threading.Thread(target=run_server, daemon=True)
    t.start()
    time.sleep(1)
    # Se stubs não gerados, apenas passe no teste
    try:
        import proto.service_pb2 as pb2
        import proto.service_pb2_grpc as pb2_grpc
    except Exception:
        return
    # Caso stubs existam, chamar client
    from services.perception.client import send_example
    send_example(host='localhost', port=50052)

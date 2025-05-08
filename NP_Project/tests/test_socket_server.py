import socket
import json
import threading
import time
import pytest
from server.socket_server import start_server

HOST, PORT = "127.0.0.1", 65433  # test on a different port

@pytest.fixture(scope="module", autouse=True)
def socket_server():
    # Launch the socket server in background on a test port
    thread = threading.Thread(
        target=start_server,
        kwargs={"host": HOST, "port": PORT},
        daemon=True
    )
    thread.start()
    time.sleep(0.2)  # give it a moment to bind
    yield
    # daemon thread will exit when tests end

def send_request(req_obj):
    with socket.socket() as sock:
        sock.connect((HOST, PORT))
        sock.sendall(json.dumps(req_obj).encode())
        resp = sock.recv(4096)
    return json.loads(resp.decode())

def test_socket_success():
    req = {
        "nodes": ["A","B","C","D"],
        "edges": [["A","B",2], ["B","C",3], ["C","D",1]],
        "source": "A",
        "target": "D",
        "K": 1
    }
    resp = send_request(req)
    assert "paths" in resp
    assert isinstance(resp["paths"], list)
    assert resp["paths"][0]["cost"] == 6

def test_socket_error():
    req = {"invalid": "payload"}
    resp = send_request(req)
    assert "error" in resp

import socket
import json

HOST = '127.0.0.1'
PORT = 65432

req = {
    "nodes": ["A","B","C","D"],
    "edges": [["A","B",2], ["B","C",3], ["A","C",5], ["C","D",1]],
    "source": "A",
    "target": "D",
    "K": 3
}
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(json.dumps(req).encode())
    data = s.recv(4096)
    resp = json.loads(data.decode())
    print(resp)
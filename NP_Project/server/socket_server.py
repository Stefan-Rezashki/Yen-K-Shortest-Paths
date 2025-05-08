import socket
import threading
import json
from server.graph_builder import build_graph
from server.yen import yen_k_shortest_paths

HOST_DEFAULT = '0.0.0.0'
PORT_DEFAULT = 65432


def handle_client(conn: socket.socket, addr):
    print(f"Connected by {addr}")
    with conn:
        try:
            data = conn.recv(4096)
            if not data:
                return
            req = json.loads(data.decode())
            nodes = req.get('nodes')
            edges = req.get('edges')
            source = req.get('source')
            target = req.get('target')
            k = req.get('K')

            G = build_graph(nodes, edges)
            results = yen_k_shortest_paths(G, source, target, k)
            response = { 'paths': [ {'route': path, 'cost': cost} for path, cost in results ] }
            conn.sendall(json.dumps(response).encode())
        except Exception as e:
            error = { 'error': str(e) }
            conn.sendall(json.dumps(error).encode())


def start_server(host: str = HOST_DEFAULT, port: int = PORT_DEFAULT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Socket server listening on {host}:{port}")
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            thread.start()

if __name__ == '__main__':
    start_server()
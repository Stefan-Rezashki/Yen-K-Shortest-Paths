# Yen K-Shortest-Paths

A Python implementation of Yen’s K-shortest-paths algorithm, exposed via both a FastAPI HTTP API and a threaded raw TCP socket server. Includes example clients and comprehensive tests.

---

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [HTTP API (FastAPI)](#http-api-fastapi)
  - [Socket Server](#socket-server)
  - [Clients](#clients)
- [Testing](#testing)
- [License](#license)

---

## Features

- **Yen’s algorithm** for finding the K shortest simple paths in a directed graph  
- **FastAPI HTTP server** with `/yen` endpoint  
- **Threaded TCP socket server** for raw-socket clients  
- **Example clients** for HTTP (requests) and sockets  
- **Automated tests** using pytest for algorithm, HTTP API, and socket server  

---

## Project Structure

```
NP_Project/
├── server/                 # Server-side implementation
│   ├── __init__.py
│   ├── models.py           # Pydantic models for requests/responses
│   ├── graph_builder.py    # Build NetworkX directed graph
│   ├── yen.py              # Yen’s K-shortest-paths algorithm
│   ├── main.py             # FastAPI HTTP API server
│   └── socket_server.py    # Threaded raw TCP socket server
└── client/                 # Client usage examples
    ├── main.py             # HTTP API client (requests)
    └── socket_client.py    # Socket server client

tests/                      # Pytest test suite
└── ...
```

---

## Requirements

- Python 3.8+  
- Dependencies listed in `requirements.txt`:
  ```text
  fastapi
  uvicorn[standard]
  networkx
  pydantic
  requests
  pytest
  httpx
  ```

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Stefan-Rezashki/Yen-K-Shortest-Paths
   cd yen_k_shortest
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # Windows PowerShell:
   Set-ExecutionPolicy -Scope Process Bypass; .\.venv\Scripts\Activate.ps1
   # macOS/Linux:
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### HTTP API (FastAPI)

Start the FastAPI server:
```bash
uvicorn server.main:app --reload --host 0.0.0.0 --port 8000
```

**Endpoint**: `POST /yen`  
**Request JSON**:
```json
{
  "nodes": ["A", "B", "C", ...],
  "edges": [["A","B",2.5], ["B","C",1.2], ...],
  "source": "A",
  "target": "C",
  "K": 3
}
```
**Response JSON**:
```json
{
  "paths": [
    { "route": ["A","B","C"], "cost": 3.7 },
    { "route": ["A","C"],     "cost": 5.0 },
    ...
  ]
}
```

---

### Socket Server

Start the threaded TCP server:
```bash
python -m server.socket_server
```

By default it listens on `0.0.0.0:65432`. Clients send the same JSON payload over the socket and receive the JSON response.

---

### Clients

- **HTTP client** (`client/main.py`): uses `requests` to call the `/yen` endpoint.  
- **Socket client** (`client/socket_client.py`): opens a TCP connection, sends JSON, and prints the response.

Run either with:
```bash
python client/main.py
python client/socket_client.py
```

---

## Testing

Run the full test suite with pytest:
```bash
pytest -q
```

This covers:
- Unit tests for the DAG and Yen implementation  
- FastAPI endpoint tests using TestClient  
- Socket server tests on a temporary port  


---

## License

MIT License. See LICENSE for details.


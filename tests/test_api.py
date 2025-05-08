import pytest
from fastapi.testclient import TestClient
from server.main import app

client = TestClient(app)

def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json() == {"message": "Welcome to the Yen K-Shortest-Paths API"}

def test_yen_endpoint_success():
    payload = {
        "nodes": ["A","B","C","D"],
        "edges": [["A","B",2], ["B","C",3], ["A","C",5], ["C","D",1]],
        "source": "A",
        "target": "D",
        "K": 2
    }
    r = client.post("/yen", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert len(data["paths"]) == 2
    # first path cost should be A→B→C→D = 2+3+1 = 6
    assert data["paths"][0]["cost"] == 6

def test_yen_endpoint_not_found():
    # no path from X to Y
    payload = {"nodes":["X","Y"], "edges":[], "source":"X","target":"Y","K":1}
    r = client.post("/yen", json=payload)
    assert r.status_code == 404

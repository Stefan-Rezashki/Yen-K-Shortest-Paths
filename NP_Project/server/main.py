from fastapi import FastAPI, HTTPException
from server.models import YenRequest, YenResponse, PathResult
from server.graph_builder import build_graph
from server.yen import yen_k_shortest_paths

app = FastAPI()

@app.post("/yen", response_model=YenResponse)
def compute_yen(req: YenRequest):
    G = build_graph(req.nodes, req.edges)
    results = yen_k_shortest_paths(G, req.source, req.target, req.K)
    if not results:
        raise HTTPException(status_code=404, detail="No path found")
    return YenResponse(
        paths=[PathResult(route=path, cost=cost) for path, cost in results]
    )

@app.get("/")
def read_root():
    return {"message": "Welcome to the Yen K-Shortest-Paths API"}
# server/models.py
from pydantic import BaseModel
from typing import List, Tuple

class YenRequest(BaseModel):
    nodes: List[str]
    edges: List[Tuple[str, str, float]]
    source: str
    target: str
    K: int

class PathResult(BaseModel):
    route: List[str]
    cost: float

class YenResponse(BaseModel):
    paths: List[PathResult]
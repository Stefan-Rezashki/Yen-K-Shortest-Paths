# server/graph_builder.py
import networkx as nx
from typing import List, Tuple

def build_graph(nodes: List[str], edges: List[Tuple[str, str, float]]) -> nx.DiGraph:
    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)
    return G
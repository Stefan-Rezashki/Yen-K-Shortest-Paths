import networkx as nx
import pytest
from server.yen import yen_k_shortest_paths

@pytest.fixture
def simple_graph():
    G = nx.DiGraph()
    G.add_weighted_edges_from([
        ("A", "B", 1),
        ("B", "C", 2),
        ("A", "C", 5),
    ])
    return G

def test_k_equals_zero(simple_graph):
    assert yen_k_shortest_paths(simple_graph, "A", "C", 0) == []

def test_no_path(simple_graph):
    G = simple_graph.copy()
    G.remove_edge("A", "B")
    G.remove_edge("A", "C")
    assert yen_k_shortest_paths(G, "A", "C", 3) == []

def test_shortest_and_second_shortest(simple_graph):
    paths = yen_k_shortest_paths(simple_graph, "A", "C", 2)
    # first: A→B→C cost 3, second: A→C cost 5
    assert paths[0][1] == 3
    assert paths[1][1] == 5

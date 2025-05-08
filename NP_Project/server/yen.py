import networkx as nx
import heapq
from typing import List, Tuple

def path_cost(
    G: nx.DiGraph, path: List[str], weight: str = 'weight'
) -> float:
    """
    Calculate the total cost of a path in graph G using the given weight attribute.
    """
    return sum(G[u][v].get(weight, 1) for u, v in zip(path, path[1:]))


def yen_k_shortest_paths(
    G: nx.DiGraph,
    source: str,
    target: str,
    k: int,
    weight: str = 'weight'
) -> List[Tuple[List[str], float]]:

    # Basic validation
    if k <= 0:
        return []
    if source not in G or target not in G:
        return []

    # First shortest path (base case)
    try:
        first_path = nx.dijkstra_path(G, source, target, weight=weight)
    except nx.NetworkXNoPath:
        return []

    shortest_paths: List[Tuple[List[str], float]] = [
        (first_path, path_cost(G, first_path, weight))
    ]
    # Min-heap of (cost, path) candidates for next shortest paths
    candidates: List[Tuple[float, List[str]]] = []


    for path_index in range(1, k):
        # The previous shortest path found
        previous_path, _ = shortest_paths[path_index - 1]

        # Iterate over each spur node in the previous path
        for spur_index in range(len(previous_path) - 1):
            spur_node = previous_path[spur_index]
            root_path = previous_path[: spur_index + 1]

            # Work on a copy of the original graph for spur path search
            G_spur = G.copy()

            # Remove edges that would create previously found root paths
            for pth, _ in shortest_paths:
                if len(pth) > spur_index and pth[: spur_index + 1] == root_path:
                    u, v = pth[spur_index], pth[spur_index + 1]
                    if G_spur.has_edge(u, v):
                        G_spur.remove_edge(u, v)

            # Remove root path nodes except the spur node to avoid loops
            for node in root_path[:-1]:
                if G_spur.has_node(node):
                    G_spur.remove_node(node)


            try:
                spur_path = nx.dijkstra_path(G_spur, spur_node, target, weight=weight)
                # Combine root and spur paths, avoiding duplicate spur node
                total_path = root_path + spur_path[1:]
                total_cost = path_cost(G, total_path, weight)
                heapq.heappush(candidates, (total_cost, total_path))
            except nx.NetworkXNoPath:
                # No alternative spur path from this spur node
                continue

        if not candidates:
            # No more candidate paths to explore
            break

        # Select the next shortest path candidate that is not already used
        while candidates:
            cost, path = heapq.heappop(candidates)
            if not any(path == existing for existing, _ in shortest_paths):
                shortest_paths.append((path, cost))
                break

    return shortest_paths

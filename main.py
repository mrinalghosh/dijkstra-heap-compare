# import matplotlib.pyplot as plt
# import numpy as np
from heaps.fibonacci import FibHeap
import sys

from networkx.algorithms.shortest_paths.unweighted import predecessor

sys.path.append(".")
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import heapq
from icecream import ic


def convert_graph(G: nx.DiGraph) -> dict:
    # Converts adjacency list for networkx graph into adjacency list dictionary
    nx_adjlist = [(n, nbrdict) for n, nbrdict in G.adjacency()]
    graph = {}
    for t in nx_adjlist:
        graph[t[0]] = {obj: t[1][obj]["weight"] for obj in t[1]}
    return graph


def dijkstra_path_heaps(G: nx.DiGraph, source, target, weight="weight", heap="FibHeap"):
    """
    Returns the shortest weighted path from source to target in G.
        Uses Dijkstra's Method to compute the shortest weighted path
        between two nodes in a graph.

        Parameters
        ----------
        G : NetworkX graph

        source : node
        Starting node

        target : node
        Ending node

        weight : string or function

        heap : string
            Heap implementation to use for priority queue

        Returns
        -------
        path : list
        List of nodes in a shortest path.

        Raises
        ------
        NodeNotFound
            If `source` is not in `G`.

        NetworkXNoPath
        If no path exists between source and target.
    """
    graph = convert_graph(G)
    queue = [(0, source)]
    distances = {source: 0}
    visited = set()
    predecessor = dict.fromkeys(G.nodes)
    heap = FibHeap()
    heap.insert(0, source)

    while queue:
        _, node = heapq.heappop(queue)  # (distance, node), ignore distance
        if node in visited:
            continue
        visited.add(node)
        dist = distances[node]
        for neighbour, neighbour_dist in graph[node].items():
            if neighbour in visited:
                continue
            neighbour_dist += dist
            if neighbour_dist < distances.get(neighbour, float("inf")):
                predecessor[neighbour] = node
                heapq.heappush(queue, (neighbour_dist, neighbour))
                distances[neighbour] = neighbour_dist
    
    pred = predecessor[target]
    path = []
    path.append(target)
    while pred is not None:
        path.append(pred)
        pred = predecessor[pred]
    path.reverse()
    return path


if __name__ == "__main__":

    A = [
        [0, 4, 2, 0, 0, 0],
        [4, 0, 1, 5, 0, 0],
        [2, 1, 0, 8, 10, 0],
        [0, 5, 8, 0, 2, 6],
        [0, 0, 10, 2, 0, 5],
        [0, 0, 0, 6, 5, 0],
    ]
    mapping = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "z"}

    G = nx.from_numpy_matrix(np.matrix(A), create_using=nx.DiGraph)
    G = nx.relabel_nodes(G, mapping)
    layout = nx.spring_layout(G)
    nx.draw(G, layout, with_labels=True)
    # path = nx.dijkstra_path(G, source="a", target="z")
    # print(path)
    path = dijkstra_path_heaps(G, source="a", target="z")
    print(path)
    path_edges = zip(path, path[1:])
    labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos=layout, edge_labels=labels)
    nx.draw_networkx_nodes(G, layout, nodelist=path, node_color="r")
    nx.draw_networkx_edges(
        G, layout, edgelist=list(path_edges), edge_color="r", width=3
    )
    plt.show()

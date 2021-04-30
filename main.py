import sys

sys.path.append(".")
import networkx as nx
import matplotlib.pyplot as plt

from heaps.fibonacci import FibHeap
from heaps.quake import QuakeHeap


def dijkstra_path_heaps(G: nx.DiGraph, source, target, heap_choice):

    if heap_choice == "Fibonacci":
        heap = FibHeap()
    if heap_choice == "Quake":
        heap = QuakeHeap()
    else:
        heap = FibHeap()

    G.nodes["a"]["key"] = 0

    for n in G.nodes:
        G.nodes[n]["node"] = heap.insert(G.nodes[n], n)

    while heap:
        n = heap.extract_min()
        for edge in G.edges(n.name):
            u, v = edge
            dist = G.nodes[u]["key"] + G[u][v]["weight"]
            if G.nodes[v]["key"] > dist:
                G.nodes[v]["key"] = dist
                G.nodes[v]["pred"] = u
                heap.decrease_key(G.nodes[v]["node"], dist)

    path = []
    path.append(target)
    pred = G.nodes[target]["pred"]
    while pred is not None:
        path.append(pred)
        pred = G.nodes[pred]["pred"]
    path.reverse()
    return path


if __name__ == "__main__":
    G = nx.Graph()

    G.add_node("a")
    G.add_node("b")
    G.add_node("c")
    G.add_node("d")
    G.add_node("e")
    G.add_node("z")

    nx.set_node_attributes(G, float("inf"), "key")
    nx.set_node_attributes(G, None, "pred")
    nx.set_node_attributes(G, None, "node")

    G.add_edge("a", "b", weight=4)
    G.add_edge("a", "c", weight=2)
    G.add_edge("b", "c", weight=1)
    G.add_edge("b", "d", weight=5)
    G.add_edge("c", "d", weight=8)
    G.add_edge("c", "e", weight=10)
    G.add_edge("d", "e", weight=2)
    G.add_edge("d", "z", weight=6)
    G.add_edge("e", "z", weight=5)

    layout = nx.spring_layout(G)
    nx.draw(G, layout, with_labels=True)

    # path = nx.dijkstra_path(G, source="a", target="z")
    # print(path)

    path = dijkstra_path_heaps(G, source="a", target="z", heap_choice="Quake")
    print(path)

    path_edges = zip(path, path[1:])
    labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos=layout, edge_labels=labels)
    nx.draw_networkx_nodes(G, layout, nodelist=path, node_color="r")
    nx.draw_networkx_edges(
        G, layout, edgelist=list(path_edges), edge_color="r", width=3
    )
    plt.show()
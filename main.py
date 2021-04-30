import sys

sys.path.append(".")
import timeit
import networkx as nx
import matplotlib.pyplot as plt

from test_graphs.graph_generator import *
from heaps.fibonacci import FibHeap
from heaps.violation import ViolationHeap
#from heaps.min import MinHeap
#from heaps.quake import QuakeHeap


#HEAPS = ["Fibonacci", "Violation", "Rank_Pairing", "Quake", "Min"]
#HEAPS = ["Fibonacci", "Violation"]
HEAPS = ["Fibonacci"]

def get_heap(heap_choice):
    """Get specified heap instance."""
    if heap_choice == "Fibonacci":
        heap = FibHeap()
    elif heap_choice == "Violation":
        heap = ViolationHeap()
    elif heap_choice == "Min":
        heap = MinHeap()
    elif heap_choice == "QuakeHeap":
        heap = QuakeHeap()
    elif heap_choice == "RankPairingHeap":
        heap = RankPairingHeap()
    
    return heap


def visualize_graph(graph, path, show=True, labels=True, layout_type="spring"):
    """Visualize a Networkx graph object."""
    nx.draw(graph, with_labels=labels, pos=getattr(nx, f"{layout_type}_layout")(graph))
    
    path_edges = zip(path, path[1:])
    edge_labels = nx.get_edge_attributes(G, "weight")

    nx.draw_networkx_edge_labels(G, pos=layout, edge_labels=edge_labels)
    nx.draw_networkx_nodes(G, layout, nodelist=path, node_color="r")
    nx.draw_networkx_edges(G, layout, edgelist=list(path_edges), edge_color="r", width=3)

    if show:
        plt.show()


def sanity_check(heap_choice="Fibonacci"):
    """Quick sanity check for dijkstra implementation"""
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

    path = dijkstra_path_heaps(G, source="a", target="z", heap_choice="Fibonacci")
    if not path:
        raise Exception(f"{heap_choice} did not find a path!!")
        
    visualize_graph(G, path)


def smoke_tests():
    """Run sanity check for each heap."""
    for heap in HEAPS:
        try:
            sanity_check(heap)
        except:
            print(f"{heap} heap failed running the sanity check!")


def dijkstra_path_heaps(G: nx.DiGraph, source, target, heap):
    """Dijkstra's Algorithm Implementation"""
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


def dijkstra_time(heap, source, target):
    """Compute Dijkstra's shortest path time."""
    
    # TODO

    return times


def get_search_nodes(G):
    """Get the source and target by getting the most distanced node pair."""
    source = None
    target = None
    
    max_len = -1
    length = dict(nx.all_pairs_dijkstra_path_length(G))
    
    # Search through to see which pair has greatest distance
    for node_a in length:
        for node_b in length[node_a]:
            if length[node_a][node_b] > max_len:
                max_len = length[node_a][node_b]
                source = node_a
                target = node_b
    
    return source, target


def performance_test():
    """Benchmarking Dijkstra with all heaps and graphs."""
    
    # Get the graphs
    test_graphs = get_graphs_from_file()
    
    results = {}
    for heap_name in HEAPS:
        run_info = {}
        for graph in test_graphs:
            source, target = get_search_nodes(graph)
            
            # Run Dijktra
            run_info["time_info"] = dijkstra_time(get_heap(heap_name), source, target)
            
            # Record graph info
            run_info['graph_info'] = [1, 2, 3] # TODO

            # Add the results
            results[heap_name] = run_info

    return results

if __name__ == "__main__":
    
    # Run sanity checks
    smoke_tests()

    # Run performance tests
    performance_test()

    



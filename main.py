import sys

sys.path.append(".")
import time
import networkx as nx
import matplotlib.pyplot as plt
import csv
from hwcounter import count, count_end

from statistics import mean
from test_graphs.graph_generator import *
from heaps.fibonacci import FibHeap
from heaps.violation import ViolationHeap
from heaps.quake import QuakeHeap
from heaps.minheap import MinHeap

# from heaps.rankpairing import RankPairingHeap


HEAPS = ["Quake", "Fibonacci", "Violation", "MinHeap"]
# HEAPS = ["Quake", "Fibonacci", "Violation", "MinHeap", "RankPairing"]


def get_heap(heap_choice):
    """Get specified heap instance."""
    if heap_choice == "Fibonacci":
        heap = FibHeap()
    elif heap_choice == "Violation":
        heap = ViolationHeap()
    elif heap_choice == "MinHeap":
        heap = MinHeap()
    elif heap_choice == "Quake":
        heap = QuakeHeap()
    # elif heap_choice == "RankPairing":
    #     heap = RankPairingHeap()
    else:
        raise NameError(f"{heap_choice} does not exist")

    return heap


def dijkstra_path_heaps(G, source, target, heap):
    """Dijkstra's Algorithm Implementation"""
    G.nodes[source]["key"] = 0

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


def visualize_graph(G, path, heap_choice, show=True, labels=True, layout_type="spring"):
    """Visualize a Networkx graph object."""
    layout = getattr(nx, f"{layout_type}_layout")(G)
    nx.draw(G, with_labels=labels, pos=layout)

    path_edges = zip(path, path[1:])
    edge_labels = nx.get_edge_attributes(G, "weight")

    nx.draw_networkx_edge_labels(G, pos=layout, edge_labels=edge_labels)
    nx.draw_networkx_nodes(G, layout, nodelist=path, node_color="r")
    nx.draw_networkx_edges(
        G, layout, edgelist=list(path_edges), edge_color="r", width=3
    )

    plt.title(heap_choice)
    plt.savefig(f"{heap_choice}.png")
    if show:
        plt.show()


def sanity_check(heap_choice="Fibonacci", show=False):
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

    heap = get_heap(heap_choice)
    path = dijkstra_path_heaps(G=G, source="a", target="z", heap=heap)
    if not path:
        raise Exception(f"{heap_choice} did not find a path!!")

    if show:
        visualize_graph(G, path, heap_choice)


def smoke_tests(show=False):
    """Run sanity check for each heap."""
    for heap in HEAPS:
        try:
            sanity_check(heap, show)
        except:
            print(f"{heap} heap failed running the sanity check!")


def dijkstra_time(G, source, target, heap):
    """Compute Dijkstra's shortest path time."""
    repeat = 3
    runs = 10
    times = []
    cycles = []

    # Add Graph attrs
    nx.set_node_attributes(G, float("inf"), "key")
    nx.set_node_attributes(G, None, "pred")
    nx.set_node_attributes(G, None, "node")

    dijkstra_results = {}
    # Run Dijkstra's
    for _ in range(repeat):
        t0 = time.time()
        c0 = count()
        for _ in range(runs):
            dijkstra_results[G] = dijkstra_path_heaps(G, source, target, heap)
        c1 = count_end()
        t1 = time.time()
        times.append(t1 - t0)
        cycles.append(c1 - c0)

    # Get the results and pass them back
    results = {
        "runs": runs,
        "repeat": repeat,
        "avg_time": mean(times),
        "avg_cycles": round(mean(cycles)),
        "algo_res": dijkstra_results,
    }

    return results


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
        print(f"Running: {heap_name}")
        run_list = []
        graph_count = 0
        for G in test_graphs:
            run_info = {}
            source, target = get_search_nodes(G)

            # Run Dijktra
            run_info["time_info"] = dijkstra_time(
                G, source, target, get_heap(heap_name)
            )

            # Record graph info
            run_info["graph_info"] = {
                "graph_obj": G,
                "graph_num": graph_count,
                "num_nodes": G.number_of_nodes(),
                "num_edges": G.number_of_edges(),
            }

            print(
                "graph: {}, num_nodes: {}, num_edges: {}, avg_time: {}, avg_cycles: {}, path_found = {}".format(
                    graph_count,
                    run_info["graph_info"]["num_nodes"],
                    run_info["graph_info"]["num_edges"],
                    run_info["time_info"]["avg_time"],
                    run_info["time_info"]["avg_cycles"],
                    run_info["time_info"]["algo_res"][G],
                )
            )

            # Add the run info into list
            run_list.append(run_info)
            graph_count += 1

        print(f"Done running for each graph: {heap_name}")
        # Add the results
        results[heap_name] = run_list

    return results


def report(results):
    fields = ["num_nodes", "num_edges", "avg_time", "avg_cycles"]
    rows = []
    paths = []
    for heap in results:
        rows.append([heap])
        rows.append(fields)
        heap_data = results[heap]

        paths.append([heap])
        for run in heap_data:
            graph_info = run["graph_info"]
            num_nodes = graph_info["num_nodes"]
            num_edges = graph_info["num_edges"]
            avg_time = run["time_info"]["avg_time"]
            avg_cycles = run["time_info"]["avg_cycles"]
            rows.append([num_nodes, num_edges, avg_time, avg_cycles])
            path = run["time_info"]["algo_res"].values()
            for item in path:
                paths.append(item)

        rows.append([])
        paths.append([])

    with open("report.csv", "w") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(rows)

    with open("paths.csv", "w") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(paths)


if __name__ == "__main__":

    # Run a sanity check on single heap
    # sanity_check("Fibonacci", show=True)
    # Run sanity checks for all heaps
    # smoke_tests(show=False)

    # Run performance tests
    results = performance_test()
    print("Finished!")

    # Record results into a csv and plot it
    report(results)

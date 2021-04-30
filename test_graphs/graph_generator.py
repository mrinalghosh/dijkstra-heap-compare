import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random
import json
import sys
import os

from networkx.readwrite import json_graph

sys.path.append('.')

MAX_VERTEX_RANGE = (10, 1000)
MAX_EDGE_RANGE = (10, 1000)
MAX_WEIGHT_RANGE = (10, 1000)

GRAPHS_DIR = "./test_graphs"


def create_graph(v_range=MAX_VERTEX_RANGE, e_range=MAX_EDGE_RANGE, w_range=MAX_WEIGHT_RANGE, graph_type="gnm_random_graph"):
    """Create a random graph"""
    
    # Create random selections for verteces and edges
    n = np.random.randint(*v_range)
    p = np.random.randint(*e_range) 

    # Create the graph
    G = getattr(nx, graph_type)(n, p)
    nx.set_node_attributes(G, float("inf"), "key")
    nx.set_node_attributes(G, None, "pred")
    nx.set_node_attributes(G, None, "node")
    if nx.is_connected(G):
        # Create a random weight for each edge
        for (u, v) in G.edges():
            G.edges[u,v]['weight'] = np.random.randint(*w_range)
    
        # Then export the created graph into a JSON file
        adj_data = json_graph.adjacency_data(G)
    
        # Dump to file
        with open(f"./test_graphs/graph_{n}_{p}_{w_range}.json", "w") as outfile:
            json.dump(adj_data, outfile)
    else:
        return False
    
    return G


def generate_graphs(x, graph_type="gnm_random_graph"):
    """Create x number of graphs and return the list of them."""
    graphs = []
    for _ in range(x):
        G = create_graph(MAX_VERTEX_RANGE, MAX_EDGE_RANGE, MAX_WEIGHT_RANGE, graph_type)
        if G:
            graphs.append(G)

    return graphs

def get_graphs_from_file(given_file_name=None):
    """Read the graphs from the test_graphs folder."""
    
    # Grab the list of files from the given directory.
    files = os.listdir(GRAPHS_DIR)

    # Covert the data into a graph object and append it to the list
    graphs = []
    if given_file_name:
        if given_file_name.endswith(".json"):
            with open(f"{GRAPHS_DIR}/{given_file_name}") as f:
                    adj_data = json.load(f)
                    graphs.append(json_graph.adjacency_graph(adj_data))
    else:
        for file in files:
            if file.endswith(".json"):
                with open(f"{GRAPHS_DIR}/{file}") as f:
                    adj_data = json.load(f)
                    graphs.append(json_graph.adjacency_graph(adj_data))

    return graphs

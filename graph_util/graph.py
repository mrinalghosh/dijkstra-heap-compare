''' Base Class for a Graph Object.

This module contains helper functions and base classes for visualization of graphs.

Sources:
https://github.com/reinvald/Dijkstra-Visualizer - NetworkX
'''

import itertools
import networkx as nx
import matplotlib.pyplot as plt


class Vertex(object):
    '''Vertex object for graph representation.'''
    uidc = itertools.count()  # unique id counter

    def __init__(self, distance=float('inf')):
        ''' initialize vertex with provided distance/key and unique ID '''
        self.distance = distance # key
        self.neighbors = {}
        self.pred = None
        self.predweight = None
        self.id = next(self.uidc) # unique ID set during creation/inheritance

    def addNeighbor(self, v, w):
        self.neighbors[v] = self.neighbors.get(v, w)



class Graph(object):
    def __init__(self):
        self.graph = {}

    def addVertex(self, vertex):
        # check if in dict else add vertex to dict
        self.graph[vertex.name] = self.graph.get(vertex.name, vertex)

    def addEdge(self, u, v, w):
        if u in self.graph and v in self.graph:  # only add edges between existing nodes in graph
            self.graph[u].addNeighbor(v, w)

    def show(self):
        G = nx.DiGraph()  # directed graph with self loops

        for name in self.graph.keys():  # add all nodes to graph
            G.add_node(name)

        for u, v in self.graph.items():  # for each vertex
            for n, w in v.neighbors.items():  # for each neighbor
                G.add_edge(u, n, weight=w)

        # shell layout - could be random, spectral_layout, spring_layout or circular_layout
        pos = nx.fruchterman_reingold_layout(G)
        nx.draw(G, pos, with_labels=True)
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        plt.draw()
        plt.show()

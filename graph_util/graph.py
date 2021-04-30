import itertools
import networkx as nx
import matplotlib.pyplot as plt


class Vertex(object):
    '''Vertex object for graph representation.'''
    uidc = itertools.count()  # unique id counter

    def __init__(self, distance=float('inf')):
        ''' initialize vertex with provided distance/key and unique ID '''
        self.distance = distance
        self.neighbors = {}
        self.pred = None
        self.predweight = None
        self.id = next(self.uidc)

    def addNeighbor(self, v, w):
        self.neighbors[v] = self.neighbors.get(v, w)


class Graph(object):
    def __init__(self):
        self.graph = {}

    def addVertex(self, vertex):
        self.graph[vertex.name] = self.graph.get(vertex.name, vertex)

    def addEdge(self, u, v, w):
        if u in self.graph and v in self.graph:
            self.graph[u].addNeighbor(v, w)

    def show(self):
        G = nx.DiGraph()  # directed graph with self loops

        for name in self.graph.keys():
            G.add_node(name)

        for u, v in self.graph.items():
            for n, w in v.neighbors.items():
                G.add_edge(u, n, weight=w)

        # shell layout - could be random, spectral_layout, spring_layout or circular_layout
        pos = nx.fruchterman_reingold_layout(G)
        nx.draw(G, pos, with_labels=True)
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        plt.draw()
        plt.show()

import itertools
import networkx as nx
import matplotlib.pyplot as plt

'''
Sources used:
https://github.com/reinvald/Dijkstra-Visualizer - Dijkstra & NetworkX

Notes:
Edge class integrated into Graph 
all comparison methods for vertices are based on distance
'''


class Vertex(object):
    ''' vertex object for graph representation '''
    uidc = itertools.count()  # unique id counter

    def __init__(self, name=None, distance=float('inf')):
        ''' initialize vertex with provided key and unique ID unless specified '''
        self.name = name or next(Vertex.uidc)
        self.distance = distance  # key for priority queues
        self.neighbors = {}
        self.pred = None
        self.predweight = None

    def addNeighbor(self, v, w):
        self.neighbors[v] = self.neighbors.get(v, w)

    def __lt__(self, other):
        ''' override < method '''
        return self.distance < other.distance

    def __le__(self, other):
        ''' override <= method '''
        return self.distance <= other.distance

    def __gt__(self, other):
        ''' override > method '''
        return self.distance > other.distance

    def __ge__(self, other):
        ''' override >= method '''
        return self.distance >= other.distance

    def __eq__(self, other):
        ''' override == method '''
        return self.distance == other.distance

    def __repr__(self):
        ''' override output method - for debug '''
        return f'{self.distance}'


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

    def Dijkstra(self, src, heap):
        ''' pass in source ID and Heap object of choice '''

        # initialize
        self.graph[src].distance = 0
        for k, v in self.graph.items():
            heap.insert(v) # insert each vertex object into heap

        while len(heap) > 0:
            current = heap.peek()
            for v, w in current.neighbors.items():
                if self.graph[v].distance > current.distance + w:
                    self.graph[v].distance = current.distance + w
                    self.graph[v].parent = current.name
                    self.graph[v].predweight = w
            heap.deleteMin()

        for u, v in self.graph.items():
            print(f'shortest distance( {str(src)}, {str(u)} ) = {str(v.distance)}')

        """ TODO: finish Dijkstra - gives wrong results for 0->1 """

    def __repr__(self):
        return '\n'.join(f'{key}: {value}' for key, value in self.graph.items())

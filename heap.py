import heapq
import itertools
import networkx as nx
import matplotlib.pyplot as plt

'''
Sources used:
https://github.com/reinvald/Dijkstra-Visualizer - Dijkstra & NetworkX
'''

''' Edge class integrated into Graph '''


class Vertex(object):
    ''' vertex object for graph representation '''
    uidc = itertools.count()  # unique id counter

    def __init__(self, name=None, dist=float('inf')):
        ''' initialize vertex with provided key and unique ID unless specified '''
        self.name = name or next(Vertex.uidc)
        self.dist = dist  # key for priority queues
        self.neighbors = {}
        self.pred = None
        self.predweight = None

    def addNeighbor(self, v, w):
        self.neighbors[v] = self.neighbors.get(v, w)

    def __lt__(self, other):
        ''' override < method '''
        return self.dist < other.dist

    def __gt__(self, other):
        ''' override > method '''
        return self.dist > other.dist

    def __repr__(self):
        ''' override output method - for debug '''
        # return f'({self.name}: {self.dist})'
        return f'{self.dist}'


class Graph(object):
    def __init__(self):
        self.graph = {}

    def addVertex(self, vertex):
        # checks if in dict else adds argument vertex
        self.graph[vertex.name] = self.graph.get(vertex.name, vertex)

    def addEdge(self, u, v, w):
        if u in self.graph and v in self.graph:  # only add edges between existing nodes in graph
            self.graph[u].addNeighbor(v, w)

    def show(self):
        G = nx.DiGraph()  # directed graph with self loops

        for name in self.graph.keys():  # add all nodes to graph
            G.add_node(name)

        for s, v in self.graph.items():  # for each vertex
            for n, w in v.neighbors.items():  # for each neighbor
                G.add_edge(s, n, weight=w)

        # shell layout - could be random, spectral_layout, spring_layout or circular_layout
        pos = nx.fruchterman_reingold_layout(G)
        nx.draw(G, pos, with_labels=True)

        plt.draw()
        plt.show()

    def Dijkstra(self, s, heap):
        ''' pass in source ID and Heap object of choice '''

        # initialize
        self.graph[s].dist = 0
        for k, v in self.graph.items():
            heap.push(v)

        while len(heap) > 0:
            u = heap.pop()
            for v, w in u.neighbors.items():
                if self.graph[v].dist > u.dist + w:
                    self.graph[v].dist = u.dist + w
                    self.graph[v].parent = u.name
                    self.graph[v].predweight = w

        for u, v in self.graph.items():
            print(f'dist({str(s)}, {str(u)}) = {str(v.dist)}')

        """ TODO: finish Dijkstra - gives wrong results for 0->1 """

    def __repr__(self):
        return '\n'.join(f'{key}: {value}' for key, value in self.graph.items())


class Heap(object):
    ''' Generic heap class for inheritance '''

    def __init__(self):
        ''' initialize heap specific data structures '''

    def push(self, value):
        ''' insert a new vertex into heap'''
        return NotImplemented

    def pop(self):
        ''' delete minimum '''
        return NotImplemented

    def decreaseKey(self, vertex, key):
        ''' decrease key and maintain heap '''
        return NotImplemented

    def show(self):
        ''' print heap in appropriate format '''
        return NotImplemented

    def __len__(self):
        ''' return number of elements in heap'''
        return NotImplemented


class MinHeap(Heap):
    ''' vanilla min-heap priority queue '''

    def __init__(self):
        ''' maintain heap with underlying list - O(1) append and delete '''
        self.heap = []

    def upHeap(self, pos=None):
        ''' up-heap element at given pos in heap array '''
        child = pos or len(self.heap) - 1
        parent = (child - 1) // 2

        while child and self.heap[child] < self.heap[parent]:
            self.heap[child], self.heap[parent] = self.heap[parent], self.heap[child]
            child = parent
            parent = (child - 1) // 2

    def downHeap(self):
        ''' downheap element '''
        if len(self.heap) < 2:
            return

        item = 0
        while (2*item+1) < len(self.heap):
            child = 2*item+1
            if (2*item+2) < len(self.heap) and self.heap[2*item+2] < self.heap[2*item+1]:
                child = 2*item+2
            if self.heap[child] > self.heap[item]:
                return
            self.heap[child], self.heap[item] = self.heap[item], self.heap[child]
            item = child

    def push(self, value):
        self.heap.append(value)
        self.upHeap()

    def pop(self):
        ''' delete minimum element '''
        if not self.heap:
            return None

        self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]
        data = self.heap.pop()
        self.downHeap()
        return data

    def decreaseKey(self, vertex, key):
        ''' TODO: decrease key - see HW4 '''
        if vertex in self.heap: # TODO: remove O(n) search
            pos = self.heap.index(vertex)
            self.heap[pos].dist = key
            self.upHeap(pos)

    def show(self):
        print(self.heap)

    def __len__(self):
        return len(self.heap)


class HeapqHeap(Heap):
    ''' wrapper class for heapq from Python standard library - used for benchmarking '''

    def __init__(self):
        self.heap = []

    def push(self, value):
        heapq.heappush(self.heap, value)

    def pop(self):
        ''' delete min '''
        return heapq.heappop(self.heap)

    def decreaseKey(self, vertex, value):
        ''' TODO: heapq doesn't have an implementation for this '''
        pass

    def show(self):
        print(self.heap)

    def __len__(self):
        return len(self.heap)

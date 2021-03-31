import heapq
import itertools
import networkx as nx
import matplotlib.pyplot as plt

'''
Sources used:
https://gist.github.com/Tetsuya3850/a271ba66f35460e1e244aacbe792576b - vanilla min-heap
https://github.com/reinvald/Dijkstra-Visualizer - networkx
'''


class Edge(object):
    def __init__(self, u, v, w):
        self.u = u
        self.v = v
        self.w = w

    def __repr__(self):
        return f'{self.u}--{self.w}-->{self.v}'


class Vertex(object):
    ''' vertex object for graph representation '''
    idcount = itertools.count()

    def __init__(self, key, id=None, distance=None):
        ''' initialize vertex with provided key and unique ID unless specified '''
        self.id = id or next(Vertex.idcount)
        self.key = key
        self.distance = float('inf')

    def __lt__(self, other):
        ''' override < method '''
        return self.key < other.key

    def __gt__(self, other):
        ''' override > method '''
        return self.key > other.key

    def __repr__(self):
        ''' override output method - for debug '''
        return f'<{self.id}: {self.key}>'


class Graph(object):
    def __init__(self):
        self.graph = {}

    def addVertex(self, vertex):
        self.graph[vertex.id] = self.graph.get(vertex.id, vertex)

    def add_edge(self, edge):
        pass

    def show(self):
        G = nx.DiGraph() # directed graph with self loops

        for key in self.graph.keys(): # add all nodes to graph
            G.add_node(key)

        # TODO: add edges and show print weights

        pos = nx.spring_layout(G) # shell layout - could be random, spectral_layout, spring_layout or circular_layout
        nx.draw(G, pos, with_labels=True)

        plt.draw()
        plt.show()
    
    def __repr__(self):
        return '\n'.join(f"{key}: {value}" for key, value in self.graph.items())


class Heap(object):
    ''' Generic heap class for inheritance '''

    def __init__(self):
        ''' initialize heap specific data structures '''
        pass

    def push(self, value):
        ''' insert a new vertex into heap'''

    def pop(self):
        ''' delete minimum '''

    def decreaseKey(self, vertex, key):
        ''' decrease key and maintain heap '''
        pass

    def show(self):
        ''' print heap in appropriate format '''
        pass

    def __len__(self):
        ''' return number of elements in heap'''
        pass


class MinHeap(Heap):
    ''' vanilla min-heap priority queue '''

    def __init__(self):
        ''' maintain heap with underlying list - O(1) append and delete '''

        self.heap = []

    def heapify_up(self, pos=None):
        ''' upheap element at given pos in heap array '''

        child = pos or len(self.heap) - 1
        parent = (child - 1) // 2

        while child and self.heap[child] < self.heap[parent]:
            self.heap[child], self.heap[parent] = self.heap[parent], self.heap[child]
            child = parent
            parent = (child - 1) // 2

    def heapify_down(self):
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
        self.heapify_up()

    def pop(self):
        if not self.heap:
            return None

        self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]
        data = self.heap.pop()
        self.heapify_down()
        return data

    def decreaseKey(self, vertex, key):
        ''' TODO: decrease key - see HW4 '''
        pass

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

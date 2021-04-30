from graph_util.graph import Vertex
import sys
sys.path.append("..")
from heaps.base import Heap

class FibTree(Vertex):
    '''Vertex Object for Fibonacci Heap.'''

    def __init__(self, distance=float('inf'), order=0):
        super().__init__(distance)
        self.order = order

    def append(self, t):
        self.child.append(t)
        self.order += 1


class FibHeap(Heap):
    ''' Fibonacci heap priority queue '''

    def __init__(self):
        self.trees = []
        self.least = None
        self.count = 0
    
    def insert(self, value):
        new_tree = FibTree(value)
        self.trees.append(new_tree)
        if (self.least is None or value < self.least.value):
            self.least = new_tree
        self.count += 1

    def get_min(self):
        if self.least is None:
            return None
        return self.least.value

    def extract_min(self):
        smallest = self.least
        if smallest is not None:
            for child in smallest.child:
                self.trees.append(child)
            self.trees.remove(smallest)
            if self.trees == []:
                self.least = None
            else:
                self.least = self.trees[0]
                self.merge()
            self.count -= 1
            return smallest.value

    def merge(self):
        # Floor log
        aux = (frexp(self.count)[1]) * [None]

        while self.trees != []:
            tree_x = self.trees[0]
            order = tree_x.order
            self.trees.remove(tree_x)
            while aux[order] is not None:
                tree_y = aux[order]
                if tree_x.value > tree_y.value:
                    tree_x, tree_y = tree_y, tree_x
                tree_x.append(tree_y)
                aux[order] = None
                order += 1
            aux[order] = x
        
        self.least = None
        for k in aux:
            if k is not None:
                self.trees.append(k)
                if (self.least is None or k.value < self.least.value):
                    self.least = k
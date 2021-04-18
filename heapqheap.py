import heapq
from heap import Heap


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

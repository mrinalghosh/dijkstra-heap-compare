from heap import Heap

class MinHeap(Heap):
    ''' vanilla min-heap priority queue '''

    def __init__(self):
        ''' maintain heap with underlying list - O(1) append and delete '''
        self.heap = []

    def upheap(self, pos=None):
        ''' up-heap element at given pos in heap array '''
        child = pos or len(self.heap) - 1
        parent = (child - 1) // 2

        while child and self.heap[child] < self.heap[parent]:
            self.heap[child], self.heap[parent] = self.heap[parent], self.heap[child]
            child = parent
            parent = (child - 1) // 2

    def downheap(self):
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

    def insert(self, value):
        self.heap.append(value)
        self.upheap()

    def peek(self):
        if not self.heap:
            return None
        
        return self.heap[0]

    def deleteMin(self):
        ''' delete minimum element '''
        if not self.heap:
            return None

        self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]
        data = self.heap.pop()
        self.downheap()
        return data

    def decreaseKey(self, vertex, key):
        if vertex in self.heap: # TODO: remove O(n) search
            pos = self.heap.index(vertex)
            self.heap[pos].dist = key
            self.upheap(pos)

    def show(self):
        print(self.heap)

    def __len__(self):
        return len(self.heap)
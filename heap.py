import heapq

'''
Sources used:
HW4 Dijkstra
https://gist.github.com/Tetsuya3850/a271ba66f35460e1e244aacbe792576b
'''

# class Vertex(object):
#     def __init__(self, id, key):
#         self.id = id
#         self.key = key
#         self.position

# class Edge(object):
#     def __init__(self, u, v, weight):


class MinHeap(object):
    ''' standard min-heap priority queue '''

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
            return None  # Change this to false if necessary

        self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]
        data = self.heap.pop()
        self.heapify_down()
        return data

    # def decreaseKey(self, node, val):
    # TODO: decrease key - see HW4

    def show(self):
        print(self.heap)

    def __len__(self):
        return len(self.heap)


# class HeapqHeap(object):
#     ''' wrapper class for heapq from Python standard library - used for benchmarking '''

#     def __init__(self):
#         self.heap = []

#     def push(self, value):
#         heapq.heappush(self.heap, value)

#     def pop(self):
#         ''' delete min '''
#         return heapq.heappop(self.heap)

#     # def decreaseKey(self):
#     #     ''' TODO: heapq doesn't have an implementation for this '''

#     def __len__(self):
#         return len(self.heap)

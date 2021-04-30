from heaps.base import Heap


class MinHeap(Heap):
    """vanilla min-heap priority queue"""

    class Node:
        def __init__(self, data: dict, name=None):
            self.key = data["key"]
            self.name = name
            self.data = data

    heap = []

    def _upheap(self, pos=None):
        """up-heap element at given pos in heap array"""
        child = pos or len(self.heap) - 1
        parent = (child - 1) // 2

        while child and self.heap[child].key < self.heap[parent].key:
            self.heap[child], self.heap[parent] = self.heap[parent], self.heap[child]
            child = parent
            parent = (child - 1) // 2

    def _downheap(self):
        """downheap element"""
        if len(self.heap) < 2:
            return

        item = 0
        while (2 * item + 1) < len(self.heap):
            child = 2 * item + 1
            if (2 * item + 2) < len(self.heap) and self.heap[
                2 * item + 2
            ].key < self.heap[2 * item + 1].key:
                child = 2 * item + 2
            if self.heap[child].key > self.heap[item].key:
                return
            self.heap[child], self.heap[item] = self.heap[item], self.heap[child]
            item = child

    def insert(self, data: dict, name=None):
        node = self.Node(data, name)
        self.heap.append(node)
        self._upheap()
        return node

    def find_min(self):
        if not self.heap:
            return None
        # TODO: Why heap[1] instead of heap[0]?
        return self.heap[1]

    def extract_min(self) -> Node:
        """delete minimum element"""
        if not self.heap:
            return None

        self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]
        data = self.heap.pop()
        self._downheap()
        return data

    def decrease_key(self, node: Node, key):
        if key >= node.key:
            raise ValueError("Cannot decrease key with value >= current key")
        if node in self.heap:  # TODO: remove O(n) search
            pos = self.heap.index(node)
            self.heap[pos].key = key
            self._upheap(pos)

    def show(self):
        print(self.heap)

    def __len__(self):
        return len(self.heap)

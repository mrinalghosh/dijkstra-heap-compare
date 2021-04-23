''' Violation Heap Implementation.'''

from fibheap import Fheap


class Violation(Fheap):
    ''' Class defining the Violation Heap Specific Methods.'''

    def __init__(self, minimum=None):
        '''Create a Violation Heap Object.'''
        super().__init__(minimum)

    def delete_min(self):
        '''Remove minimum value from the heap.'''
        pass


    def decreaseKey(self, node, key):
        '''Decrease key from a given vertex.'''
        if k > node.key:
            raise ValueError('new key is greater than current key')
        node.key = k
        y = node.prev
        if y and node.key < y.key:
            # Make a cut here
        if node.key < self.min.key:
            self.min = node

    def show(self):
        '''Print the heap.'''
        pass
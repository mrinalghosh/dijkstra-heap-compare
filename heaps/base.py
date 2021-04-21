''' Abstract Base Class for a Heap Object.'''


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
        return len(self.heap)

class Heap(object):
    ''' Generic heap class for inheritance '''

    def __init__(self):
        ''' initialize heap specific data structures '''

    def insert(self, value):
        ''' insert a new vertex into heap'''
        raise NotImplementedError

    def peek(self):
        ''' delete minimum '''
        raise NotImplementedError

    def deleteMin(self):
        ''' see minimum '''
        raise NotImplementedError

    def decreaseKey(self, vertex, key):
        ''' decrease key and maintain heap '''
        raise NotImplementedError

    def show(self):
        ''' print heap in appropriate format '''
        raise NotImplementedError

    def __len__(self):
        ''' return number of elements in heap'''
        raise NotImplementedError

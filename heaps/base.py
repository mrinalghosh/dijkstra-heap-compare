''' Abstract Base Class for a Heap Object.'''


class Heap(object):
    '''Generic heap class for inheritance'''

    def __init__(self):
        '''initialize heap specific data structures'''
        pass

    def insert(self, key):
        '''insert a new vertex into heap'''
        pass

    def extract_min(self):
        '''delete minimum'''
        pass

    def find_min(self):
        '''return minimum'''
        pass

    def decrease_key(self, node, key):
        '''decrease key and maintain heap'''
        pass

    def show(self):
        '''print heap in appropriate format'''
        pass

    def __len__(self):
        ''' return number of elements in heap'''
        pass

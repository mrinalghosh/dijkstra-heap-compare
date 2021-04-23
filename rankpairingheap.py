import math
from heap import Heap
from collections import defaultdict

'''
Tasks:

1. Handle multiple same keys    X
2. decrease key
3. 

'''


class HalfTreeNode:
    ''' class for root-list / internal nodes '''

    def __init__(self, key):
        self.rank = 0  # rank of half-tree
        self.key = key  # navigation key
        self.next = self.prev = None  # DLL
        self.left = self.right = None  # half-tree navigation

    def __repr__(self):
        s = f'(R{self.rank}) '
        s += f' l{self.left.key}' if self.left else ' l-'
        s += f' r{self.right.key}' if self.right else ' r-'
        s += f' p{self.prev.key}' if self.prev else ' p-'
        s += f' n{self.next.key}' if self.next else ' n-'
        return s


class RankPairingHeap(Heap):
    ''' Rank-Pairing Heap as described in Tarjan's original paper: https://www.cs.princeton.edu/courses/archive/spr10/cos423/handouts/rankpairingheaps.pdf '''

    def __init__(self):
        ''' initialize empty heap - data structure is circular DLL with head at min '''
        self.min = None  # head of DLL
        self.count = 0  # number of nodes
        # self.nodes = {}  # for debug ONLY

    def insert(self, key):
        ''' add singleton to root-list - O(1) '''
        ht = HalfTreeNode(key)

        if self.count == 0:  # initialize empty
            self.min = ht.next = ht.prev = ht  # one node circular DLL

        elif self.count == 1:  # extend circular DLL
            self.min.next, self.min.prev, ht.next, ht.prev = ht, ht, self.min, self.min
            self.min = ht if self.min.key > ht.key else self.min

        else:
            if self.min.key > key:  # first position
                self.min.prev, ht.prev, ht.next = ht, self.min.prev, self.min
                ht.prev.next = self.min = ht
            else:  # second position
                self.min.next, ht.next, ht.prev = ht, self.min.next, self.min
                ht.next.prev = ht

        # self.nodes[ht.key] = ht

        self.count += 1

    # def print_nodes(self):
        # for _, node in self.nodes.items():
            # print(f'{node}')

    def show(self, verbose=False, forward=True):
        ''' debug output - verbose prints {previous-self-next} nodes '''
        if self.count == 0:
            print('Rank-pairing heap empty - cannot print')
            return

        v = self.min
        for _ in range(self.count):
            if verbose:
                print(f'{v.key}: {v.prev}, {v}, {v.next}')
            else:
                print(f'{v.key}', end=' ')

            v = v.next if forward else v.prev

        if not verbose:  # TODO: fix hacky fix for newline
            print('')

        print(f'min-key={self.min.key}, count={self.count}\n')

    def merge(self, heap):
        ''' merge root lists and update minimum '''
        if not self.min or not heap.min:  # either empty
            self.min = self.min or heap.min
            return

        ''' conatenate DLL of roots '''
        self.min.next.prev, heap.min.prev.next = heap.min.prev, self.min.next
        self.min.next, heap.min.prev = heap.min, self.min

        ''' update self.min '''
        if self.min.key > heap.min.key:
            self.min = heap.min

        self.count += heap.count

    def peek(self):
        ''' return minimum key '''
        if self.count == 0:
            print('Rank-pairing heap empty - cannot peek')
            return None
        return self.min.key

    def compress(self):
        ''' merge roots of equal rank until no two roots have equal rank - O(log n) but O(1) amortized '''

        ''' populate dict with list of roots by rank '''
        rankdict = defaultdict(lambda: [])
        node = self.min

        # iterate over rootlist
        while node != self.min:
            rankdict[node.rank].append(node)
            node = node.next

        ''' recursively merge roots - since looking at all - select a new minimum now '''
        for rank in range(int(math.log(self.count, 2)) + 1):  # this errors out - the DLL created is not correct
            mergelist = rankdict[rank]

            for _ in range(0, len(mergelist)-1, 2):  # pop pairs
                lg, sm = mergelist.pop(), mergelist.pop()

                if lg.key < sm.key: # lg is actually smaller
                    sm, lg = lg, sm

                sm.left, lg.right = lg, sm.left  # build half-tree with sm as root
                lg.prev.next, lg.next.prev = lg.next, lg.prev  # sm inplace - close lg
                lg.next = lg.prev = None
                sm.rank += 1
                
                rankdict[sm.rank].append(sm) # carry in dict

                if sm.key < self.min.key:  # update self.min
                    self.min = sm

    def delete_min(self):
        if self.count == 0:
            print('Rank-pairing heap empty - no min to delete')
            return None

        if self.count == 1:
            minkey = self.min.key
            # del self.nodes[self.min.key]
            self.min, self.count = None, 0
            return minkey

        minkey = self.min.key  # store return value

        ''' add right spine to root-list '''
        node = self.min.left  # can't update self.min.left to None object

        while node:
            self.min.next, node.next = node, self.min.next
            node.prev, node.next.prev = self.min, node
            node = node.right

        #debug
        # print(f'root-list w/ right spine:\n{self.nodes.items()}')
        # oldmin = self.min # debug

        ''' find new min in root-list and unlink old '''
        
        node, newkey = self.min.next, float('inf')
        while node != self.min:
            if node.key < newkey:
                newmin = node
                newkey = node.key
            node = node.next

        # unlink, reassign self.min and delete old
        self.min.next.prev, self.min.prev.next = self.min.prev, self.min.next

        # assign self.min to newmin
        self.min = newmin

        # # debug
        # del self.nodes[oldmin.key]
        # print(f'root-list w/ min removed:\n{self.nodes}')

        ''' compress - merge roots of equal rank until all ranks unique '''
        self.compress()

        self.count -= 1
        return minkey

        def decrease_key(self, vertex, key):



        def __len__(self):
            ''' number of elements currently in heap '''
            return self.count

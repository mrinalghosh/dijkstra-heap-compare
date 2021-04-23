import math
from heap import Heap
from collections import defaultdict

'''
Tasks:

1. Handle multiple same keys                X
2. decrease key
    - parent set during compression
3. delete min                               X
4. integrate with vertex
5. clean up
6. return key or vertex from delete_min?
'''


class HalfTreeNode:
    ''' class for root/internal nodes - can be merged into vertex '''

    def __init__(self, key):
        self.rank = 0
        self.key = key
        self.next = self.prev = None  # root-list nav
        self.parent = self.left = self.right = None  # half-tree nav

    def __repr__(self):
        s = f'(R{self.rank}) '
        s += f' P({self.parent.key})' if self.parent else ' P(~)'
        s += f' l({self.left.key})' if self.left else ' l(~)'
        s += f' r({self.right.key})' if self.right else ' r(~)'
        s += f' p({self.prev.key})' if self.prev else ' p(~)'
        s += f' n({self.next.key})' if self.next else ' n(~)'
        return s


class RankPairingHeap(Heap):
    ''' Tarjan's paper: https://www.cs.princeton.edu/courses/archive/spr10/cos423/handouts/rankpairingheaps.pdf '''

    def __init__(self):
        ''' initialize empty heap '''
        self.min = None
        self.count = 0
        self.nodes = {}  # debug

    def insert(self, key):
        ''' add singleton to root-list '''
        ht = HalfTreeNode(key)

        self.nodes[key] = ht  # debug

        if self.count == 0:
            self.min = ht.next = ht.prev = ht

        elif self.count == 1:
            self.min.next, self.min.prev, ht.next, ht.prev = ht, ht, self.min, self.min
            self.min = ht if self.min.key > ht.key else self.min

        else:
            if self.min.key > key:  # first position
                self.min.prev, ht.prev, ht.next = ht, self.min.prev, self.min
                ht.prev.next = self.min = ht
            else:  # second position
                self.min.next, ht.next, ht.prev = ht, self.min.next, self.min
                ht.next.prev = ht

        self.count += 1

    def show(self, verbose=False, forward=True):
        ''' debug print utility - verbose prints {previous-self-next} '''
        # if self.count == 0:
        #     print('Rank-pairing heap empty')
        #     return

        # v = self.min
        # for _ in range(self.count):
        #     if verbose:
        #         print(f'{v.key}: {v.prev}, {v}, {v.next}')
        #     else:
        #         print(f'{v.key}', end=' ')
        #     v = v.next if forward else v.prev

        # print(f'[min-key={self.min.key}, count={self.count}]\n')

        if self.count == 0:
            print('Rank-pairing heap empty')
            return

        for key, node in self.nodes.items():  # debug
            print(f'{key} : {node}')        # debug

        print(f'[min-key={self.min.key}, count={self.count}]\n')

    def merge(self, heap):
        ''' merge root lists and update minimum '''
        if not self.min or not heap.min:
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
        ''' merge roots of equal rank until no two roots have equal rank '''

        rankdict = defaultdict(lambda: [])  # {rank : list of roots}

        node = self.min
        while node != self.min:
            rankdict[node.rank].append(node)
            node = node.next

        ''' recursively merge in pairs - update minimum '''
        for rank in range(int(math.log(self.count, 2)) + 1):
            mergelist = rankdict[rank]

            for _ in range(0, len(mergelist)-1, 2):
                lg, sm = mergelist.pop(), mergelist.pop()

                if lg.key < sm.key:
                    sm, lg = lg, sm

                sm.left, lg.right, lg.parent = lg, sm.left, sm  # build half-tree
                lg.prev.next, lg.next.prev = lg.next, lg.prev  # relink - sm inplace
                lg.next = lg.prev = None
                sm.rank += 1

                rankdict[sm.rank].append(sm)

                if sm.key < self.min.key:
                    self.min = sm

    def delete_min(self):
        ''' pop minimum key vertex and return value '''
        del self.nodes[self.min.key]  # debug

        if self.count == 0:
            print('Rank-pairing heap empty - no min to delete')
            return None

        if self.count == 1:
            minkey = self.min.key
            self.min, self.count = None, 0
            return minkey

        minkey = self.min.key

        ''' add right spine to root-list '''
        node = self.min.left
        while node:
            node.parent = None
            self.min.next, node.next = node, self.min.next
            node.prev, node.next.prev = self.min, node
            node = node.right

        ''' find new min in root-list and unlink old '''
        node, newkey = self.min.next, float('inf')
        while node != self.min:
            if node.key < newkey:
                newmin = node
                newkey = node.key
            node = node.next

        ''' unlink and reassign self.min to node in root-list '''
        self.min.next.prev, self.min.prev.next = self.min.prev, self.min.next
        self.min = newmin

        self.compress()
        self.count -= 1

        return minkey

    def decrease_key(self, node, key):
        ''' decrement specified node.key absolutely to key '''

        # assuming vertex passed in (integrated with Vertex class) -
        # or some kind of cleverer inheritance system where we convert to inherited nodes from a vertex base class
        # and main can pass in the parent for comparison - COULD use a dictionary for {parent-Vertex: child-Custom} to get object

        ''' remove node and L subtree to new half-tree '''
        # TODO: need to know which half-tree the node is under
        node.key = key

        ''' replace node in parent with previous R child '''
        ''' update min '''
        ''' update ranks for previous tree node was in '''

    def __len__(self):
        ''' number of elements currently in heap '''
        return self.count

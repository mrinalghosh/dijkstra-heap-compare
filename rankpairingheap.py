from heap import Heap
from collections import defaultdict
import math
''' We need to uniformly decide whether to have all variables in the Vertex class or inherit basic vertices into wrapper classes '''


class HalfTreeNode:
    ''' class for root-list and internal nodes '''

    def __init__(self, key):
        self.rank = 0  # rank of half-tree
        self.key = key  # root key
        self.next = self.prev = None  # used for DLL
        self.left = self.right = None  # used for half-tree navigation
        # note: for root - only left child

    def __repr__(self):
        s = f'{self.key}'
        if self.left:
            s.join(f' L={self.left.key}')
        if self.right:
            s.join(f' R={self.right.key}')
        return s


class RankPairingHeap(Heap):

    def __init__(self):
        ''' new empty rank-pairing heap - data structure is circular DLL for O(1) insertion '''
        self.ranks = defaultdict(
            lambda: [])  # {rank: list of half-trees} - for merging
        self.min = None  # head of DLL
        self.count = 0

    def insert(self, key):
        ''' add singleton half-tree to root - O(1) '''
        ht = HalfTreeNode(key)

        if self.count == 0:  # initialize empty
            self.min = ht.next = ht.prev = ht  # one node circular DLL

        elif self.count == 1:  # extend circular DLL
            self.min.next, self.min.prev, ht.next, ht.prev = ht, ht, self.min, self.min
            self.min = ht if self.min.key > ht.key else self.min

        else:
            if self.min.key > key:  # insert into first position
                self.min.prev, ht.prev, ht.next = ht, self.min.prev, self.min
                ht.prev.next = self.min = ht  # this works - hopefully
            else:  # insert into second position
                self.min.next, ht.next, ht.prev = ht, self.min.next, self.min
                ht.next.prev = ht  # for some reason need to do this separately

        self.count += 1
        # self.ranks[0].append(ht) # O(1) but have to append dicts in merge - O(log(m) + log(n)) :(
        # handle this in compress itself

    def show(self, verbose=False, forward=True):
        ''' debug output - verbose prints previous-self-next '''
        v = self.min
        for _ in range(self.count):
            if verbose:
                print(f'{v.key}: {v.prev}, {v}, {v.next}')
            else:
                print(f'{v.key}', end=' ')

            v = v.next if forward else v.prev
        if not verbose:
            print('')
        print(f'min-key={self.min.key}, count={self.count}\n')

    def merge(self, heap):
        ''' merge root lists and update minimum - O(1)'''
        if not self.min or not heap.min:  # either heap is empty
            self.min = self.min or heap.min
            return

        # conatenate DLL of roots
        self.min.next.prev, heap.min.prev.next = heap.min.prev, self.min.next
        self.min.next, heap.min.prev = heap.min, self.min

        # update self.min
        if self.min.key > heap.min.key:
            self.min = heap.min

        self.count += heap.count

    def peek(self):
        ''' return minimum key '''
        return self.min.key  # could be none if no inserts

    def compress(self):
        ''' merge roots of equal rank until no two roots have equal rank - O(log n) but O(1) amortized '''

        ''' populate dictionary of roots by rank '''
        node = self.min
        for _ in range(self.count):
            self.ranks[node.rank].append(node)
            node = node.next

        ''' recursively merge roots '''
        for rank in range(int(math.log(self.count, 2)) + 1):  # O(log n)
            mergelist = self.ranks[rank]

            for _ in range(0, len(mergelist)-1, 2):  # pop pairs of half trees
                A, B = mergelist.pop(), mergelist.pop()
                if A.key > B.key:
                    B.left, A.right = A, B.left  # build half tree
                    # keep B in place and close hole where A was
                    A.prev.next, A.next.prev = A.next, A.prev
                    B.rank += 1
                    # update dictionary for recursive compression
                    self.ranks[B.rank].append(B)
                else:
                    A.left, B.right = B, A.left
                    # relink DLL - keep A in place and close hole where B was
                    B.prev.next, B.next.prev = B.next, B.prev
                    A.rank += 1
                    self.ranks[A.rank].append(A)

                # print(smaller)
                # print(smaller.left)
                # print(smaller.right)
                # print(larger)
                # print(larger.left)
                # print(larger.right)
                # print('')

            print(self.ranks)

    def delete_min(self):
        ''' TODO: extractMin/pop better '''

        ''' delete root '''

        ''' cut edges along right spine and add to root list '''

        ''' compress - merge roots of equal rank until all ranks unique '''

        # def decreaseKey(self, vertex, key):

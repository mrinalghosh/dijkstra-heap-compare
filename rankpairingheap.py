import math
from heap import Heap
from collections import defaultdict


class HalfTreeNode:
    ''' class for root-list / internal nodes '''

    def __init__(self, key):
        self.rank = 0  # rank of half-tree
        self.key = key  # navigation key
        self.next = self.prev = None  # DLL
        self.left = self.right = None  # half-tree navigation

    def __repr__(self):
        s = f'(R{self.rank}) '
        s += f'l{self.left.key} ' if self.left else 'l- '
        s += f'r{self.right.key} ' if self.right else 'r- '
        s += f'p{self.prev.key} ' if self.prev else 'p- '
        s += f'n{self.next.key} ' if self.next else 'n- '
        return s


class RankPairingHeap(Heap):
    ''' Rank-Pairing Heap as described in Tarjan's original paper: https://www.cs.princeton.edu/courses/archive/spr10/cos423/handouts/rankpairingheaps.pdf '''

    def __init__(self):
        ''' initialize empty heap - data structure is circular DLL with head at min '''
        self.min = None  # head of DLL
        self.count = 0  # number of nodes
        self.nodes = {}  # for debug ONLY

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

        self.nodes[ht.key] = ht

        self.count += 1

    def print_nodes(self):
        for _, node in self.nodes.items():
            print(f'{node}')

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

        ''' populate dictionary with list of roots by rank '''
        rankdict = defaultdict(lambda: [])
        node = self.min

        # iterate over rootlist not number of nodes left
        while node != self.min:
            rankdict[node.rank].append(node)
            node = node.next

        # for _ in range(self.count):
        #     rankdict[node.rank].append(node)
        #     node = node.next

        ''' recursively merge roots - since looking at all - select a new minimum now '''
        for rank in range(int(math.log(self.count, 2)) + 1):  # this errors out - the DLL created is not correct
            mergelist = rankdict[rank]

            for _ in range(0, len(mergelist)-1, 2):  # pop pairs - leaves 0/1
                A, B = mergelist.pop(), mergelist.pop()

                if A.key > B.key:
                    B.left, A.right = A, B.left  # build half-tree
                    A.prev.next, A.next.prev = A.next, A.prev  # B inplace and close hole for A
                    A.next = A.prev = None
                    B.rank += 1
                    # update dict for recursive compression
                    rankdict[B.rank].append(B)
                    if B.key < self.min.key:  # update true self.min
                        self.min = B
                else:
                    A.left, B.right = B, A.left
                    B.prev.next, B.next.prev = B.next, B.prev  # A inplace and close hole for B
                    B.next = B.prev = None
                    A.rank += 1
                    rankdict[A.rank].append(A)
                    if A.key < self.min.key:
                        self.min = A

            # print(rankdict)

    def delete_min(self):
        if self.count == 0:
            print('Rank-pairing heap empty - no min to delete')
            return None

        min_key = self.min.key  # store return value

        ''' add right spine to root-list '''
        node = self.min.left # can't update self.min.left to None object

        while node:
            self.min.next, node.next = node, self.min.next
            node.prev, node.next.prev = self.min, node
            node = node.right

        print(f'root-list w/ right spine:\n{self.nodes.items()}\n') # WORKS

        ''' find new min in root-list and unlink old '''

        
        # may need to still errorcheck 0/1...
        self.min.next.prev , self.min.prev.next = self.min.prev, self.min.next
        node, self.min = self.min, self.min.next

        del self.nodes[node.key] # debug

        ''' find new min '''
        while node != self.min:
            if node.key < self.min.key:
                new_min = node
            node = node.next

        self.min = new_min

        print(f'root-list w/ min removed:\n{self.nodes}\n')


        ''' compress - merge roots of equal rank until all ranks unique '''
        self.compress()

        # print(f'root-list after compression:\n{self.nodes}\n')

        return min_key

        ''' # store key to return, node to delete
        min_key, min_node = self.min.key, self.min '''

        ''' delete root - update dll to skip self.min '''

        # self.count -= 1  # decrement count

        # if self.count == 0:  # heap will be emptied
        #     self.min = None

        # elif self.count == 1:  # heap will only have one node
        #     self.min = self.min.left if self.min.next == self.min else self.min.next
        #     self.min.next = self.min.prev = self.min

        # else:  # multiple nodes remain in one or more half-trees

        #     # make gap in DLL - if only one root left this is bad
        #     self.min.next.prev, self.min.prev.next = self.min.prev, self.min.next
        #     # this has to be wrong when there's only one tree left - otherwise check if only one tree
        #     self.min = self.min.next  # idk just assign it to next node still in root-list

        #     ''' cut edges along right spine and add to root list '''
        #     ht = self.min.left
        #     while ht:
        #         # insert into second position in root-list
        #         ht.next, ht.prev = self.min.next, self.min
        #         self.min.next, ht.next.prev = ht, ht
        #         ht = ht.right  # move down spine

        #     print(f'\nBefore compress - nodelist:\n{self.nodes}')

        #     ''' compress - merge roots of equal rank until all ranks unique '''
        #     self.compress()

        # self.remove(min_node)  # wrong min kept sometimes after compression
        # return min_key

        # def decreaseKey(self, vertex, key):

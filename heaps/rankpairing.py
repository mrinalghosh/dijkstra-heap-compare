from math import log
from heaps.base import Heap
from graph_util.graph import Vertex
from collections import defaultdict

'''
Tasks:

1. Handle multiple same keys                X
2. decrease key
    - parent set during compression         X
3. delete min                               X
4. integrate with vertex
5. clean up
6. return key or vertex from extract_min?
'''


class HalfTree(Vertex):
    ''' class for root/internal nodes - can be merged into vertex '''

    def __init__(self, key):
        super().__init__(key)
        self.rank = 0
        self.key = key
        self.next = self.prev = self.parent = self.left = self.right = None

    def __repr__(self):
        s = f'key({self.key}) rank({self.rank}) '
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
        # self.nodes = {}  # debug

    def insert(self, key):
        ''' add singleton to root-list '''
        ht = HalfTree(key)

        # self.nodes[key] = ht  # debug

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

    # def show(self, verbose=False, forward=True):
    #     ''' debug print utility - verbose prints {previous-self-next} '''
    #     if self.count == 0:
    #         raise ValueError('RankPairingHeap empty')

    #     v = self.min
    #     for _ in range(self.count):
    #         if verbose:
    #             print(f'{v.key}: {v.prev}, {v}, {v.next}')
    #         else:
    #             print(f'{v.key}', end=' ')
    #         v = v.next if forward else v.prev

    #     print(f'[min-key={self.min.key}, count={self.count}]\n')

    def show(self):
        def show_halftree(root):
            if root is None:
                return

            queue = []
            queue.append(root)
            while(len(queue) > 0):
                print(queue[0])
                node = queue.pop(0)

                if node.left is not None:
                    queue.append(node.left)

                if node.right is not None:
                    queue.append(node.right)

            print('')

        show_halftree(self.min)
        node = self.min.next
        while node != self.min:
            show_halftree(node)
            node = node.next

        print(f'[min-key={self.min.key}, count={self.count}]\n')

        # if self.count == 0:
        #     print('Rank-pairing heap empty')
        #     return

        # for key, node in self.nodes.items():  # debug
        # print(f'{key} : {node}')        # debug

        # print(f'[min-key={self.min.key}, count={self.count}]\n')

    def merge(self, heap):
        ''' merge root lists and update minimum '''
        if not self.min or not heap.min:
            self.min = self.min or heap.min
            self.count = max(self.count, heap.count)
            return

        ''' conatenate DLL of roots '''
        self.min.next.prev, heap.min.prev.next = heap.min.prev, self.min.next
        self.min.next, heap.min.prev = heap.min, self.min

        ''' update self.min '''
        if self.min.key > heap.min.key:
            self.min = heap.min

        self.count += heap.count

    def find_min(self):
        ''' return minimum key '''
        if self.count == 0:
            raise ValueError('Cannot peek: RankPairingHeap is empty')
        return self.min.key

    def _compress(self):
        ''' merge roots of equal rank until no two roots have equal rank '''

        rankdict = defaultdict(lambda: [])

        node = self.min.next
        while node != self.min:
            rankdict[node.rank].append(node)
            node = node.next

        ''' recursively merge in pairs - update minimum '''
        for rank in range(int(log(self.count, 2)) + 1):
            mergelist = rankdict[rank]

            for _ in range(0, len(mergelist)-1, 2):
                lg, sm = mergelist.pop(), mergelist.pop()

                if lg.key < sm.key:
                    sm, lg = lg, sm

                sm.left, lg.right, lg.parent = lg, sm.left, sm
                lg.prev.next, lg.next.prev = lg.next, lg.prev
                lg.next = lg.prev = None
                sm.rank += 1

                rankdict[sm.rank].append(sm)

                if sm.key < self.min.key:
                    self.min = sm

    def extract_min(self):
        ''' pop minimum key vertex and return value '''
        # self.show()

        if self.count == 0:
            raise ValueError('Cannot extract_min: RankPairingHeap is empty')

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
            newnode = node.right
            node.right = None
            node = newnode

        ''' find new min in root-list and unlink old '''
        node, newkey = self.min.next, float('inf')
        if node == self.min:
            node = newmin = self.min.left

        while node != self.min:
            if node.key <= newkey:
                newmin = node
                newkey = node.key
            node = node.next

        ''' unlink and reassign self.min to node in root-list '''
        self.min.next.prev, self.min.prev.next = self.min.prev, self.min.next
        self.min = newmin

        self._compress()
        self.count -= 1

        return minkey

    def decrease_key(self, node, key):
        ''' decrement specified node.key absolutely to key '''

        # TODO: need to integrate with Vertex to have object passed in correctly

        if key >= node.key:
            raise ValueError('Cannot decrease_key with value >= current value')

        node.key = key

        ''' remove node and L subtree to new half-tree 
        replace node in parent with node's previous R child '''

        node.parent.left = node.right
        node.right = None

        ''' relink and update min '''
        if self.min.key > key:  # first
            self.min.prev, node.prev, node.next = node, self.min.prev, self.min
            node.prev.next = self.min = node
        else:  # second
            self.min.next, node.next, node.prev = node, self.min.next, self.min
            node.next.prev = node

        ''' update ranks for previous tree node was in '''
        p = node.parent
        while p:
            if not p.left and not p.right:  # leaf
                p.rank = 0
            elif not p.parent:  # root
                if p.left:
                    p.rank = p.left.rank + 1
                break
            else:
                if abs(p.left.rank - p.right.rank) > 1:
                    p.rank = max(p.left.rank, p.right.rank)
                else:
                    p.rank = max(p.left.rank, p.right.rank) + 1

            p = p.parent

    def __len__(self):
        ''' number of elements currently in heap '''
        return self.count

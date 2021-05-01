import itertools
from math import log
# from heaps.base import Heap
from collections import defaultdict


'''
Sources: 
https://www.cs.princeton.edu/courses/archive/spr10/cos423/handouts/rankpairingheaps.pdf
'''


class RankPairingHeap(object):
    ''' Rank-Pairing Heap Implementation based on Tarjan's paper '''

    class HalfTree(object):
        ''' HalfTree class for internal nodes '''

        # uidc = itertools.count()  # unique ID counter for debug

        def __init__(self, data: dict, name=None):
            self.name = name
            self.key = data['key']
            self.rank = 0
            self.next = self.prev = self.parent = self.left = self.right = None
            self.data = data

        def __repr__(self):
            ''' debug representation '''
            s = f'{self.name:^7}|{self.key:^7}|{self.rank:^7}'
            s += f'||{self.parent.name:^9}' if self.parent else f'||{"-":^9}'
            s += f'|{self.left.name:^9}' if self.left else f'|{"-":^9}'
            s += f'|{self.right.name:^9}' if self.right else f'|{"-":^9}'
            s += f'||{self.prev.name:^9}' if self.prev else f'||{"-":^9}'
            s += f'|{self.next.name:^9}' if self.next else f'|{"-":^9}'
            return s

    def __init__(self):
        ''' initialize empty heap '''
        self.min = None
        self.count = 0

    def insert(self, data: dict, name=None):
        ''' add singleton to root-list '''
        node = RankPairingHeap.HalfTree(data, name)

        if self.count == 0:
            self.min = node.next = node.prev = node

        elif self.count == 1:
            self.min.next, self.min.prev, node.next, node.prev = node, node, self.min, self.min
            self.min = node if self.min.key > node.key else self.min

        else:
            # always insert in 'first' position
            node.prev, node.next = self.min.prev, self.min
            node.prev.next, node.next.prev = node, node

            # update min-root
            if self.min.key > node.key:
                self.min = node

        self.count += 1
        return node

    def debug_check_loop(self, node=None):
        node, seen = self.min.next, []
        while node != self.min:
            if node in seen:  # loop exists without touching self.min again
                self.show(verbose=True, node=node)
            seen.append(node)
            node = node.next

    def _show_bfs(self, root):
        ''' traverse half-tree using breadth first search '''
        if root is None:
            return

        queue = [root]
        while(len(queue) > 0):
            node = queue.pop(0)
            if node == self.min:
                print(' * '*25)

            print(node)
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)

        print('-'*80)

    def show(self, verbose=False, node=None):
        ''' debug print utility - verbose prints all half trees '''
        if self.count == 0:
            raise ValueError('RankPairingHeap empty')

        if verbose:
            if node:
                print(f'\nnode decreased - {node}')
            print(f'minimum root - {self.min}\n')

            print(
                f'{"id":^7}|{"key":^7}|{"rank":^7}||{"parent":^9}|{"left":^9}|{"right":^9}||{"prev":^9}|{"next":^9}\n' + '-'*80)
            self._show_bfs(self.min)
            node, seen = self.min.next, []
            while node != self.min:
                self._show_bfs(node)
                if node.name in seen:
                    raise RuntimeError(
                        f'\nLast fn call caused min to be skipped:\n{self.min}\n')
                seen.append(node.name)
                node = node.next
        else:
            node = self.min.next
            while node != self.min:
                print(f'{node.key}', end=' ')
                node = node.next

        print(f'[min-key={self.min.key}, count={self.count}]\n')

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
            raise ValueError('Cannot find_min: RankPairingHeap is empty')
        return self.min

    def _compress(self):
        ''' merge roots of equal rank until no two roots have equal rank '''

        rankdict = defaultdict(lambda: [])

        node = self.min.next
        if node == self.min:
            return

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
                if lg.right:
                    lg.right.parent = lg
                lg.prev.next = lg.next
                lg.next.prev = lg.prev
                lg.next = lg.prev = None
                sm.rank += 1

                rankdict[sm.rank].append(sm)

                if sm.key < self.min.key:
                    self.min = sm

    def extract_min(self):
        ''' pop minimum key vertex and return key '''

        if self.count == 0:
            raise ValueError('Cannot extract_min: RankPairingHeap is empty')

        min_node = self.min  # store old min

        if self.count == 1:  # now will have zero elements in heap
            self.min, self.count = None, 0
            return min_node

        ''' add right spine to root-list '''
        node = self.min.left
        while node:
            node.parent, right = None, node.right # set parent as none and store R-child
            node.prev, node.next = self.min, self.min.next
            node.prev.next = node.next.prev = node  # node.prev.next = self.min.next
            node.right, node = None, right  # correct right and set next node

        self.show(verbose=True)

        ''' unlink self.min and assign to next element '''
        self.min.next.prev, self.min.prev.next = self.min.prev, self.min.next
        self.min = self.min.next

        ''' compress and decrement count '''
        self._compress()
        self.count -= 1

        return min_node

    def decrease_key(self, node, key):
        ''' decrement specified node.key absolutely to key '''
        if key >= node.key:
            raise ValueError('Cannot decrease_distance with key >= current')

        if node == self.min:
            self.min.key = key
            return

        node.key = key

        ''' remove node and L-child to new half-tree & replace in parent with node R-child '''
        if node.parent:
            if node.parent.left == node:
                node.parent.left = node.right
                if node.right:
                    node.right.parent = node.parent
                node.right = None  # remove right child

            elif node.parent.right == node:
                node.parent.right = node.right
                if node.right:
                    node.right.parent = node.parent
                node.right = None
        else:  # in root-list - update min without relinking
            if self.min.key > node.key:
                self.min = node
            return

        ''' relink second position in root list '''
        node.next, node.prev = self.min.next, self.min
        # if not node.next or not node.prev:
        #     print(self.min)
        #     self.show(verbose=True)
        node.next.prev = node.prev.next = node

        # self.debug_check_loop(node)

        ''' update min '''
        if self.min.key > node.key:
            self.min = node

        ''' update ranks for previous tree '''
        p = node.parent
        node.parent = None

        while p:
            if not p.left and not p.right:  # leaf - no children
                p.rank = 0

            elif not p.parent:  # root
                if p.left:
                    p.rank = p.left.rank + 1

            elif not p.left:
                p.rank = p.right.rank
            elif not p.right:  # has only one child
                p.rank = p.left.rank

            else:  # must have both children
                if abs(p.left.rank - p.right.rank) > 1:
                    p.rank = max(p.left.rank, p.right.rank)
                else:
                    p.rank = max(p.left.rank, p.right.rank) + 1

            p = p.parent

    def __len__(self):
        ''' number of elements currently in heap '''
        return self.count

from math import log
from heaps.base import Heap
from graph_util.graph import Vertex
from collections import defaultdict


class HalfTree(Vertex):
    ''' HalfTree class for internal nodes '''

    def __init__(self, distance):
        super().__init__(distance)
        self.rank = 0
        self.next = self.prev = self.parent = self.left = self.right = None

    def __repr__(self):
        ''' debug representation '''
        s = f'{self.id:^9}|{self.distance:^9}|{self.rank:^9}'        
        s += f'|{self.parent.id:^9}' if self.parent else f'|{"-":^9}'
        s += f'|{self.left.id:^9}' if self.left else f'|{"-":^9}'
        s += f'|{self.right.id:^9}' if self.right else f'|{"-":^9}'
        s += f'|{self.prev.id:^9}' if self.prev else f'|{"-":^9}'
        s += f'|{self.next.id:^9}' if self.next else f'|{"-":^9}'
        return s


class RankPairingHeap(Heap):
    ''' Implementation based on Tarjan's paper: https://www.cs.princeton.edu/courses/archive/spr10/cos423/handouts/rankpairingheaps.pdf '''

    def __init__(self):
        ''' initialize empty heap '''
        self.min = None
        self.count = 0

    def insert(self, key):
        ''' add singleton to root-list '''
        node = HalfTree(key)

        if self.count == 0:
            self.min = node.next = node.prev = node

        elif self.count == 1:
            self.min.next, self.min.prev, node.next, node.prev = node, node, self.min, self.min
            self.min = node if self.min.distance > node.distance else self.min

        else:
            if self.min.distance > key:  # min-root
                self.min.prev, node.prev, node.next = node, self.min.prev, self.min
                node.prev.next = self.min = node
            else:  # min-root.next
                self.min.next, node.next, node.prev = node, self.min.next, self.min
                node.next.prev = node

        self.count += 1
        return node

    def _show_bfs(self, root):
        ''' traverse half-tree using breadth first search '''
        if root is None:
            return

        queue = [root]
        while(len(queue) > 0):
            print(queue[0])
            node = queue.pop(0)
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)

        print('-'*80)

    def show(self, verbose=False):
        ''' debug print utility - verbose prints all half trees '''
        if self.count == 0:
            raise ValueError('RankPairingHeap empty')

        if verbose:
            print(f'{"id":^9}|{"key":^9}|{"rank":^9}|{"parent":^9}|{"left":^9}|{"right":^9}|{"prev":^9}|{"next":^9}')
            self._show_bfs(self.min)
            node = self.min.next
            while node != self.min:
                self._show_bfs(node)
                node = node.next
        else:
            node = self.min.next
            while node != self.min:
                print(f'{node.distance}', end=' ')
                node = node.next

        print(f'[min-distance={self.min.distance}, count={self.count}]\n')

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
        if self.min.distance > heap.min.distance:
            self.min = heap.min

        self.count += heap.count

    def find_min(self):
        ''' return minimum distance '''
        if self.count == 0:
            raise ValueError('Cannot find_min: RankPairingHeap is empty')
        return self.min

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

                if lg.distance < sm.distance:
                    sm, lg = lg, sm

                sm.left, lg.right, lg.parent = lg, sm.left, sm
                lg.prev.next, lg.next.prev = lg.next, lg.prev
                lg.next = lg.prev = None
                sm.rank += 1

                rankdict[sm.rank].append(sm)

                if sm.distance < self.min.distance:
                    self.min = sm

    def extract_min(self):
        ''' pop minimum distance vertex and return key '''
        if self.count == 0:
            raise ValueError('Cannot extract_min: RankPairingHeap is empty')

        oldmin = self.min

        if self.count == 1:
            self.min, self.count = None, 0
            return oldmin

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
        node, newdistance = self.min.next, float('inf')
        if node == self.min:  # only min in rootlist
            node = newmin = self.min.left

        while node != self.min:
            if node.distance < newdistance:
                newmin = node
                newdistance = node.distance
            node = node.next

        ''' unlink and reassign self.min to node in root-list '''
        self.min.next.prev, self.min.prev.next = self.min.prev, self.min.next
        self.min = newmin

        ''' compress and decrement count '''
        self._compress()
        self.count -= 1

        return oldmin

    def decrease_key(self, node, key):
        ''' decrement specified node.distance absolutely to key '''
        if key >= node.distance:
            raise ValueError('Cannot decrease_distance with key >= current')

        node.distance = key

        ''' remove node and Lchild to new half-tree & replace in parent with node Rchild '''
        if node.parent:
            node.parent.left = node.right
            node.right = None
        else:  # in root-list - just update min without relinking
            if self.min.distance > node.distance:
                self.min = node
                return

        ''' relink and update min '''
        if self.min.distance > key:  # min-root
            node.prev, node.next = self.min.prev, self.min
            self.min.prev = self.min = node
            node.prev.next = node.next.prev = node
        else:  # min-root.next
            node.prev.next = node.next
            node.next, node.prev = self.min.next, self.min
            self.min.next = node.next.prev = node

        ''' update ranks for previous tree '''
        p = node.parent
        node.parent = None
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

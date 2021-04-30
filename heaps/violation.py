''' Violation Heap Implementation.

References:
https://violationheap.weebly.com/
https://arxiv.org/pdf/0812.2851.pdf
https://github.com/haoliangx/Violation-Heap
'''

from math import ceil


class ViolationHeap(object):
    ''' Class defining the Violation Heap Specific Methods.'''

    class Node:
        '''Class defining the Violation Heap node.'''
        def __init__(self, data: dict, name=None, rank=0):
            self.key = data["key"]
            self.name = name
            self.data = data
            self.rank = rank
            self.next = None
            self.prev = None
            self.child = None

    def __init__(self):
        '''Create a Violation Heap Object.'''
        self.root = None
        self.count = 0
    
    def __len__(self):
        return self.count

    def _active(self, node):
        '''Check if given node is active or not.''' 
        parent = None
        max = 2
        p = node
        if node.prev == None:
            return True

        # Moving backwards
        while p.prev.child != p:
            p = p.prev
            max -= 1
        parent = q.prev

        return (True if max > 0 else False, parent)

    def _join(self, nodel_a, nodel_b):
        '''Join given node into existing heap.'''
        if nodel_b == None:
            return (nodel_a, nodel_b)

        # If our current heap is empty, just add the node to it
        if nodel_a == None:
            nodel_a = nodel_b
            return (nodel_a, nodel_b)
        
        # Swap, to get a new min
        if nodel_a.key > nodel_b.key:
            tmp = nodel_a
            nodel_a = nodel_b
            nodel_b = tmp
        
        # Connect node to the next to root and move curr to the end.
        next = nodel_a.next
        nodel_a.next = nodel_b
        curr = nodel_b
        
        while curr.next:
            curr = curr.next
        if next:
            curr.next = next
        
        return (nodel_a, nodel_b)

    def _update_rank(self, node):
        ''' Update given node's rank.'''
        # Get the active children, which are the two last children
        if node.child:
            active1 = node.child
            active2 = node.child.next

        rank1 = rank2 = -1
        if active1:
            rank1 = active1.rank
        if active2:
            rank2 = active2.rank
        node.rank = ceil((rank1 + rank2)/2) + 1

        return node

    def _consolidate(self):
        '''Consolidate the heap.'''
        max_rank = 0
        
        # We need another list to do a 3 way join
        rank_comb = [None] * (self.count * 100)
        
        # Move to a tmp list, do a deep copy
        tmp = []
        curr = self.root
        if curr == None:
            return
        while curr:
            tmp.append(curr)
            curr = curr.next

        # Perform 3-way join
        for i in tmp:
            i.prev = None
            i.next = None

            i1 = rank_comb[2 * i.rank]
            i2 = rank_comb[(2 * i.rank) + 1]
            while i1 and i2:
                # Swap to get min
                if i.key > i1.key:
                    tmp_i = i
                    i = i1
                    i1 = tmp_i  
                if i.key > i2.key:
                    tmp_i = i
                    i = i2
                    i2 = tmp_i

                i, i1 = self._join(i, i1)
                i, i2 = self._join(i, i2)
                rank_comb[2 * i.rank] = None
                rank_comb[(2 * i.rank) + 1] = None
                i.rank += 1
                i1 = rank_comb[2 * i.rank]
                i2 = rank_comb[(2 * i.rank) + 1]
            if i1 == None:
                rank_comb[2 * i.rank] = i
            elif i2 == None:
                rank_comb[(2 * i.rank) + 1] = i

            if max_rank < i.rank:
                max_rank = i.rank

        # Consolidate the root list
        self.root = None
        for j in range(0, 2 * (max_rank + 1), 2):
            tmp1 = rank_comb[j]
            tmp2 = rank_comb[j + 1]
            self.root, tmp1 = self._join(self.root, tmp1)
            self.root, tmp2 = self._join(self.root, tmp2)

    def insert(self, data: dict, name=None):
        '''Add a new node into the heap.'''
        new_node = self.Node(data, name)
        self.root, new_node = self._join(self.root, new_node)
        self.count += 1
        
        return new_node

    def extract_min(self):
        '''Remove minimum value from the heap.'''
        min_node = self.root
        children = min_node.child

        if min_node:
            self.root = min_node.next
            self.count -= 1

            # Join the children to the root list.
            self.root, children = self._join(self.root, children)

            # Now, we have to fix the heap...
            self._consolidate()

        else:
            raise ValueError("Cannot extract minimum: ViolationHeap is empty.")

        return min_node

    def decrease_key(self, node, key):
        '''Decrease key from a given vertex.'''
        if key >= node.key:
            raise ValueError("Key provided >= to node.key!")
        else:
            node.key = key

        if node.prev == None:
            if node.key < self.root.key:
                curr = self.root
                while curr.next != node:
                    curr= curr.next
                curr.next = None
                h = self.root
                self.root = node
                t = node
                while t.next != None:
                    t = t.next
                t.next = h
            return

        node_is_active, parent = self._active(node)
        if node_is_active and parent.key <= node.key:
            return

        n_rank = self._update_rank(node)
        curr = node
        curr_is_active, curr_parent = self._active(curr)
        while curr_is_active and n_rank > node.rank:
            n_rank = self._update_rank(curr_parent)
            curr = curr_parent
            if curr.prev == None:
                break

        if node.prev.child == node:
            node.prev.child = node.next
            if node.next:
                node.next.prev = node.prev
        else:
            node.prev.next = node.next
            if (node.next):
                node.next.prev = node.prev
        node.next = None
        node.prev = None

        self._join(self.root, node)

    def find_min(self):
        return self.root

    def show(self):
        '''Print the heap.'''
        curr = self.root
        while curr:
            print("D:", curr.key)
            curr = curr.next

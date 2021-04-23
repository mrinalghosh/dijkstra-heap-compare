from graph_util.graph import Vertex
from heaps.base import Heap


class FibTree(Vertex):
    """Vertex Object for Fibonacci Heap."""

    def __init__(self, distance=float("inf"), order=0):
        super().__init__(distance)
        self.order = order

    def append(self, t):
        self.child.append(t)
        self.order += 1


class FibHeap(Heap):
    """ Fibonacci heap priority queue """

    class Node:
        def __init__(self, key, value):
            self.key = key
            self.value = value
            self.parent = self.child = self.left = self.right = None
            self.degree = 0
            self.mark = False

    # Pointer to element of doubly linked root list
    root_list = None
    # Pointer to node with minimum element on heap
    min_node = Node(None, None)
    # Num nodes in heap
    total_nodes = 0

    def find_min(self) -> Node:
        return self.min_node

    def insert(self, key, value=None):
        node = self.Node(key, value)
        node.left = node.right = node
        self.merge_with_root_list(node)
        # Update min if needed
        if self.min_node is not None or node.key < self.min_node.key:
            self.min_node = node
        self.total_nodes += 1
        return node

    # Iterate through a doubly linked list
    def iterate(self, head = None):
        if head is None:
            head = self.root_list
        current = head
        while True:
            yield current
            if current is None:
                break
            current = current.right
            if current == head:
                break

    def extract_min(self) -> Node:
        smallest = self.min_node
        if smallest is None:
            raise ValueError("Cannot extract minimum: FibHeap is empty.")
        if smallest is not None:
            children = [x for x in self.iterate(smallest.child)]
            for i in range(0, len(children)):
                self.merge_with_root_list(children[i])
                children[i].parent = None
        self.remove_from_root_list(smallest)
        self.total_nodes -= 1
        # Update min
        if smallest == smallest.right:
            self.min_node = self.root_list = None
        else:
            # self.min_node = smallest.right
            self.min_node = self.find_min_node()
            self.consolidate()
        return smallest

    # Decrease key of node in the heap in O(1)
    def decrease_key(self, node: Node, k):
        if k >= node.key:
            raise ValueError("Cannot decrease key with value >= current key")
        node.key = k
        p = node.parent
        if p is not None and node.key < p.key:
            self.cut(node, p)
            self.cascading_cut(p)
        if node.key < self.min_node.key:
            self.min_node = node

    # Merge two trees in O(1) by concatenating root list
    def merge(self, fh: "FibHeap") -> "FibHeap":
        if fh.total_nodes == 0:
            return
        H = FibHeap()
        H.root_list, H.min_node = self.root_list, self.min_node
        last = fh.root_list.left
        fh.root_list.left = H.root_list.left
        H.root_list.left.right = fh.root_list
        H.root_list.left = last
        H.root_list.left.right = H.root_list
        # update min node if needed
        if fh.min_node.key < H.min_node.key:
            H.min_node = fh.min_node
        # update total nodes
        H.total_nodes = self.total_nodes + fh.total_nodes
        return H

    # If child node becomes smaller than parent node,
    # cut child node off and move to  root list
    def cut(self, node: Node, parent: Node):
        self.remove_from_child_list(parent, node)
        parent.degree -= 1
        self.merge_with_root_list(node)
        node.parent = None
        node.mark = False

    def cascading_cut(self, node: Node):
        p = node.parent
        if p is not None:
            if p.mark is False:
                p.mark = True
            else:
                self.cut(node, p)
                self.cascading_cut(p)

    def merge_with_root_list(self, node: Node):
        if self.root_list is None:
            self.root_list = node
        else:
            node.right = self.root_list.right
            node.left = self.root_list
            self.root_list.right.left = node
            self.root_list.right = node

    def remove_from_root_list(self, node: Node):
        if self.root_list is None:
            raise ValueError("Cannot remove from empty heap")
        if self.root_list == node:
            if self.root_list == self.root_list.right:
                self.root_list = None
                return
            else:
                self.root_list = node.right
        node.left.right = node.right
        node.right.left = node.left
        return

    def merge_with_child_list(self, parent: Node, node: Node):
        if parent.child is None:
            parent.child = node
        else:
            node.right = parent.child.right
            node.left = parent.child
            parent.child.right.left = node
            parent.child.right = node

    def remove_from_child_list(self, parent: Node, node: Node):
        if parent.child == parent.child.right:
            parent.child = None
        elif parent.child == node:
            parent.child = node.right
            node.right.parent = parent
        node.left.right = node.right
        node.right.left = node.left

    # Consolidate root nodes of equal degree
    def consolidate(self):
        if self.root_list is None:
            return
        ranks_mapping = [None] * self.total_nodes
        nodes = [x for x in self.iterate(self.root_list)]
        for node in nodes:
            degree = node.degree
            while ranks_mapping[degree] != None:
                other = ranks_mapping[degree]
                if node.key > other.key:
                    node, other = other, node
                self.merge_nodes(node, other)
                ranks_mapping[degree] = None
                degree += 1
            ranks_mapping[degree] = node

    def merge_nodes(self, node: Node, other: Node):
        self.remove_from_root_list(other)
        other.left = other.right = other
        # Adding other node to child list of the frst one.
        self.merge_with_child_list(node, other)
        node.degree += 1
        other.parent = node
        other.mark = False

    # Iterate through list to find minimum node
    def find_min_node(self):
        if self.root_list is None:
            return None
        else:
            smallest = self.root_list
            for x in self.iterate(self.root_list):
                if x.key < smallest.key:
                    smallest = x
            return smallest

    def print(self, head = None):
        if self.root_list is not None:
            count = 0
            for heap in self.iterate():
                print(f"tree{count}\n[")
                self.print_tree(heap)
                print("]\n")
                count += 1

    def print_tree(self, node: Node):
        if node is None:
            return
        print(f"{node.key}: {node.value} ")
        if node.child is not None:
            print()
            for child in self.iterate(node.child):
                self.print_tree(child)
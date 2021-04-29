import heapq
import itertools
import math
'''
Sources used:
https://gist.github.com/Tetsuya3850/a271ba66f35460e1e244aacbe792576b - vanilla min-heap
https://github.com/reinvald/Dijkstra-Visualizer - networkx
'''


class Vertex(object):
    ''' vertex object for graph representation '''
    idcount = itertools.count()

    def __init__(self, key, id=None, distance=None):
        ''' initialize vertex with provided key and unique ID unless specified '''
        self.id = id or next(Vertex.idcount)
        self.key = key
        self.distance = float('inf')
        #!Needed for quake heaps
        self.highestclone = None
        self.highclonelevel = 0
        self.lowestclone = None

    def __lt__(self, other):
        ''' override < method '''
        return self.key < other.key

    def __gt__(self, other):
        ''' override > method '''
        return self.key > other.key

    def __repr__(self):
        ''' override output method - for debug '''
        return f'{self.key}'


class Heap(object):
    ''' Generic heap class for inheritance '''

    def __init__(self):
        ''' initialize heap specific data structures '''
        pass

    def insert(self, value):
        ''' insert a new vertex into heap'''

    def extract_min(self):
        ''' delete minimum '''

    def decrease_key(self, vertex, key):
        ''' decrease key and maintain heap '''
        pass

    def show(self):
        ''' print heap in appropriate format '''
        pass

    def __len__(self):
        ''' return number of elements in heap'''
        pass


class TournamentTree:
    '''
    Clone class maintains a pointer to vertex objects for O(1) updates
    '''
    class Clone:
        '''
        To maintain consistency, bottom level is a clone node with isvertex set to true
        All other clones default to false
        '''

        def __init__(self, vertex: Vertex, isvertex=False):
            self.vertex = vertex
            self.left = self.right = self.parent = None
            self.isvertex = isvertex
            vertex.highestclone = self
            if(isvertex):
                vertex.lowestclone = self

        def __repr__(self):
            ''' override output method - for debug '''
            return f'{self.vertex.key}'

    def __init__(self, node: Vertex or Clone, clone=False, isvertex=False):
        if(clone):
            self.root = node
            self.height = node.vertex.highclonelevel
        else:
            self.root = self.Clone(node, isvertex)
            self.height = 0
        # self.numv = 1

    def __repr__(self):
        ''' override output method - for debug '''
        return f'{self.root}'


class QuakeHeap(Heap):
    def __init__(self, vertex: Vertex = None):
        # invariant used for seismic operation
        self.alpha = 3/4
        # 2d list of trees, outer index corresponds to height of trees
        # inner lists are list of TournamentTrees
        self.trees = []
        self.trees.append([])
        # pointer to tree with minimum root
        self.min = None
        # number of vertices on each level
        self.numv = []
        self.numv.append(0)
        if(vertex is not None):
            self.insert(vertex)
            self.numv[0] += 1

    # insert a new element, creating new tree, update min root
    def insert(self, vertex: Vertex):
        t = TournamentTree(vertex, isvertex=True)
        self.trees[0].append(t)
        if (self.min is None or vertex.key < self.min.vertex.key):
            self.min = t.root
        self.numv[0] += 1
        # we need to maintain a length of the maximum number of nodes
        # amortize to O(1)?
        while(len(self.numv) < math.log(self.numv[0], (1/self.alpha))):
            self.numv.append(0)

    '''add a tree to the internal list of trees'''

    def _add_tree(self, tree):
        while(len(self.trees) <= tree.height):
            self.trees.append([])
        self.trees[tree.height].append(tree)

    '''
    _link two trees during a "recursive" _merge
    assumes equal height
    '''

    def _link(self, tree1: TournamentTree, tree2: TournamentTree):
        # _link trees
        minroot = min(tree1.root.vertex, tree2.root.vertex)

        # create a new tree with root being a clone of the minimum root of subtrees
        n = TournamentTree(minroot)
        n.root.left = tree1.root
        n.root.right = tree2.root
        tree1.root.parent = n.root
        tree2.root.parent = n.root

        # update height
        n.height = tree1.height + 1
        n.root.vertex.highclonelevel += 1
        minroot.highestclone = n.root

        # update level count
        self.numv[n.height] += 1
        if (self.min is None or n.root.vertex.key < self.min.vertex.key):
            self.min = n.root
        # add to list of trees
        self._add_tree(n)

    # perform merging on trees with the same height
    def _merge(self):
        for L in self.trees:
            # search for new min node among trees
            curr_min = float('inf')
            for l in L:
                if (l.root.vertex.key < curr_min):
                    self.min = l.root
                    curr_min = self.min.vertex.key
            # _link as long as there are two trees with the same height
            # min will make it's way to the top anyway so above is safe
            while (len(L) >= 2):
                self._link(L[0], L[1])
                L.pop(0)
                L.pop(0)

    '''_cut a node from its parent'''

    def _cut(self, node: TournamentTree.Clone):
        # if highest vertex is root
        if(node.parent is None):
            return
        if(node.parent.left == node):
            node.parent.left = None
        else:
            node.parent.right = None

        # then _cut from node parent
        node.parent = None

    '''take a Vertex object and decrease its value to value'''

    def decrease_key(self, vertex: Vertex, value):
        # update value of vertex, updating all clones by default
        vertex.key = value
        # _cut from parent
        # check which side to _cut from parent's child reference

        # if the highest clone is a root (no parents) update min to new root
        if(vertex.highestclone.parent == None):
            if(self.min == None or vertex.highestclone.vertex.key < self.min.vertex.key):
                self.min = vertex.highestclone
            return

        self._cut(vertex.highestclone)
        # add a new tree of height of this tree
        newtree = TournamentTree(vertex.highestclone, clone=True)
        if (self.min is None or vertex.key < self.min.vertex.key):
            self.min = newtree.root
        newtree.height = vertex.highclonelevel
        self.trees[newtree.height].append(newtree)

    '''deletes the min vertex in heap'''

    def extract_min(self):
        # walk up from vertex clone _cutting itself from parents
        quake_needed = False
        quake_level = 0
        min_vert = self.min.vertex
        curr = self.min.vertex.lowestclone
        heightcount = 0
        if (curr.parent is None):
            for t in self.trees[self.min.vertex.highclonelevel]:
                if (t.root == curr):
                    self.trees[self.min.vertex.highclonelevel].remove(t)
                    self.numv[t.height] -= 1
                    break
        else:
            # _cut up
            # highest clone should always be root in extract_min
            while(curr.vertex.highestclone is not curr):
                # see which side current node came from
                # _cut the other side
                self.numv[heightcount] -= 1
                '''
                #!check for seismic operation
                N(i+1) must be less than or equal to alpha * N(i)
                '''
                if((heightcount+1 < len(self.numv)) and (self.numv[heightcount+1]/self.numv[heightcount] > self.alpha)):
                    quake_needed = True
                    quake_level = heightcount+1

                if(curr.parent.left.vertex == curr.vertex):
                    if(curr.parent.right is not None):
                        addnode = curr.parent.right
                        self._cut(curr.parent.right)
                        curr.right = None
                else:
                    if(curr.parent.left is not None):
                        addnode = curr.parent.left
                        self._cut(curr.parent.left)
                        curr.left = None
                curr = curr.parent

                # add to tree list
                n = TournamentTree(addnode, clone=True,
                                   isvertex=addnode.isvertex)
                n.height = addnode.vertex.highclonelevel
                self._add_tree(n)
                heightcount += 1

            # now at the root, remove from tree list, add other child
            for t in self.trees[self.min.vertex.highclonelevel]:
                if (t.root == curr):
                    self.trees[self.min.vertex.highclonelevel].remove(t)
                    self.numv[t.height] -= 1
                    break

        # recursive _merge trees of same height
        self._merge()

        if(quake_needed):
            self._seismic_event(quake_level)
        
        return min_vert

    '''performs DFS during quake operation, removing all the nodes at level "level" and above'''

    def _dfs_delete(self, currheight, targetlevel, node):
        if(node == None):
            return
        # decrement if successful traversal down a node a level, we will be deleting the previous levels
        self.numv[currheight] -= 1
        if(currheight == targetlevel):
            if(node.left is not None):
                node.left.parent = None
                addnode = node.left
            if(node.right is not None):
                node.right.parent = None
                addnode = node.left
            # add to tree list
            n = TournamentTree(addnode, clone=True,
                               isvertex=addnode.isvertex)
            n.height = currheight-1
            n.root.vertex.highclonelevel = n.height
            n.root.vertex.highestclone = n.root
            self._add_tree(n)
            node.left = None
            node.right = None
        else:
            self._dfs_delete(currheight-1, targetlevel, node.left)
            self._dfs_delete(currheight-1, targetlevel, node.right)

    '''perform quake operation'''

    def _seismic_event(self, level):
        # print("QUAKKKEEEEEEEEEEE at level: ", level)
        '''height of tree must be at least equal to level
        loop through trees, with at least that level
        '''
        for i in range(level, len(self.trees)):
            for tree in self.trees[i]:
                self._dfs_delete(i, level, tree.root)
                # within DFS Delete we create new trees, delete the original tree from list
                self.trees[i].remove(tree)
        # we find a new min here
        self._merge()

    '''return the minimum VERTEX'''

    def peak_min(self):
        return self.min.vertex if self.min is not None else None

    '''print human readable heap'''

    def show(self):
        for i in range(0, len(self.trees)):
            print("Height", i, ": ")
            for L in self.trees[i]:
                self._print_tree(L.root)
                print("-------------------------------")
    '''called by show method to print tree'''
    # source: https://stackoverflow.com/questions/34012886/print-binary-tree-level-by-level-in-python

    def _print_tree(self, root, level=0):
        if root != None:
            self._print_tree(root.left, level + 1)
            print(' ' * 4 * level + '->', root.vertex)
            self._print_tree(root.right, level + 1)


qh = QuakeHeap()
v8 = Vertex(8)
v1 = Vertex(1)
v2 = Vertex(2)
v3 = Vertex(3)
v4 = Vertex(4)
v5 = Vertex(5)
v6 = Vertex(6)
v7 = Vertex(7)


qh.insert(v1)
qh.insert(v2)
qh.insert(v3)
qh.insert(v4)
qh.insert(v5)
qh.insert(v6)
qh.insert(v7)
print(qh.extract_min())
# qh.insert(v8)
# qh.extract_min()


# qh.decrease_key(v4, 0)
# qh.extract_min()
# qh.decrease_key(v5, 0)
# qh.extract_min()
print("Min node: ", qh.peak_min())


# # print(v2.highclonelevel)
# qh.extract_min()
# # print(qh.numv)
# print(qh.peak_min())

# print(qh.numv)
qh.show()


# print(qh.trees)

# print(v5.highclonelevel)
# print(qh.peak_min())

# qh._merge()
# qh.extract_min()

# qh.decrease_key(v2, 1)


# qh.show()

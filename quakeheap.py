import heapq
import itertools

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

    def deleteMin(self):
        ''' delete minimum '''

    def decreaseKey(self, vertex, key):
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
            vertex.highestclone = self
            self.left = self.right = self.parent = None
            self.isvertex = isvertex

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
        # 2d list of trees, outer index corresponds to height of trees
        # inner lists are list of TournamentTrees
        self.trees = []
        self.trees.append([])
        # pointer to tree with minimum root
        self.min = None
        # number of vertices on the lowest level
        self.no = 0
        if(vertex is not None):
            self.insert(vertex)
            self.no += 1

    # insert a new element, creating new tree, update min root
    def insert(self, vertex: Vertex):
        t = TournamentTree(vertex, isvertex=True)
        self.trees[0].append(t)
        if (self.min is None or vertex < self.min.vertex):
            self.min = t.root
        self.no += 1

    # link two trees during a "recursive" merge
    # assumes equal height

    def link(self, tree1: TournamentTree, tree2: TournamentTree):
        # link trees
        minroot = min(tree1.root.vertex, tree2.root.vertex)

        n = TournamentTree(minroot)
        n.root.left = tree1.root
        n.root.right = tree2.root
        tree1.root.parent = n.root
        tree2.root.parent = n.root

        # update height
        n.height = tree1.height + 1
        n.root.vertex.highclonelevel += 1
        minroot.highestclone = n.root

        if (self.min is None or n.root.vertex < self.min.vertex):
            self.min = n.root

        # add to list of trees
        #!This is not a good way to do this
        while(len(self.trees) <= n.height):
            self.trees.append([])
        self.trees[n.height].append(n)

    # perform merging on trees with the same height
    def merge(self):
        for L in self.trees:
            while (len(L) >= 2):
                self.link(L[0], L[1])
                L.pop(0)
                L.pop(0)

    '''cut a node from its parent'''
    def cut(self, node: TournamentTree.Clone):
        # if highest vertex is root
        if(node.parent is None):
            return
        if(node.parent.left == node):
            node.parent.left = None
        else:
            node.parent.right = None

        # then cut from node parent
        node.parent = None


    '''take a Vertex object and decrease its value to value'''

    def decreaseKey(self, vertex: Vertex, value):
        # update value of vertex, updating all clones by default
        vertex.key = value
        # cut from parent
        # check which side to cut from parent's child reference

        if(vertex.highestclone.parent == None):
            if(self.min == None or vertex.highestclone.vertex < self.min.vertex):
                self.min = vertex.highestclone
            return

        self.cut(vertex.highestclone)
        # add a new tree of height of this tree
        newtree = TournamentTree(vertex.highestclone, clone=True)
        if (self.min is None or vertex < self.min.vertex):
            self.min = newtree.root
        newtree.height = vertex.highclonelevel
        self.trees[newtree.height].append(newtree)


    '''deletes the min vertex in heap'''
    def deleteMin(self):
        # walk down from highest clone cutting itself from parents
        self.no -= 1
        curr = self.min
        #always a root of a tree, remove from tree list
        for t in self.trees[self.min.vertex.highclonelevel]:
            if (t.root == curr):
                self.trees[self.min.vertex.highclonelevel].remove(t)
                break
        addnode = None

        #cut down all subtrees
        while(curr.isvertex is False):
            #see which side current node came from
            #cut the other side
            if(curr.left != None and curr.left.vertex == curr.vertex):
                addnode = curr.right
                self.cut(curr.right)
                curr = curr.left
            else:
                addnode = curr.left
                self.cut(curr.left)
                curr = curr.left
            
            # add to tree list
            n = TournamentTree(addnode, clone=True, isvertex=addnode.isvertex)
            n.height = addnode.vertex.highclonelevel
            #!This is not a good way to do this
            while(len(self.trees) <= n.height):
                self.trees.append([])
            n.height = addnode.vertex.highclonelevel
            self.trees[n.height].append(n)
        #now at the vertex
        self.cut(curr)
        del(curr)
        
        #recursive merge trees of same height
        self.merge()

        # search for new min node among trees
        inf = float('inf')
        for t in self.trees:
            for l in t:
                if (l.root.vertex.key < inf):
                    self.min = l.root



    def peakMin(self):
        return self.min.vertex

    '''print human readable tree'''

    def show(self):
        for i in range(0, len(self.trees)):
            print("Height", i, ": ")
            for L in self.trees[i]:
                self.printTree(L.root)
                print("-------------------------------")
    '''called by show method to print tree'''
    # source: https://stackoverflow.com/questions/34012886/print-binary-tree-level-by-level-in-python

    def printTree(self, root, level=0):
        if root != None:
            self.printTree(root.left, level + 1)
            print(' ' * 4 * level + '->', root.vertex)
            self.printTree(root.right, level + 1)


qh = QuakeHeap()
v1 = Vertex(1)
v2 = Vertex(2)
v3 = Vertex(3)
v4 = Vertex(4)
v5 = Vertex(5)
v6 = Vertex(6)


qh.insert(v1)
qh.insert(v2)
qh.insert(v3)
qh.insert(v4)
qh.deleteMin()
qh.insert(v5)
qh.insert(v6)
qh.merge()
# qh.decreaseKey(v2, 21)
qh.decreaseKey(v4, 0)
qh.decreaseKey(v3, 1)




# print(v2.highclonelevel)
qh.deleteMin()
qh.show()

print(qh.trees)

print(v5.highclonelevel)
# print(qh.peakMin())

# qh.merge()
# qh.deleteMin()

# qh.decreaseKey(v2, 1)



# qh.show()

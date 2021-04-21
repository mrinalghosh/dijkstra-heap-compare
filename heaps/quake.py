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
        if (self.min is None or vertex < self.min.vertex):
            self.min = t.root
        self.numv[0] += 1
        # we need to maintain a length of the maximum number of nodes
        # amortize to O(1)?
        while(len(self.numv) < math.log(self.numv[0], (1/self.alpha))):
            self.numv.append(0)

    '''add a tree to the internal list of trees'''

    def addTree(self, tree):
        while(len(self.trees) <= tree.height):
            self.trees.append([])
        self.trees[tree.height].append(tree)

    '''
    link two trees during a "recursive" merge
    assumes equal height
    '''

    def link(self, tree1: TournamentTree, tree2: TournamentTree):
        # link trees
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
        if (self.min is None or n.root.vertex < self.min.vertex):
            self.min = n.root
        # add to list of trees
        self.addTree(n)

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
        # walk up from vertex clone cutting itself from parents
        quake_needed = False
        quake_level = 0
        curr = self.min.vertex.lowestclone
        heightcount = 0
        if (curr.parent is None):
            for t in self.trees[self.min.vertex.highclonelevel]:
                if (t.root == curr):
                    self.trees[self.min.vertex.highclonelevel].remove(t)
                    self.numv[t.height] -= 1
                    break
        else:
            # cut up
            # highest clone should always be root in deleteMin
            while(curr.vertex.highestclone is not curr):
                # see which side current node came from
                # cut the other side
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
                        self.cut(curr.parent.right)
                        curr.right = None
                else:
                    if(curr.parent.left is not None):
                        addnode = curr.parent.left
                        self.cut(curr.parent.left)
                        curr.left = None
                curr = curr.parent

                # add to tree list
                n = TournamentTree(addnode, clone=True,
                                   isvertex=addnode.isvertex)
                n.height = addnode.vertex.highclonelevel
                self.addTree(n)
                heightcount += 1

            # now at the root, remove from tree list, add other child
            for t in self.trees[self.min.vertex.highclonelevel]:
                if (t.root == curr):
                    self.trees[self.min.vertex.highclonelevel].remove(t)
                    self.numv[t.height] -= 1
                    break

        # recursive merge trees of same height
        self.merge()

        # search for new min node among trees
        curr_min = float('inf')
        for t in self.trees:
            for l in t:
                if (l.root.vertex.key < curr_min):
                    self.min = l.root
                    curr_min = self.min.vertex.key
        if(quake_needed):
            self.seismicEvent(quake_level)

    '''performs DFS during quake operation, removing all the nodes at level "level" and above'''
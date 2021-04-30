# Created by Camden Kronhaus
import sys
sys.path.append("..")
import math
class TournamentTree:
    '''
    Clone class maintains a pointer to vertex objects for O(1) updates
    '''
    class Clone:
        '''
        To maintain consistency, bottom level is a clone node with isvertex set to true
        All other clones default to false
        '''

        def __init__(self, data: dict = None, name=None, isvertex=False):
            if(isvertex):
                self.key = data["key"]
                self.highestclone = self
                self.highestclonelevel = 0
                self.data = data
                self.name = name
            self.vertex = self
            self.left = self.right = self.parent = None
            self.isvertex = isvertex


        def __repr__(self):
            ''' override output method - for debug '''
            return f'{self.vertex.name, self.vertex.key}'

    def __init__(self, node: Clone):
            self.root = node
            self.height = node.vertex.highestclonelevel

    def __repr__(self):
        ''' override output method - for debug '''
        return f'{self.root}'


class QuakeHeap():
    def __init__(self):
        self.alpha = 3/4 # invariant used for seismic operation
        # 2d list of trees, outer index corresponds to height of trees
        # inner lists are list of TournamentTrees
        self.trees = []
        self.trees.append([])
        self.min = None # pointer to tree with minimum root
        self.numv = [] # number of vertices on each level, index is level
        self.numv.append(0)

    def __len__(self):
        return self.numv[0]
    '''
    Insert a new element, creating new tree, update min root
    '''
    def insert(self, data: dict, name=None):
        new_node = TournamentTree.Clone(data, name, isvertex=True)
        t = TournamentTree(new_node) #Create a new tree when inserting
        self.trees[0].append(t) #append new tree to level 0
        if (self.min is None or data["key"] < self.min.vertex.key): #if there is no min node, or inserted key is less than min node, update min node
            self.min = t.root
        self.numv[0] += 1 #increment number of nodes at lowest level
        while(len(self.numv) < math.log(self.numv[0], (1/self.alpha))): # we need to maintain a length of the maximum number of nodes
            self.numv.append(0)

        return new_node

    '''Add a tree to the internal list of trees'''

    def _append_tree(self, tree):
        while(len(self.trees) <= tree.height):
            self.trees.append([])
        self.trees[tree.height].append(tree)

    '''
    Compares two Clones, and returns the minimum
    '''
    def _give_min(self, node1: TournamentTree.Clone, node2: TournamentTree.Clone):
        if(node1.vertex.key <= node2.vertex.key):
            return node1
        else:
            return node2

    
    '''
    Link two trees during a "recursive" merge. Assumes equal height trees
    '''

    def _link(self, tree1: TournamentTree, tree2: TournamentTree):
        # Clone min of two roots, to become a new tree root
        minroot = self._give_min(tree1.root, tree2.root)
        newroot = TournamentTree.Clone()
        newroot.vertex = minroot.vertex

        # Create a new tree with root being a clone of the minimum root of subtrees
        t = TournamentTree(newroot)
        t.root.left = tree1.root
        t.root.right = tree2.root
        t.height = tree1.height + 1
        t.root.vertex = minroot.vertex
        

        
        tree1.root.parent = t.root
        tree2.root.parent = t.root
        minroot.vertex.highestclone = newroot
        minroot.vertex.highestclonelevel += 1
       
        
        


        # Update level count
        self.numv[t.height] += 1
        if (self.min is None or newroot.vertex.key < self.min.vertex.key):
            self.min = t.root
        # Add to list of trees
        self._append_tree(t)

    '''
    Perform merging on trees with the same height
    '''
    def _merge(self):
        a = 0
        curr_min = float('inf')
        backup_min = 0

        for L in self.trees:
            # Search for new min node among trees
            for l in L:
                if (l.root.vertex.key <= curr_min):
                    if (l.root.vertex.key < curr_min):
                        self.min = l.root
                        curr_min = self.min.vertex.key
                    else:
                        if(backup_min == 0):
                            backup_min = l.root
                # Link as long as there are two trees with the same height
                # Min will make it's way to the top anyway so above is safe
            while (len(L) >= 2):
                self._link(L[0], L[1])
                L.pop(0)
                L.pop(0)
        if(curr_min == float('inf')):
            self.min = backup_min
       
    '''Cut a node from its parent'''

    def _cut(self, node: TournamentTree.Clone):
        
        '''
        If highest vertex is root do nothing.
        Otherwise we need to check where we need to cut from (whether it is a left or right child) 
        and set parent's child to none
        '''
        if(node.parent is None):
            return
        if(node.parent.left == node):
            node.parent.left = None
        else:
            node.parent.right = None

        # Then cut from parent
        node.parent = None

    '''Take a Vertex object and decrease its value to value'''

    def decrease_key(self, node: TournamentTree.Clone, value):
        if value >= node.vertex.key:
            raise ValueError("Cannot decrease key with value >= current key")
        # Update value of vertex, updating all clones by default
        node.key = value

        '''
        If the highest clone is a root (no parents) update min if necessary
        then do not cut and return
        '''
        if(node.vertex.highestclone.parent == None):
            if(self.min == None or node.vertex.highestclone.vertex.key < self.min.vertex.key):
                self.min = node.vertex.highestclone
            return
        
        # Cut highest clone and decsendents of decreased key and create a new tree from node
        self._cut(node.vertex.highestclone)
        newtree = TournamentTree(node.vertex.highestclone)
        self._append_tree(newtree)
        # Update min
        if (self.min is None or node.vertex.key < self.min.vertex.key):
            self.min = newtree.root

    '''Removes the min vertex in heap and returns it'''

    def extract_min(self):
        # Walk up from vertex, cutting itself from parents
        quake_needed = False
        quake_level = 0
        curr = self.min.vertex
        min_node = self.min.vertex
        # Heightcount keeps track of current tree level as we walk up
        heightcount = 0 

        #If the min node is a lone vertex (no parents), simply find and remove, O(n)
        if (curr.parent is None):
            for t in self.trees[self.min.vertex.highestclonelevel]:
                if (t.root == curr):
                    self.trees[self.min.vertex.highestclonelevel].remove(t)
                    self.numv[t.height] -= 1
        else:
            # Cut up
            # Highest clone should always be root in extract_min
            while(curr.vertex.highestclone is not curr):
                addnode = None

                #Every level passed is a level that will be have one less node
                self.numv[heightcount] -= 1
                '''
                #!check for seismic operation
                N(i+1) must be less than or equal to alpha * N(i)
                '''
                if((heightcount+1 < len(self.numv)) and (self.numv[heightcount+1]/self.numv[heightcount] > self.alpha)):
                    quake_needed = True
                    quake_level = heightcount+1

                '''
                Cut as we go, checking which side the vertex came from, adding other side to a new tree
                Addnode keeps track of node on the other side
                If current clone is on the left, add right not if there is one
                '''    
                if(curr.parent.left is not None and curr.parent.left.vertex == curr.vertex):
                    if(curr.parent.right is not None):
                        addnode = curr.parent.right
                        self._cut(curr.parent.right)
                        curr.right = None
                else:
                    if(curr.parent.left is not None):
                        addnode = curr.parent.left
                        self._cut(curr.parent.left)
                        curr.left = None
                if(addnode is not None):
                    # Add addnode to tree list
                    n = TournamentTree(addnode)
                    n.height = addnode.vertex.highestclonelevel
                    self._append_tree(n)
                
                # Go up a level
                curr = curr.parent
                heightcount += 1

            # Now at the root, remove from tree list, add other child
            for t in self.trees[self.min.vertex.highestclonelevel]:
                if (t.root == curr):
                    self.trees[self.min.vertex.highestclonelevel].remove(t)
                    self.numv[t.height] -= 1
                    break

        # recursive _merge trees of same height
        self._merge()

        if(quake_needed):
            self._seismic_event(quake_level)
        
        return min_node

    '''Performs DFS during quake operation, removing all the nodes at level "level" and above.
        Takes a currentheight of the tree, and traverses down to the left and right attempting to reach the target level.
        If target level is reached, disconnect above nodes, add subtrees to tree list.'''

    def _dfs_delete(self, currheight, targetlevel, node):
        if(node == None):
            return
        # Decrement if successful traversal down a node a level, we will be deleting the previous levels
        self.numv[currheight] -= 1
        if(currheight == targetlevel):
            if(node.left is not None):
                node.left.parent = None
                addnode = node.left
                 # add to tree list
                n = TournamentTree(addnode)
                n.height = currheight-1
                n.root.vertex.highestclonelevel = n.height
                n.root.vertex.highestclone = n.root
                self._append_tree(n)
            if(node.right is not None):
                node.right.parent = None
                addnode = node.right
                # add to tree list
                n = TournamentTree(addnode)
                n.height = currheight-1
                n.root.vertex.highestclonelevel = n.height
                n.root.vertex.highestclone = n.root
                self._append_tree(n)
           
            node.left = None
            node.right = None
        else:
            self._dfs_delete(currheight-1, targetlevel, node.left)
            self._dfs_delete(currheight-1, targetlevel, node.right)

    '''Perform quake operation'''

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

    '''Return the minimum vertex in the heap'''

    def _peak_min(self):
        return self.min.vertex if self.min is not None else None

    '''Print human readable heap'''

    def show(self):
        for i in range(0, len(self.trees)):
            print("Height", i, ": ")
            for L in self.trees[i]:
                self._print_tree(L.root)
                print("-------------------------------")
    '''Called by show method to print tree
            source: https://stackoverflow.com/questions/34012886/print-binary-tree-level-by-level-in-python
    '''

    def _print_tree(self, root, level=0):
        if root != None:
            self._print_tree(root.left, level + 1)
            print(' ' * 4 * level + '->', root.vertex)
            self._print_tree(root.right, level + 1)





import networkx as nx
# def dijkstra_path_heaps(G: nx.DiGraph, source, target, heap_choice):
    

#     G.nodes["a"]["key"] = 0

#     for n in G.nodes:
#         G.nodes[n]["node"] = heap.insert(G.nodes[n], n)

#     while heap:
#         n = heap.extract_min()
#         for edge in G.edges(n.name):
#             u, v = edge
#             dist = G.nodes[u]["key"] + G[u][v]["weight"]
#             if G.nodes[v]["key"] > dist:
#                 G.nodes[v]["key"] = dist
#                 G.nodes[v]["pred"] = u
#                 heap.decrease_key(G.nodes[v]["node"], dist)

#     path = []
#     path.append(target)
#     pred = G.nodes[target]["pred"]
#     while pred is not None:
#         path.append(pred)
#         pred = G.nodes[pred]["pred"]
#     path.reverse()
#     return path


# if __name__ == "__main__":
#     heap = QuakeHeap()
#     G = nx.Graph()

#     G.add_node("a")
#     G.add_node("b")
#     G.add_node("c")
#     G.add_node("d")
#     G.add_node("e")
#     G.add_node("f")
#     G.nodes["a"]["key"] = 0
#     G.nodes["b"]["key"] = 1
#     G.nodes["c"]["key"] = 2
#     G.nodes["d"]["key"] = 3
#     G.nodes["e"]["key"] = 4
#     G.nodes["f"]["key"] = 5



#     for n in G.nodes:
#         G.nodes[n]["node"] = heap.insert(G.nodes[n], n)

#     print("Extracted min: ", heap.extract_min())
#     heap.decrease_key(G.nodes["d"]["node"], 0)
#     heap.decrease_key(G.nodes["e"]["node"], -1)
#     heap.show()
#     print("Peak min: ", heap.peak_min())

#     # path = nx.dijkstra_path(G, source="a", target="z")
#     # print(path)

# heap = QuakeHeap()
# heap.insert({"key": 5})
# heap.insert({"key": 4})
# heap.insert({"key": 7})
# heap.insert({"key": 9})
# heap.insert({"key": 67})
# print(heap._peak_min())
# print("Extracted min: ", heap.extract_min()) # Extract 4
# print(heap._peak_min())
# print("Extracted min: ", heap.extract_min()) # Extract 5
# print(heap._peak_min())
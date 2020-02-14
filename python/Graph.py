#
# File:    Graph.py
# Author:  Alex Stivala
# Created: Feburary 2020
#
# Defines the undirected graph structure Graph with edge list graph
# representation
#

class Graph:
    """
    The network is represented as a dictionary of dictionaries.
    Nodes are indexed by integers 0..n-1. The outermost dictionary has the node
    v as a key, and dictionary as value. Then this dictionary has the neighbours
    of v as the keys, and here simply 1 as value (there are no edge weights).

    So G[i] is a dictionary with k entries, where k is the degree of node i.
    and G[i][j] exists (and has value 1) exactly when j is a neighbour of i.
    And simple operations are:
      degree of node i:                      len(G[i])
      does edge i--j exist?:                 j in G[i]                 
      dict where keys are  neighbours of i:  G[i]
      iterator over neighbourhood of i       G[i].iterkeys()
      in-place insert edge i--j:             G[i][j] = 1
      in-place remove edge i--j:             G[i].pop(j) 
      copy of G (not modified when G is):    deepcopy(G)
      number of edges:              sum([len(v.keys()) for v in G.itervalues()])
    To make these operations simple (no special cases for nodes with no
    neighbours),  the graph is initialized so that G[i] = dict() for
    all 0 <= i < n: dict(zip(range(n), [dict() for i in range(n)]))

    For simplicity in undirected graph, we always store both the edge i -- j
    and the edge j -- i.

    Node attributes are stored in a separate list, which is simply
    indexed by node id i.e. a simple list of the attribute values in
    node id order.
    """

    def __init__(self, pajek_edgelist_filename, binattr_filename=None,
                 contattr_filename=None):
        """
        Construct graph from Pajek format network and binary attributes.

        Parameters:
            pajek_edgelist_filename - edge list in Pajek format
            binattr_filename  - binary attributes
                                Default None: no binary attributes loaded
            contattr_filename - continuous attributes
                                Default None: no continuous attributes loaded
        """
        self.G = None  # dict of dicts as described above
        self.binattr = None # binary attributes: list by node (int not boolean)
        self.contattr = None # continuous attributes: list by node

        f =  open(pajek_edgelist_filename)
        l = f.readline() # first line must be e.g. "*vertices 500"
        n = int(l.split()[1])

        # empty graph n nodes        
        self.G = dict(zip(range(n), [dict() for i in range(n)]))

        while l.rstrip().lower() != "*edges":
            l = f.readline()
        lsplit = f.readline().split()
        while len(lsplit) == 2:
            (i, j) = map(int, lsplit)
            assert(i >= 1 and i <= n and j >= 1 and j <= n)
            self.insertEdge(i-1, j-1)    # input is 1-based but we are 0-based
            lsplit = f.readline().split()

        if binattr_filename is not None:
            self.binattr = map(int, open(binattr_filename).read().split()[1:]) 
            assert(len(self.binattr) == n)

        if contattr_filename is not None:
            self.contattr = map(float, open(contattr_filename).read().split()[1:])
            assert(len(self.contattr) == n)


    def numNodes(self):
        """
        Return number of nodes in graph
        """
        return len(self.G)
    
    def numEdges(self):
        """
        Return number of edges in graph
        """
        return sum([len(v.keys()) for v in self.G.itervalues()])/2
    
    def density(self):
        """
        Return the graph density 
        """
        edges = self.numEdges()
        nodes = self.numNodes()
        return float(edges) / (float(nodes*(nodes-1)) / 2.0)

    def degree(self, i):
        """
        Return degree of node i
        """
        return len(self.G[i])

    def isEdge(self, i, j):
        """
        Return True iff edge i -- j in graph
        """
        return j in self.G[i]

    def neighbourIterator(self, i):
        """
        Return iterator over neighbours of i
        """
        return self.G[i].iterkeys()

    def insertEdge(self, i, j):
        """
        Insert edge i -- j in place
        """
        self.G[i][j] = 1
        self.G[j][i] = 1


    def removeEdge(self, i, j):
        """
        Delete edge i -- j in place
        """
        self.G[i].pop(j)
        self.G[j].pop(i)



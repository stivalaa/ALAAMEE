#
# File:    Graph.py
# Author:  Alex Stivala
# Created: Feburary 2020
#
# Defines the undirected graph structure Graph with edge list graph
# representation
#

import math
import functools
from utils import int_or_na,float_or_na,NA_VALUE

from numba import jitclass


@jitclass
class Graph:
    """The network is represented as a dictionary of dictionaries.
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

    In the Pajek format *vertices at top, then followed by one line for each
    vertex (just vertex number) then *arcs (or *edges for undirected)
    followed by arcs list one per
    line. For this program the nodes must be numbered 1..N.

    The format of the attributes files is header line with
    whitespace-delimited attribute names, followed by (whitespace
    delimited) attributes one line per node (corresponding to node
    number order, i.e the first non-header line is for node is 0, the
    second for 1, etc.). E.g. (categorical):

    gender   class
    1        1
    0        2
    0        3

    Binary attributes must be 0 or 1; categorical positive integers, and
    continuous floating point. For NA values -1 is used for binary and
    categorical, and NaN for continuous.

    Node attributes (binary, continuous, categorical; separately)
    are each stored in a dictionary of lists. The key of the dictionary
    is the attribute name, and the value is a list which is simply
    indexed by node id i.e. a simple list of the attribute values in
    node id order. So e.g. the categorical attribute 'class' for node id 2
    (the third node, so row 4 in data which has header)
    would be catattr['class'][2]

    Also there can be optionally be a 'zone' for each node, which is
    the snowball sampling zone: 0 for the seed nodes, 1 for nodes
    reached directly from those in zone 0, and so on. These are read
    from a text file with zone number one per line for each node in
    order, with a header line that must just be one column name "zone", and
    stored simply as a list (in node id order just as for attributes).

    """

    def __init__(self, pajek_edgelist_filename=None, binattr_filename=None,
                 contattr_filename=None, catattr_filename=None,
                 zone_filename=None,
                 num_nodes=None):
        """
        Construct graph from Pajek format network and binary attributes.

        Parameters:
            pajek_edgelist_filename - edge list in Pajek format
                                      If None then num_nodes must be
                                      used instead to make empty graph
                                      Default None
            binattr_filename  - binary attributes
                                Default None: no binary attributes loaded
            contattr_filename - continuous attributes
                                Default None: no continuous attributes loaded
            catattr_filename - categorical attributes
                                Default None: no categorical attributes loaded
            zone_filename    - snowball sample zone for each node
                                Deafult None: no zone information loaded
            num_nodes        - number of nodes in empty graph to create
                               (only if pajek_edgelist_filename = None)
                               Default None
        """
        assert not (num_nodes is not None and
                    pajek_edgelist_filename is not None)
        assert num_nodes is not None or pajek_edgelist_filename is not None
        self.G = None  # dict of dicts as described above
        self.binattr = None # binary attributes: dict name, list by node (int not boolean)
        self.contattr = None # continuous attributes: dict name, list by node
        self.catattr = None  # categorical attributes: dict name, list by node

        # for conditional estimation on snowball sampling structure
        self.zone    = None  # node snowball zone, list by node
        self.max_zone= None  # maximum snowball zone number
        self.inner_nodes = None # list of nodes with zone < max_zone

        if pajek_edgelist_filename is not None:
            f =  open(pajek_edgelist_filename)
            l = f.readline() # first line must be e.g. "*vertices 500"
            n = int(l.split()[1])
        else:
            n = num_nodes

        # empty graph n nodes        
        self.G = dict(list(zip(list(range(n)), [dict() for i in range(n)])))

        if pajek_edgelist_filename is not None:
            while l and l.rstrip().lower() != "*edges":
                l = f.readline()
            if not l:
                raise ValueError("no *edges in Pajek file " +
                                 pajek_edgelist_filename)
            lsplit = f.readline().split()
            while len(lsplit) >= 2:
                lsplit = lsplit[:2]  # only used first two (i,j) ignore weight
                (i, j) = list(map(int, lsplit))
                assert(i >= 1 and i <= n and j >= 1 and j <= n)
                self.insertEdge(i-1, j-1)    # input is 1-based but we are 0-based
                lsplit = f.readline().split()

        # Note in the following,
        #  map(list, zip(*[row.split() for row in open(filename).readlines()]))
        # reads the data and transposes it so we have a list of columns
        # not a list of rows, which then makes it easy to convert to
        # the dict where key is column header and value is list of values
        # (converted to the appropraite data type from sting with int_or_na()
        # etc.)
        # https://stackoverflow.com/questions/6473679/transpose-list-of-lists#
        
        if binattr_filename is not None:
            self.binattr = dict([(col[0], list(map(int_or_na, col[1:]))) for col in map(list, list(zip(*[row.split() for row in open(binattr_filename).readlines()])))])
            assert(all([len(v) == n for v in self.binattr.values()]))

        if contattr_filename is not None:
            self.contattr = dict([(col[0], list(map(float_or_na, col[1:]))) for col in map(list, list(zip(*[row.split() for row in open(contattr_filename).readlines()])))])
            assert(all([len(v) == n for v in self.contattr.values()]))

        if catattr_filename is not None:
            self.catattr = dict([(col[0], list(map(int_or_na, col[1:]))) for col in map(list, list(zip(*[row.split() for row in open(catattr_filename).readlines()])))])
            assert(all([len(v) == n for v in self.catattr.values()]))

        if zone_filename is not None:
            self.zone = [int(s) for s in open(zone_filename).readlines()[1:]]
            assert(len(self.zone) == n)
            self.max_zone = max(self.zone)
            assert(min(self.zone) == 0)
            assert(len(set(self.zone)) == self.max_zone + 1) # zones must be 0,1,..,max
            # get list of nodes in inner waves, i.e. with zone < max_zone
            self.inner_nodes = [i for (i, z) in enumerate(self.zone) if z < self.max_zone]

    def numNodes(self):
        """
        Return number of nodes in graph
        """
        return len(self.G)
    
    def numEdges(self):
        """
        Return number of edges in graph
        """
        # Since or simplicity in undirected graph, we always store both the
        # edge i -- j and the edge j -- i we have to divide by 2 here.
        # using // for integer (floor) division to keep result as int
        return sum([len(list(v.keys())) for v in self.G.values()])//2

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
        return iter(self.G[i].keys())

    def insertEdge(self, i, j):
        """
        Insert edge i -- j in place
        """
        assert i != j # do not allow loops (self-edges)
        self.G[i][j] = 1
        self.G[j][i] = 1


    def removeEdge(self, i, j):
        """
        Delete edge i -- j in place
        """
        self.G[i].pop(j)
        self.G[j].pop(i)


    def printSummary(self):
        """
        Print summary of Graph object
        """
        print('graph nodes = ', self.numNodes())
        print('graph edges = ', self.numEdges())
        print('graph density = ', self.density())


        if self.binattr is not None:
            for attrname in self.binattr.keys():
                print('Binary attribute', attrname, 'has', self.binattr[attrname].count(NA_VALUE), 'NA values')
        else:
            print('No binary attributes')
        if self.contattr is not None:
            for attrname in self.contattr.keys():
                print('Continuous attribute', attrname, 'has', sum([math.isnan(x) for x in self.contattr[attrname]]), 'NA values')
        else:
            print('No continuous attributes')
        if self.catattr is not None:
            for attrname in self.catattr.keys():
                print('Categorical attribute', attrname, 'has', self.catattr[attrname].count(NA_VALUE), 'NA values')
        else:
            print('No categorical attributes')

        if self.zone is not None:
            print('There are', self.max_zone, 'snowball sample waves, with', len(self.inner_nodes), 'nodes in inner waves')
        else:
            print('No snowball zones')
            

    def nodeIterator(self):
        """
        Return iterator over nodes of graph
        """
        return iter(self.G.keys())


    def edgeIterator(self):
        """
        Iterate over edges in graph

        This is a generator function that yields a tuple (i, j) for
        each edge (i, j) in the graph
        """
        # Since for simplicity in undirected graph, we always store
        # both the edge i -- j and the edge j -- i we will return only
        # those edges where i < j
        for i in self.G.keys():
            for j in self.G[i].keys():
                if i < j:
                    yield (i, j)


    @functools.cache # Memoize the twoPaths function (Python 3.9)
    def twoPaths(self, i, j):
        """
        Count undirected two-paths for (i, j): paths i -- v -- j for some v
        (where v is distinct from both i and j, which are also distinct)
        """
        return sum([(v in self.neighbourIterator(j)) for v in self.neighbourIterator(i)]) if i != j else 0


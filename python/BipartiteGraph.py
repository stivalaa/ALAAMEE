#
# File:    BipartiteGraph.py
# Author:  Alex Stivala
# Created: August 2022
#
# Defines the bipartite undirected graph structure BipartiteGraph
# with edge list graph, as a subclass of Graph
#

import sys
import random
import math
from Graph import Graph
from SparseMatrix import SparseMatrix
from utils import NA_VALUE



# Mode (node type) of a node for bipartite (two-mode) networks
MODE_A = 'A'
MODE_B = 'B'


class BipartiteGraph(Graph):
    """
    BipartiteGraph is a bipartite (two-mode) graph, implemented as a
    subclass of the undirected graph class Graph.

    
    This reads from the Pajek format for bipartite (two-mode) netwowkrs, 
    in which the first lines should be e.g.
    *vertices 36 10
    first number is total number of nodes
    second number is number of mode A nodes
    the rest are mode B - conventionally in the affiliation
    matrix the rows are mode A and the columns mode B, e.g. mode A is
    actors and mode B is their affiliations.
    They must be numbered 1 ... N where N = num_A + num_B
    so nodes 1 .. num_A are type A and num_A+1 .. N are type B
    see e.g. http://www.pfeffer.at/txt2pajek/txt2pajek.pdf
    
    """

    def __init__(self, pajek_edgelist_filename, binattr_filename=None,
                 contattr_filename=None, catattr_filename=None,
                 zone_filename=None):
        """
        Construct graph from Pajek format network and binary attributes.

        Parameters:
            pajek_edgelist_filename - edge list in Pajek format
            binattr_filename  - binary attributes
                                Default None: no binary attributes loaded
            contattr_filename - continuous attributes
                                Default None: no continuous attributes loaded
            catattr_filename - categorical attributes
                                Default None: no categorical attributes loaded
            zone_filename    - snowball sample zone for each node
                                Deafult None: no zone information loaded
        """
        f =  open(pajek_edgelist_filename)
        l = f.readline() # first line must be e.g. "*vertices 500 200"
        n = int(l.split()[1])
        f.close()

        # sparse matrix of two-path counts
        self.twoPathsMatrix = SparseMatrix(n)

        try:
            self.num_A_nodes = int(l.split()[2])
        except IndexError:
            raise ValueError('expecting "*vertices num_nodes num_A_nodes" for two-mode network')
        super().__init__(pajek_edgelist_filename, binattr_filename,
                         contattr_filename, catattr_filename, zone_filename)
        self.num_B_nodes = self.numNodes() - self.num_A_nodes
        assert(self.num_A_nodes <= self.numNodes())
        assert(n == self.numNodes())


        
    def density(self):
        """
        Return the graph density 
        """
        edges = self.numEdges()
        return float(edges) / float(self.num_A_nodes * self.num_B_nodes)

    
    def printSummary(self):
        """
        Print summary of Graph object
        """
        print('Bipartite graph')
        print('number of mode A nodes = ', self.num_A_nodes)
        print('number of mode B nodes = ', self.num_B_nodes)
        print('graph density = ', self.density())
        

        if self.binattr is not None:
            for attrname in self.binattr.keys():
                print('Binary attribute', attrname, 'has', self.binattr[attrname].count(NA_VALUE), 'NA values (', self.binattr[attrname][:self.num_A_nodes].count(NA_VALUE), 'in mode A and', self.binattr[attrname][self.num_A_nodes:].count(NA_VALUE), 'in mode B)' )
        else:
            print('No binary attributes')
        if self.contattr is not None:
            for attrname in self.contattr.keys():
                print('Continuous attribute', attrname, 'has', sum([math.isnan(x) for x in self.contattr[attrname]]), 'NA values (', sum([math.isnan(x) for x in self.contattr[attrname][:self.num_A_nodes]]), 'in mode A and ', sum([math.isnan(x) for x in self.contattr[attrname][self.num_A_nodes:]]), 'in mode B')
        else:
            print('No continuous attributes')
        if self.catattr is not None:
            for attrname in self.catattr.keys():
                print('Categorical attribute', attrname, 'has', self.catattr[attrname].count(NA_VALUE), 'NA values (', self.catattr[attrname][:self.num_A_nodes].count(NA_VALUE), 'in mode A and ', self.catattr[attrname][self.num_A_nodes:].count(NA_VALUE), 'in mode B')
        else:
            print('No categorical attributes')


        if self.zone is not None:
            print('There are', self.max_zone, 'snowball sample waves, with', len(self.inner_nodes), 'nodes in inner waves')
        else:
            print('No snowball zones')



    def bipartite_node_mode(self, i):
        """
        Return node type (mode) of node i
        """
        return MODE_A if i < self.num_A_nodes else MODE_B
                            

    def insertEdge(self, i, j):
        """
        Insert edge i -- j in place
        """
        if self.bipartite_node_mode(i) == self.bipartite_node_mode(j):
            raise ValueError("edge in bipartite graph inserted between nodes in same mode")
        super().insertEdge(i, j)
        self.updateTwoPathsMatrix(i, j)

    def nodeModeIterator(self, mode):
        """
        Return iterator over nodes of graph with supplied mode
        (MODE_A or MODE_B)
        """
        return filter(
            lambda v: self.bipartite_node_mode(v) == mode, self.G.keys())

    def updateTwoPathsMatrix(self, i, j):
        """
        Update the two-paths sparse matrix used for fast computation
        of some change statistics (specifically 4-cycles), for addition
        of the edge i -- j.
        """
        for u in self.neighbourIterator(i):
            if u == i or u == j:
                continue
            self.twoPathsMatrix.incrementValue(u, j)
            self.twoPathsMatrix.incrementValue(j, u)
        for u in self.neighbourIterator(j):
            if u == i or u == j:
                continue
            self.twoPathsMatrix.incrementValue(u, i)
            self.twoPathsMatrix.incrementValue(i, u)

    def random_node(self, mode):
        """
        Choose a node of the given mode (MODE_A or MODE_B) uniformly at random
        and return it.
        """
        assert mode == MODE_A or mode == MODE_B
        return (random.randint(0, self.num_A_nodes-1) if mode == MODE_A else
                random.randint(self.num_A_nodes, self.numNodes()-1))


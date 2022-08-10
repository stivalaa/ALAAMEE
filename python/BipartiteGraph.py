#
# File:    BipartiteGraph.py
# Author:  Alex Stivala
# Created: August 2020
#
# Defines the bipartite undirected graph structure BipartiteGraph
# with edge list graph, as a subclass of Graph
#

from Graph import Graph



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
        super().__init__(pajek_edgelist_filename, binattr_filename,
                         contattr_filename, catattr_filename, zone_filename)
        

    
    def density(self):
        """
        Return the graph density 
        """
        edges = self.numEdges()
        nodes = self.numNodes()
        return 9999 # float(edges) / float(num_A_nodes * num_B_nodes)

    
    def printSummary(self):
        """
        Print summary of Graph object
        """
        print('Bipartite graph')
        super().printSummary()

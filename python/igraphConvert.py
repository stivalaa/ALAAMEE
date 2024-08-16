#
# File:    igraphConvert.py
# Author:  Alex Stivala
# Created: August 2024
#
"""Convert igraph [https://igraph.org/] Python version (python-igraph)
[https://python.igraph.org/en/stable/] object to Graph, Digraph or
BipartiteGraphfor for ALAAMEE.

Citation for igraph:

   Gabor Csardi, Tamas Nepusz: The igraph software package for complex
   network research. InterJournal Complex Systems, 1695, 2006.

Although this article appears to be no longer available online; see also
the new preprint (not cited anywhere yet):

   Antonov, M., Csardi, G., Horvat, S., Muller, K., Nepusz, T., Noom,
   D., ... & Zanini, F. (2023). igraph enables fast and robust network
   analysis across programming languages. arXiv preprint
   arXiv:2311.10260.

Developed with igraph 0.11.6 on python 3.10.18 (Linux)
"""

import igraph
from Graph import Graph
from Digraph import Digraph
from BipartiteGraph import BipartiteGraph

def igraphConvert(g):
    """Convert the igraph.Graph object g to an ALAAMEE Graph, Digraph or 
    BipartiteGraph object as appropriate.

    Parameters:
        g - igraph.Graph object 

    Return value:
        If g is bipartite then BipartiteGraph, else if g is directed then
        Digraph, else Graph, representing the same graph as g.
    """

    # Note that in R/igraph, is_bipartite() just checks for the presence
    # of the 'type' node attribute. However in igraph-python, instead
    # it actually tests if the graph is bipartite i.e. equivalent to
    # bipartite_mapping() in R/igraph. This is not what we want here,
    # so we just check for the presence of the 'type' vertex attribute
    # directly (like R/igraph is_bipartite() does).
    if 'type' in g.vs[0].attribute_names():
        num_B = sum(g.vs['type'])
        num_A = g.vcount() - num_B
        gnew = BipartiteGraph(num_nodes = (num_A, num_B))
    elif g.is_directed():
        gnew = Digraph(num_nodes = g.vcount())
    else:
        gnew = Graph(num_nodes = g.vcount())

    # This depends on get_edgelist() returning list of tuples
    # representing edges (i, j) where nodes (i, j) are numbered from
    # 0..N-1, just as used in ALAAMEE Graph etc. internally
    for edge in g.get_edgelist():
        gnew.insertEdge(edge[0], edge[1])

    return gnew

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
from utils import NA_VALUE

def convert_to_int_cat(attrs):
    """
    convert_to_int_cat() - convert string categorical attrs to integer

    Like factor() in R, convert categories represented as strings into
    integers.

    Parameters:
       attrs - list of string attributes
    
    Return value:
       list of integer attributes corresponding to the strings
    
    """
    # build dict mapping string to integer for unique strings in attrs list
    fdict = dict([(y,x) for (x,y) in enumerate(set(attrs))])
    ##print(fdict) # output for possible future reversal (TODO write to file)
    return [NA_VALUE if x == 'NA' else fdict[x] for x in attrs]


def fromIgraph(g):
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
    if 'type' in g.vs.attribute_names():
        # for some reason type can be float (0.0 or 1.0) not int,
        # at least in python-igraph 0.9.9 for a bipartite graph read from
        # Pajek format, so convert to int
        # (if this is not done then node counts are also float and
        # causes type errors in e.g. constructing sparse matrix for two-paths)
        num_B = sum([int(i) for i in g.vs['type']])
        num_A = g.vcount() - num_B
        gnew = BipartiteGraph(num_nodes = (num_A, num_B))
    elif g.is_directed():
        gnew = Digraph(num_nodes = g.vcount())
    else:
        gnew = Graph(num_nodes = g.vcount())

    # This depends on get_edgelist() returning list of tuples
    # representing edges (i, j) where nodes (i, j) are numbered from
    # 0..N-1, just as used in ALAAMEE Graph etc. internally,
    # Note also we do not try to convert directly into internal
    # dict of dict representation, but instead use the insertEdge()
    # function, not only for consistency checks etc., but also
    # (in the case of BipartiteGraph for example) that other data
    # structures are kept up to date e,g,the sparse two-paths matrix
    # in BipartiteGraph.
    for edge in g.get_edgelist():
        gnew.insertEdge(edge[0], edge[1])

    # Now convert vertex attributes. Boolean atributes are converted to
    # binary attributes, float to continuous, and integer to categorical.
    # String attributes are converted to categorical by first being conerted
    # to integers repsrenting unique values, like as.factor() in R.
    for attrname in g.vs.attribute_names():
        if isinstance(g.vs[attrname][0], bool):
            if gnew.binattr is None:
                gnew.binattr = dict([(attrname,
                                      [int(x) for x in g.vs[attrname]])])
            else:
                gnew.binattr[attrname] = [int(x) for x in g.vs[attrname]]
        elif isinstance(g.vs[attrname][0], float):
            if gnew.contattr is None:
                gnew.contattr = dict([(attrname, list(g.vs[attrname]))])
            else:
                gnew.contattr[attrname] = list(g.vs[attrname])
        elif isinstance(g.vs[attrname][0], int):
            if gnew.catattr is None:
                gnew.catattr = dict([(attrname, list(g.vs[attrname]))])
            else:
                gnew.catattr[attrname] = list(g.vs[attrname])
        elif isinstance(g.vs[attrname][0], str):
            if gnew.catattr is None:
                gnew.catattr = dict([(attrname, convert_to_int_cat(g.vs[attrname]))])
            else:
                gnew.catattr[attrname] = convert_to_int_cat(g.vs[attrname])
        else:
            raise ValueError('Unsupported type ' +
                             str(type(g.vs[attrname][0])) +
                             ' for vertex attribute ' + attrname)
        
    return gnew



def toIgraph(g):
    """Convert the ALAAMEE Graph, Digraph or BipartiteGraph object to an
    igraph Graph object.

    Parameters:
        g - a Graph, Digraph or BipartiteGraph object

    Return value:
        igraph.Graph object representing same graph as g

    """
    # to_dict_dict() is not available in python-igraph 0.9.9?
    # so costructing igraph grpaph object this way instead.
    # Also note not just using igraph.Graph.TupleList() as this
    # infers the node count from the tuple (edge) list, so if there
    # are any isolates, they will be excluded and will have wrong number
    # of nodes.
    if isinstance(g, BipartiteGraph):
        pass
    else:
        gi = igraph.Graph(n = g.numNodes(), edges = g.edgeIterator(),
                          directed = isinstance(g, Digraph))
    return gi

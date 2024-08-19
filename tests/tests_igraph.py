#!/usr/bin/env python3
#
# File:    tests_igraph.py
# Author:  Alex Stivala
# Created: August 2024
#
"""Unit and regression tests for ALAAMEE igrph conversion
(i.e. conversion from igraph to ALAAMEE internal format, particularly
change statistics computations.

Developed with igraph 0.9.9 on python 3.9.16 (cygwin)

"""
import sys,os,time,random,gzip
from functools import partial
import numpy as np
try:
    import igraph
except ImportError:
    print("Could not import igraph, skipping tests.")
    sys.exit(0)

from igraphConvert import fromIgraph
from Graph import Graph
from Digraph import Digraph
from BipartiteGraph import BipartiteGraph,MODE_A,MODE_B
from changeStatisticsALAAMdirected import *
from changeStatisticsALAAM import changeDensity, param_func_to_label
from computeObservedStatistics import computeObservedStatistics

from bipartitematrix import read_bipartite_matrix,bipartite_to_adjmatrix


######################### test functions #####################################
#
##############################################################################

def test_undirected_graph():

    """
    test Graph object from igraph
    """
    print("testing Graph object converted from igraph...")
    start = time.time()
    g_igraph = igraph.Graph.Read("../examples/data/simulated_n1000_bin_cont/n1000_kstar_simulate12750000.txt", format="pajek")
    print(g_igraph.summary())
    g = fromIgraph(g_igraph)

    # specific to this graph
    assert g.numNodes() == 1000
    assert g.numEdges() == 3001
    assert round(g.density(), 9) == 0.006008008 # from R/igraph
    g.printSummary()

    # following must be true for any Graph
    assert len(list(g.nodeIterator())) == g.numNodes()
    assert all([g.isEdge(i, j) for i in g.nodeIterator() for j in g.neighbourIterator(i)])
    assert all([len(list(g.neighbourIterator(i))) == g.degree(i) for i in g.nodeIterator()])
    for i in g.nodeIterator():
        assert(len(list(g.neighbourIterator(i))) == len(set(g.neighbourIterator(i)))) # check no repeated neighbours in iterator
    assert g.numEdges() == len(list(g.edgeIterator()))

    # following must be true from any Graph constructed from igraph
    assert isinstance(g, Graph)
    assert round(g.density(), 9) == round(g_igraph.density(), 9)


    print("OK,", time.time() - start, "s")
    print()




def test_directed_graph():

    """
    test Digraph object from igraph
    """
    print("testing Digraph object converted from igraph...")
    start = time.time()
    datadir = os.path.join("..", "examples", "data", "directed", "HighSchoolFriendship")
    edgelist_text = gzip.open(os.path.join(datadir,"Friendship-network_data_2013.csv.gz"), mode="rt").readlines()
    edgelist_tuples = [tuple(s.split()) for s in edgelist_text]
    g_igraph = igraph.Graph.TupleList(edgelist_tuples, directed = True)
    
    print(g_igraph.summary())
    g = fromIgraph(g_igraph)

    # specific to this graph
    assert g.numNodes() == 134
    assert g.numArcs() == 668
    assert round(g.density(), 9) == 0.037481764 # calculated manually 
    g.printSummary()

    # following must be true for any Digraph
    assert len(list(g.nodeIterator())) == g.numNodes()
    assert all([g.isArc(i, j) for i in g.nodeIterator() for j in g.outIterator(i)])
    assert all([g.isArc(j, i) for i in g.nodeIterator() for j in g.inIterator(i)])    
    assert all([len(list(g.outIterator(i))) == g.outdegree(i) for i in g.nodeIterator()]) 
    assert all([len(list(g.inIterator(i))) == g.indegree(i) for i in g.nodeIterator()])   
    for i in g.nodeIterator():
        assert(len(list(g.outIterator(i))) == len(set(g.outIterator(i)))) # check no repeated neighbours in iterator
        assert(len(list(g.inIterator(i))) == len(set(g.inIterator(i)))) # check no repeated neighbours in iterator        

    # following must be true from any Digraph constructed from igraph
    assert isinstance(g, Digraph)
    assert round(g.density(), 9) == round(g_igraph.density(), 9)

    print("OK,", time.time() - start, "s")
    print()
    


def test_bipartite_graph():

    """
    test BipartiteGraph object from igraph
    """
    print("testing BipartiteGraph object converted from igraph...")
    start = time.time()
    datadir = os.path.join("..", "examples", "data", "bipartite", "Inouye_Pyke_pollinator_web/")
    #with open(os.path.join(datadir, "inouye_matrix.txt")) as f:
    #    biadj_matrix = [[int(num) for num in line.split()] for line in f]
    #Not available in python-igraph 0.9.9?: g_igraph = igraph.Graph.Biadjacency(biadj_matrix)
    with open(os.path.join(datadir, "inouye_matrix.txt")) as f:    
        (m, bipartite_graph) = read_bipartite_matrix(f)
    n = len(bipartite_graph)
    edgelist = []
    for i in range(n):
        for j in range(m):
            if j in bipartite_graph[i]:
                edgelist.append((i, n+j))
    types = n*[0] + m*[1]
    #gprint(types)#XXX
    #print(edgelist)#XXX
    g_igraph = igraph.Graph.Bipartite(types, edgelist, directed = False)
    print(g_igraph.summary())
    g = fromIgraph(g_igraph)

    # specific to this graph
    assert g.numNodes() == 133
    assert g.num_A_nodes == 91
    assert g.num_B_nodes == 42
    assert g.numEdges() == 281
    g.printSummary()

    # following must be true for any BipartiteGraph
    assert len(list(g.nodeIterator())) == g.numNodes()
    assert len(list(g.nodeModeIterator(MODE_A))) + len(list(g.nodeModeIterator(MODE_B))) == g.numNodes()
    assert all([g.isEdge(i, j) for i in g.nodeIterator() for j in g.neighbourIterator(i)])
    assert all([len(list(g.neighbourIterator(i))) == g.degree(i) for i in g.nodeIterator()])
    for i in g.nodeIterator():
        assert(len(list(g.neighbourIterator(i))) == len(set(g.neighbourIterator(i)))) # check no repeated neighbours in iterator
    assert g.numEdges() == len(list(g.edgeIterator()))

    # following must be true from any BipartiteGraph constructed from igraph
    assert isinstance(g, BipartiteGraph)
    num_B = sum(g_igraph.vs["type"])
    num_A = g_igraph.vcount() - num_B
    assert round(g.density(), 9) == round(g.numEdges() / (num_A * num_B), 9)

    print("OK,", time.time() - start, "s")
    print()
    


def test_attributes_digraph_stats():
    """ Test Digraph converted from igraph object with attributes, making
    sure computing statistics gets same results as for same data converted
    previously with R script.Using the high school data for this.
    """
    print("testing Digraph object converted from igraph with attributes...")
    start = time.time()
    #
    # Read edge list (two column, space delimited, no header) from compressed
    # file, convert to list of tuples, and build igraph graph object from it
    #
    datadir = os.path.join("..", "examples", "data", "directed", "HighSchoolFriendship")
    edgelist_text = gzip.open(os.path.join(datadir,"Friendship-network_data_2013.csv.gz"), mode="rt").readlines()
    edgelist_tuples = [tuple(s.split()) for s in edgelist_text]
    Gigraph = igraph.Graph.TupleList(edgelist_tuples, directed = True)


    #
    # Read the node attributes and add to igraph object
    #

    node_attrs_filename = os.path.join(datadir, 'metadata_2013.txt')

    # metadata_2013.txt
    # "-Finally the metadata file contains a tab-separated list in which each line of the form “i Ci Gi” gives class Ci and gender Gi of the person having ID i."

    # Note in the following,
    #  map(list, zip(*[row.split() for row in open(filename).readlines()]))
    # reads the data and transposes it so we have a list of columns
    # not a list of rows, which then makes it easy to convert to
    # the dict where key is column header and value is list of values
    # https://stackoverflow.com/questions/6473679/transpose-list-of-lists#

    attr_names = ['id', 'class', 'sex']
    attr_data = list(map(list, list(zip(*[row.split() for row in open(node_attrs_filename).readlines()]))))
    assert(len(attr_data) == len(attr_names))
    attr_dict = dict([(attr_names[i], attr_data[i]) for i in range(len(attr_names))])
    for v in Gigraph.vs:
        for aname in ['class', 'sex']:
            v[aname] = attr_dict[aname][attr_dict['id'].index(v['name'])]


    # Replace "Unknown" values with "NA"
    Gigraph.vs["sex"] = [sex if sex in ["F", "M"] else "NA" for sex in Gigraph.vs["sex"]]

    #
    # Convert sex to binary attribute male with True for male and False for female
    # (also for the single "Unknown")
    #

    Gigraph.vs["male"] = [True if sex == "M" else False for sex in Gigraph.vs["sex"]]

    print(Gigraph.summary())
    
    #
    # Convert to directed graph (Digraph) object for ALAAMEE
    #

    G = fromIgraph(Gigraph)
    G.printSummary()

    # following must be true for any Digraph
    assert len(list(G.nodeIterator())) == G.numNodes()
    assert all([G.isArc(i, j) for i in G.nodeIterator() for j in G.outIterator(i)])
    assert all([G.isArc(j, i) for i in G.nodeIterator() for j in G.inIterator(i)])    
    assert all([len(list(G.outIterator(i))) == G.outdegree(i) for i in G.nodeIterator()]) 
    assert all([len(list(G.inIterator(i))) == G.indegree(i) for i in G.nodeIterator()])   
    for i in G.nodeIterator():
        assert(len(list(G.outIterator(i))) == len(set(G.outIterator(i)))) # check no repeated neighbours in iterator
        assert(len(list(G.inIterator(i))) == len(set(G.inIterator(i)))) # check no repeated neighbours in iterator        

    # following must be true from any Digraph constructed from igraph
    assert isinstance(G, Digraph)
    assert round(G.density(), 9) == round(Gigraph.density(), 9)
    
    #
    # Verify the observed statistics are the same as from data converted
    # with original R sript
    #

    param_func_list =  [changeDensity, changeSender, changeReceiver, changeEgoInTwoStar, changeEgoInThreeStar, changeEgoOutTwoStar, changeEgoOutThreeStar, changeContagion, changeReciprocity, changeContagionReciprocity, changeMixedTwoStarSource, changeMixedTwoStarSink, changeTransitiveTriangleT1, changeTransitiveTriangleT3, partial(changeSenderMatch, "class"), partial(changeReceiverMatch, "class"), partial(changeReciprocityMatch, "class")]

    Zobs_orig = np.array([  54,  293,  285,  855, 1881,  993, 2583,  156,  209,   52, 1633, 1584,  785,  267,  227,  221,  171 ]) # Zobs output of runALAAMSAhighschool_gender_more.py    
    Zobs = computeObservedStatistics(G, G.binattr['male'], param_func_list)
    assert(np.all(Zobs == Zobs_orig))

    print("OK,", time.time() - start, "s")
    print()

############################### main #########################################

def main():
    """main: run all tests
    """
    test_undirected_graph()
    test_directed_graph()
    test_bipartite_graph()
    test_attributes_digraph_stats()

    
if __name__ == "__main__":
    main()

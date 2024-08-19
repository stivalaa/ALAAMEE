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

try:
    import igraph
except ImportError:
    print("Could not import igraph, skipping tests.")
    sys.exit(0)

from igraphConvert import igraphConvert
from Graph import Graph
from Digraph import Digraph
from BipartiteGraph import BipartiteGraph,MODE_A,MODE_B
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
    g = igraphConvert(g_igraph)

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
    g = igraphConvert(g_igraph)

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

    # following must be true from any Diraph constructed from igraph
    assert isinstance(g, Digraph)
    assert round(g.density(), 9) == round(g_igraph.density(), 9)

    print("OK,", time.time() - start, "s")
    print()
    


def test_bipartite_graph():

    """
    test Digraph object from igraph
    """
    print("testing Digraph object converted from igraph...")
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
    g = igraphConvert(g_igraph)

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
    

    

############################### main #########################################

def main():
    """main: run all tests
    """
    test_undirected_graph()
    test_directed_graph()
    test_bipartite_graph()


    
if __name__ == "__main__":
    main()

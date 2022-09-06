#!/usr/bin/env python3
#
# File:    tests.py
# Author:  Alex Stivala
# Created: September 2022
#
"""Unit and regression tests for ALAAMEE, particularly change statistics
   computations.
"""
import time
import random
from functools import partial
import numpy

from Graph import Graph
from Digraph import Digraph
from BipartiteGraph import BipartiteGraph,MODE_A,MODE_B
from computeObservedStatistics import computeObservedStatistics
from changeStatisticsALAAM import *
import changeStatisticsALAAMdirected
from changeStatisticsALAAMbipartite import *

####################### utililty functions ###################################

def get_random_nodelist(G, A):
    """
    Return a list of random nodes in G for usin in basic_sampler_test

    Parameters:
       G                   - Graph object for network (fixed)
       A                   - vector of 0/1 outcome variables for ALAAM

    Return value: list of nodes in A (with replacement)
    """
    NUM_TESTS = 1000
    nodelist = [None] * NUM_TESTS
    for k in range(NUM_TESTS):
        # select a node  i uniformly at random
        i = random.randint(0, G.numNodes()-1)
        while A[i] == NA_VALUE:  # keep going until we get one that is not NA
            i = random.randint(0, G.numNodes()-1)
        nodelist[k] = i
    return nodelist
    
def basic_sampler_test(G, A, changestats_func, nodelist):
    """do basic ALAAM sampler-like test on a single change stat for
    timing and regression testing for change stats functions

    Parameters:
       G                   - Graph object for network (fixed)
       A                   - vector of 0/1 outcome variables for ALAAM
       changestats_func    -  change statistics function
       nodelist            - list of nodes to change

    Note A is updated in place
    
    Return value: list of change stats values
    
    """
    deltas = [None] * len(nodelist)
    for k in range(len(nodelist)):
        # basic sampler: select a node  i uniformly at random
        # and toggle outcome variable for it
        i = nodelist[k]
        isChangeToZero = (A[i] == 1)
        if isChangeToZero:
            A[i] = 0
        changeSignMul = -1 if isChangeToZero else +1
        deltas[k] = changestats_func(G, A, i) * changeSignMul
        # always accept the change for testing
        # if changing to 0, we have already done it.
        # For changeTo1 move, set outcome to 1 now
        if not isChangeToZero:
            A[i] = 1
    return deltas

######################## test functions #####################################

def test_undirected_change_stats_karate():
    """
    test Graph object and undirected ALAAM change stats on karate club example
    """
    print("testing undirected change stats on karate club example...")
    start = time.time()
    g = Graph("../examples/data/karate_club/karate.net",
              "../examples/data/karate_club/karate_binattr.txt",
              "../examples/data/karate_club/karate_contattr.txt",
              "../examples/data/karate_club/karate_catattr.txt")
    assert g.numNodes() == 34
    assert g.numEdges() == 78
    assert round(g.density(), 7) == 0.1390374 # from R/igraph
    g.printSummary()
    outcome_binvar = list(map(int, open("../examples/data/karate_club/karate_outcome.txt").read().split()[1:]))
    obs_stats = computeObservedStatistics(g, outcome_binvar, [changeDensity, changeActivity, changeTwoStar, changeThreeStar, changeContagion, changeTriangleT1, changeTriangleT2, changeTriangleT3, changeIndirectPartnerAttribute, changePartnerAttributeActivity, changePartnerPartnerAttribute, partial(changeoOb, "senior"), partial(changeo_Ob, "senior"), partial(changeoOc, "age"), partial(changeo_Oc, "age"), partial(changeoO_Osame, "gender")])
    print(obs_stats)
    assert all(numpy.round(obs_stats, 3) == numpy.array([18, 80, 271, 955, 35, 57, 55, 18, 219, 477, 416, 12, 49, 578.407, 2537.189, 20])) # verified on IPNet 1.5  (nb IPNet 1.5 uses binattr not contattr on matching hence 20 not 40 for oO_Osame_gender)
    obs_alter2star1 = computeObservedStatistics(g, outcome_binvar,
                                                [changePartnerActivityTwoPath])
    print (obs_alter2star1)
    assert obs_alter2star1 == [566] # verified on MPNet
    print("OK,", time.time() - start, "s")
    print()


def test_directed_change_stats_highschool():
    """
    test Digraph object and directed ALAAM change stats on SocioPatterns data
    """
    print("testing directed change setats on SocioPatterns example...")
    start = time.time()
    g = Digraph("../examples/data/directed/HighSchoolFriendship/highschool_friendship_arclist.net",
                "../examples/data/directed/HighSchoolFriendship/highschool_friendship_binattr.txt",
                None, # continuous attributes
                "../examples/data/directed/HighSchoolFriendship/highschool_friendship_catattr.txt")
    assert g.numNodes() == 134
    assert g.numArcs() == 668
    assert round(g.density(), 8) == 0.03748176 # from R/igraph
    g.printSummary()
    outcome_binvar = list(map(int, open("../examples/data/directed/HighSchoolFriendship/highschool_friendship_binattr.txt").read().split()[1:])) # male
    obs_stats = computeObservedStatistics(g, outcome_binvar, [changeDensity, changeStatisticsALAAMdirected.changeSender, changeStatisticsALAAMdirected.changeReceiver, changeStatisticsALAAMdirected.changeContagion])
    print(obs_stats)
    assert all(obs_stats == [54, 293, 285, 156]) # verified on MPNet
    print("OK,", time.time() - start, "s")
    print()


def test_regression_undirected_change_stats():
    """
    test new against old version of undirected ALAAM change stats on
    simmulated 1000 node example
    """
    print("testing undirected change stats on 1000 node simulated example...")
    start = time.time()
    g = Graph("../examples/data/simulated_n1000_bin_cont/n1000_kstar_simulate12750000.txt",
              "../examples/data/simulated_n1000_bin_cont/binaryAttribute_50_50_n1000.txt",
              "../examples/data/simulated_n1000_bin_cont/continuousAttributes_n1000.txt")
    assert g.numNodes() == 1000
    assert g.numEdges() == 3001
    assert round(g.density(), 9) == 0.006008008 # from R/igraph
    outcome_binvar = list(map(int, open("../examples/data/simulated_n1000_bin_cont/sample-n1000_bin_cont3800000.txt").read().split()[1:]))

    nodelist = get_random_nodelist(g, outcome_binvar)
    outcome_binvar_orig = numpy.copy(outcome_binvar)
    oldstart = time.time()
    old_deltas = basic_sampler_test(g, outcome_binvar, changePartnerPartnerAttribute_OLD, nodelist)
    print("old version: ", time.time() - oldstart, "s")
    newstart = time.time()
    new_deltas = basic_sampler_test(g, outcome_binvar_orig, changePartnerPartnerAttribute, nodelist)
    print("new version: ", time.time() - newstart, "s")
    assert new_deltas == old_deltas

    print("OK,", time.time() - start, "s")
    print()


def test_bipartite_change_stats_tiny():
    """ test BipartiteGraph object and bipartite undirected change stats on
    tiny example (manually verified)
    """
    print("testing bipartrite change stats on tiny example...")
    start = time.time()
    g = BipartiteGraph("../examples/data/bipartite/tiny/tiny_bipartite.net")
    assert g.numNodes() == 5
    assert g.numEdges() == 5
    assert round(g.density(), 5) == 0.83333 # 5/(3*2)
    assert g.bipartite_node_mode(0) == MODE_A
    assert g.bipartite_node_mode(1) == MODE_A
    assert g.bipartite_node_mode(2) == MODE_A
    assert g.bipartite_node_mode(3) == MODE_B
    assert g.bipartite_node_mode(4) == MODE_B
    assert len(list(g.nodeModeIterator(MODE_A))) == 3
    assert len(list(g.nodeModeIterator(MODE_B))) == 2
    assert list(g.nodeModeIterator(MODE_A)) == [0, 1, 2]
    assert list(g.nodeModeIterator(MODE_B)) == [3, 4]
    g.printSummary()
    outcome_binvar = list(map(int, open("../examples/data/bipartite/tiny/tiny_outcome.txt").read().split()[1:]))
    obs_stats = computeObservedStatistics(g, outcome_binvar, [partial(changeBipartiteDensity, MODE_A), partial(changeBipartiteActivity, MODE_A), partial(changeBipartiteEgoTwoStar, MODE_A), partial(changeBipartiteAlterTwoStar1,MODE_A), partial(changeBipartiteAlterTwoStar2,MODE_A), partial(changeBipartiteFourCycle1, MODE_A),partial(changeBipartiteFourCycle2, MODE_A)])
    assert all(obs_stats == numpy.array([0, 0, 0, 0, 0, 0, 0])) #mode A all zero
    obs_stats = computeObservedStatistics(g, outcome_binvar, [partial(changeBipartiteDensity, MODE_B), partial(changeBipartiteActivity, MODE_B), partial(changeBipartiteEgoTwoStar, MODE_B), partial(changeBipartiteAlterTwoStar1,MODE_B), partial(changeBipartiteAlterTwoStar2,MODE_B), partial(changeBipartiteFourCycle1, MODE_B),partial(changeBipartiteFourCycle2, MODE_B)])
    print(obs_stats)
    assert all(obs_stats == numpy.array([1, 2, 1, 2, 0, 1, 0])) #manually verified and also used to fix MPNet (see ../examples/data/bipartite/tiny/)

    print("OK,", time.time() - start, "s")
    print()

def test_bipartite_change_stats_inouye():
    """ test BipartiteGraph object and bipartite undirected change stats on
    Inouye-Pyke pollinator web example
    """
    print("testing bipartrite change stats on Inouye-Pyke example...")
    start = time.time()
    g = BipartiteGraph("../examples/data/bipartite/Inouye_Pyke_pollinator_web/inouye_bipartite.net")
    assert g.numNodes() == 133
    assert g.numEdges() == 281
    assert len(list(g.nodeModeIterator(MODE_A))) == 91
    assert len(list(g.nodeModeIterator(MODE_B))) == 42
    g.printSummary()
    b2star2 = sum([(g.twoPaths(i, j) if i < j else 0) for i in g.nodeModeIterator(MODE_A) for j in g.nodeModeIterator(MODE_A)])
    assert b2star2 == 1437 # verified in statnet (see ../examples/data/bipartite/Inouye_Pyke_pollinator_web/testing.txt)
    b1star2 = sum([(g.twoPaths(i, j) if i < j else 0) for i in g.nodeModeIterator(MODE_B) for j in g.nodeModeIterator(MODE_B)])
    assert b1star2 == 877 # verified in statnet (see ../examples/data/bipartite/Inouye_Pyke_pollinator_web/testing.txt)
    twopaths = sum([(g.twoPaths(i, j) if i < j else 0) for i in g.nodeIterator() for j in g.nodeIterator()])    
    assert twopaths == 2314 # verified in statnet (see ../examples/data/bipartite/Inouye_Pyke_pollinator_web/testing.txt)

    outcome_binvar = list(map(int, open("../examples/data/bipartite/Inouye_Pyke_pollinator_web/inouye_outcome.txt").read().split()[1:]))
    obs_stats = computeObservedStatistics(g, outcome_binvar,
                        [partial(changeBipartiteDensity, MODE_A),
                         partial(changeBipartiteActivity, MODE_A),
                         partial(changeBipartiteEgoTwoStar, MODE_A),
                         partial(changeBipartiteAlterTwoStar1,MODE_A),
                         partial(changeBipartiteAlterTwoStar2,MODE_A),
                         partial(changeBipartiteFourCycle1, MODE_A),
                         partial(changeBipartiteFourCycle2, MODE_A)])
    print(obs_stats)
    assert all(obs_stats == numpy.array([39, 129, 347, 1258, 266, 718, 122])) # verified against corrected version of MPNet (After manually checking tiny example)

    print("OK,", time.time() - start, "s")
    print()
    
############################### main #########################################

def main():
    """main: run all tests
    """
    test_undirected_change_stats_karate()
    test_directed_change_stats_highschool()
    test_regression_undirected_change_stats()
    test_bipartite_change_stats_tiny()
    test_bipartite_change_stats_inouye()

if __name__ == "__main__":
    main()

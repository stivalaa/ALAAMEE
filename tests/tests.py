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

from Graph import Graph,int_or_na
from Digraph import Digraph
from BipartiteGraph import BipartiteGraph,MODE_A,MODE_B
from computeObservedStatistics import computeObservedStatistics
from changeStatisticsALAAM import *
import changeStatisticsALAAMdirected
from changeStatisticsALAAMbipartite import *

DEFAULT_NUM_TESTS = 10000 # number of random node samples

####################### utililty functions ###################################

def get_random_nodelist(G, A, num_tests):
    """
    Return a list of random nodes in G for usin in basic_sampler_test

    Parameters:
       G                   - Graph object for network (fixed)
       A                   - vector of 0/1 outcome variables for ALAAM
       num_tests           - number of nodes to sample

    Return value: list of nodes in A (with replacement)
    """
    nodelist = [None] * num_tests
    for k in range(num_tests):
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

def compare_changestats_implementations(g, outcome_binvar, changestats_func_1,
                                        changestats_func_2, num_tests):
    """
    compare two change statistics functions, verify they get the same
    results and show times

    Parameters:
        g                  - Graph object
        outcome_binvar     - vector of 0/1 outcome variables for ALAAM
        changestats_func_1 - old implementation of change stats function
        changestats_func_2 - new implementation of chage stats function
        num_tests          - number of nodes to randomly sample
    """ 
    nodelist = get_random_nodelist(g, outcome_binvar, num_tests)
    outcome_binvar_orig = numpy.copy(outcome_binvar)
    oldstart = time.time()
    old_deltas = basic_sampler_test(g, outcome_binvar, changestats_func_1, nodelist)
    print("old version: ", time.time() - oldstart, "s")
    newstart = time.time()
    new_deltas = basic_sampler_test(g, outcome_binvar_orig, changestats_func_2, nodelist)
    print("new version: ", time.time() - newstart, "s")
    #print(new_deltas)
    assert new_deltas == old_deltas


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
    outcome_binvar = list(map(int_or_na, open("../examples/data/karate_club/karate_outcome.txt").read().split()[1:]))
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
    print("testing directed change stats on SocioPatterns example...")
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
    print("testing undirected change stats on 1000 node simulated example")
    print("for ", DEFAULT_NUM_TESTS, "iterations...")    
    start = time.time()
    g = Graph("../examples/data/simulated_n1000_bin_cont/n1000_kstar_simulate12750000.txt",
              "../examples/data/simulated_n1000_bin_cont/binaryAttribute_50_50_n1000.txt",
              "../examples/data/simulated_n1000_bin_cont/continuousAttributes_n1000.txt")
    assert g.numNodes() == 1000
    assert g.numEdges() == 3001
    assert round(g.density(), 9) == 0.006008008 # from R/igraph
    g.printSummary()
    outcome_binvar = list(map(int_or_na, open("../examples/data/simulated_n1000_bin_cont/sample-n1000_bin_cont3800000.txt").read().split()[1:]))

    nodelist = get_random_nodelist(g, outcome_binvar, DEFAULT_NUM_TESTS)
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

    outcome_binvar = list(map(int_or_na, open("../examples/data/bipartite/Inouye_Pyke_pollinator_web/inouye_outcome.txt").read().split()[1:]))
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


def test_regression_twopaths(netfilename):
    """
    test that nonzero two-paths values in two-paths sparse matrix
    built at network construction are same as those computed by the
    twoPaths function.
    For bipartite only, since only build matrix for bipartite

    Parameters:
           netfile      - filename bipartite network in Pajek format
    """
    print("testing two-paths values for ", netfilename)
    start = time.time()
    g = BipartiteGraph(netfilename)
    g.printSummary()
    for i in g.nodeModeIterator(MODE_A):
        for j in g.nodeModeIterator(MODE_B):
            assert g.twoPathsMatrix.getValue(i, j) == g.twoPaths(i, j)

    print("OK,", time.time() - start, "s")
    print()

def test_regression_twopaths_iterators(netfilename):
    """
    test iterator fuinctions for two-paths sparse matrix.
    For bipartite only, since only build matrix for bipartite

    Parameters:
           netfile      - filename bipartite network in Pajek format
    """
    print("testing two-paths sparse matrix iterators for ", netfilename)
    start = time.time()
    g = BipartiteGraph(netfilename)
    g.printSummary()
    for i in range(g.numNodes()):
        for j in g.twoPathsMatrix.rowNonZeroColumnsIterator(i):
            assert g.twoPathsMatrix.getValue(i, j) > 0
            assert g.twoPathsMatrix.getValue(i, j) == g.twoPaths(i, j)
    for i in range(g.numNodes()):
        for (j, p) in zip(g.twoPathsMatrix.rowNonZeroColumnsIterator(i),
                          g.twoPathsMatrix.rowNonZeroValuesIterator(i)):
            assert p > 0
            assert p == g.twoPaths(i, j)
    print("OK,", time.time() - start, "s")
    print()


def test_regression_bipartite_change_stats(netfilename, outcomefilename,
                                           num_tests = DEFAULT_NUM_TESTS):
    """
    test new against old version of bipartite undirected ALAAM change stats

    Parameters:
           netfile      - filename bipartite network in Pajek format
           outcomefile  - filename of binary outcome file
           num_tests    - number of nodes to sample (number of times
                          the change statistic is computed)
    """
    print("testing bipartite change stats for ", netfilename)
    print("for ", num_tests, "iterations...")
    start = time.time()
    g = BipartiteGraph(netfilename)
    g.printSummary()
    outcome_binvar = list(map(int_or_na, open(outcomefilename).read().split()[1:]))

    print("changeBipartiteAlterTwoStar1")
    compare_changestats_implementations(g, outcome_binvar, partial(changeBipartiteAlterTwoStar1_SLOW, MODE_A), partial(changeBipartiteAlterTwoStar1, MODE_A), num_tests)

    print("changeBipartiteAlterTwoStar2")
    compare_changestats_implementations(g, outcome_binvar, partial(changeBipartiteAlterTwoStar2_SLOW, MODE_A), partial(changeBipartiteAlterTwoStar2, MODE_A), num_tests)

    print("changeBipartiteFourCycle1")
    compare_changestats_implementations(g, outcome_binvar, partial(changeBipartiteFourCycle1_OLD, MODE_A), partial(changeBipartiteFourCycle1, MODE_A), num_tests)

    print("changeBipartiteFourCycle2")
    compare_changestats_implementations(g, outcome_binvar, partial(changeBipartiteFourCycle2_OLD, MODE_A), partial(changeBipartiteFourCycle2, MODE_A), num_tests)
    
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
    test_regression_twopaths("../examples/data/bipartite/Inouye_Pyke_pollinator_web/inouye_bipartite.net")
    test_regression_twopaths_iterators("../examples/data/bipartite/Inouye_Pyke_pollinator_web/inouye_bipartite.net")
    test_regression_bipartite_change_stats("../examples/data/bipartite/Inouye_Pyke_pollinator_web/inouye_bipartite.net", "../examples/data/bipartite/Inouye_Pyke_pollinator_web/inouye_outcome.txt")
    #too slow (and data large for GitHub): test_regression_bipartite_change_stats("../examples/data/bipartite/Evtusehnko_Gastner_directors/evtushenko_directors_bipartite.net", "../examples/data/bipartite/Evtusehnko_Gastner_directors/evtushenko_directors_outcome.txt", 10)

if __name__ == "__main__":
    main()

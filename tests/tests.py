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
from math import log,exp,isclose
import math
from collections import Counter
import numpy

from Graph import Graph,int_or_na
from Digraph import Digraph
from BipartiteGraph import BipartiteGraph,MODE_A,MODE_B
from computeObservedStatistics import computeObservedStatistics
from changeStatisticsALAAM import *
import changeStatisticsALAAMdirected
from changeStatisticsALAAMbipartite import *
from gofALAAM import mahalanobis

DEFAULT_NUM_TESTS = 10000 # number of random node samples

####################### utililty functions ###################################
#
##############################################################################

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
                                        changestats_func_2, num_tests,
                                        epsilon =  None):
    """
    compare two change statistics functions, verify they get the same
    results and show times

    Parameters:
        g                  - Graph object
        outcome_binvar     - vector of 0/1 outcome variables for ALAAM
        changestats_func_1 - old implementation of change stats function
        changestats_func_2 - new implementation of chage stats function
        num_tests          - number of nodes to randomly sample
        epsilon            - epsilon for testing absolute difference in values
                             for float, or None for exact (for integers)
                             default None
    """ 
    nodelist = get_random_nodelist(g, outcome_binvar, num_tests)
    outcome_binvar1 = list.copy(outcome_binvar)
    outcome_binvar2 = list.copy(outcome_binvar)
    oldstart = time.time()
    old_deltas = basic_sampler_test(g, outcome_binvar1, changestats_func_1, nodelist)
    print("old version: ", time.time() - oldstart, "s")
    newstart = time.time()
    new_deltas = basic_sampler_test(g, outcome_binvar2, changestats_func_2, nodelist)
    print("new version: ", time.time() - newstart, "s")
    if epsilon is not None:
        #print([abs(new_deltas[i] - old_deltas[i]) for i in range(len(new_deltas))])
        assert all([math.isclose(new_deltas[i], old_deltas[i], abs_tol=epsilon)
                    for i in range(len(new_deltas))])
    else:
        assert new_deltas == old_deltas


def compare_statistic_sum_changestatistic(g, outcome_binvar, stat_func,
                                          changestats_func,
                                          epsilon = None):
    """
    Compare the dircetly computed statistic to the value computed
    by summming the correpsonding change statistic for each node with
    outcome variable = 1 (as done by the computeObservedStatistics()
    function), to verify they get the same result.

    Parameters:
        g                  - Graph object
        outcome_binvar     - vector of 0/1 outcome variables for ALAAM
        stat_func          - function that directly computes statistic value
        changestats_func   - change statistics function
        epsilon            - epsilon for testing absolute difference in values
                             for float, or None for exact (for integers)
                             default None
    """
    start = time.time()
    change_stat_sum = computeObservedStatistics(g, outcome_binvar,
                                                [changestats_func])[0]
    #print("sum changestats time:  ", time.time() - start, "s")
    start = time.time()
    stat_value =  stat_func(g, outcome_binvar)
    #print("direct statistic time: ", time.time() - start, "s")
    #print(stat_value)
    #print(change_stat_sum)
    if epsilon is not None:
        assert math.isclose(change_stat_sum, stat_value, abs_tol=epsilon)
    else:
        assert change_stat_sum == stat_value


####################  ALAAM statistics functions ############################
#
# These compute ALAAM statistics directly (rather than by summing change
# statistics) in order to verify / regression test change statistic functions
# by comparing the dircetly computed statistic to the value computed
# by summming the corresponding change statistic for each node with
# outcome variable = 1 (as done by the computeObservedStatistics() function),
# which is done by the compare_statistic_sum_changestatistic() function.
#
# These functions all have signature (G, A) where G is the Graph (or Digraph)
# and A is the outcome vector. (For those with aditional parameters, such as
# alpha on GWActivity, the additional parameters are at the start to allow
# the use of functools.partial to create a function with the (G, A) signature
# e.g.  partial(GWActivity, log(2))
#
##############################################################################

def Activity(G, A):
    """
    Activity statistic (undirected)

    *--o
    """
    return sum(G.degree(i) for i in G.nodeIterator() if A[i] == 1)


def Contagion(G, A):
    """
    Undirected Contagtion statistic (partner attribute)

    *--*
    """
    # Number of edges i -- j where both A[i] and A[j] are 1
    return sum(int(A[i] == A[j] == 1) for (i, j) in G.edgeIterator())

def Contagion_nodeiter(G, A):
    """
    Undirected Contagion statistic (partner attribute)

    *--*

    Alternative implementation iterating over nodes not edges
    """
    ## Division by two to adjust for double-counting (operator // is int. div.)
    ## Note the above implementation iterating over edges instead is therefore
    ## simpler and more elegant (and more efficient), does not double-count
    return sum(sum((A[u] == 1) for u in G.neighbourIterator(i))
                               for i in G.nodeIterator() if A[i] == 1) // 2

def GWActivity(alpha, G, A):
    """Geometrically Weighted Activity statistic

       o
      /
     *--o
      \ :
       o

    See equation (4) in:

    Stivala, A. (2023). Overcoming near-degeneracy in the autologistic
    actor attribute model. arXiv preprint arXiv:2309.07338v2.
    https://arxiv.org/abs/2309.07338v2

    """
    return sum(exp(-alpha * G.degree(i))
               for i in G.nodeIterator() if A[i] == 1)


def GWActivity_kiter(alpha, G, A):
    """Geometrically Weighted Activity statistic

       o
      /
     *--o
      \ :
       o

    This implementation iterates over node degrees rather than nodes

    See equations (3) and (4) in:

    Stivala, A. (2023). Overcoming near-degeneracy in the autologistic
    actor attribute model. arXiv preprint arXiv:2309.07338v2.
    https://arxiv.org/abs/2309.07338v2

    """
    maxdegree = max(G.degree(i) for i in G.nodeIterator())
    # build frequency counts (histogram) of degrees of nodes with
    # outcome variable 1 using Counter (multiset or bag) data type
    # from collections library which conveniently returns 0 instead of
    # KeyError key not present
    degree1_freq = Counter(G.degree(i) for i in G.nodeIterator() if A[i] == 1)
    return sum(exp(-alpha * k) * degree1_freq[k] for k in range(maxdegree+1))



def GWContagion_kiter(alpha, G, A):
    """Geometrically Weighted Contagion statistic

       *
      /
     *--*
      \ :
       *

    This implementation iterates over node degrees rather than nodes

    """
    maxdegree = max(G.degree(i) for i in G.nodeIterator())
    # build frequency counts (histogram) of number of neighbours with
    # outcmome 1 of nodes also with outcome variable 1 using Counter
    # (multiset or bag) data type from collections library which
    # conveniently returns 0 instead of KeyError key not present
    degree1_1_freq = Counter(sum((A[u] == 1) for u in G.neighbourIterator(i))
                             for i in G.nodeIterator() if A[i] == 1)
    return sum(exp(-alpha * k) * degree1_1_freq[k] for k in range(maxdegree+1))


def GWContagion(alpha, G, A):
    """Geometrically Weighted Contagion statistic

       *
      /
     *--*
      \ :
       *

    """
    return sum(exp(-alpha * sum((A[u] == 1) for u in G.neighbourIterator(i)))
               for i in G.nodeIterator() if A[i] == 1)

def directedGWContagion(alpha, G, A):
    """Directed Geometrically Weighted Contagion statistic

        >*
      /
     *-->*
      \ :
       >*

          *
        /
      <
     *<--*
      <  :
        \
         *
    """
    return ( sum(exp(-alpha * sum((A[u] == 1) for u in G.outIterator(i)))
                 for i in G.nodeIterator() if A[i] == 1) +
             sum(exp(-alpha * sum((A[u] == 1) for u in G.inIterator(i)))
                 for i in G.nodeIterator() if A[i] == 1) )



def LogContagion(G, A):
    """Logarithmic Contagion statistic

       *
      /
     *--*
      \ :
       *

    """
    ## Note adding one to degree so never have log(0)
    return sum(log(sum((A[u] == 1) for u in G.neighbourIterator(i)) + 1)
               for i in G.nodeIterator() if A[i] == 1)


def directedLogContagion(G, A):
    """Directed Log Contagion statistic

        >*
      /
     *-->*
      \ :
       >*

          *
        /
      <
     *<--*
      <  :
        \
         *
    """
    ## Note adding one to degree so never have log(0)
    return  ( sum(log(sum((A[u] == 1) for u in G.outIterator(i)) + 1)
                  for i in G.nodeIterator() if A[i] == 1) +
              sum(log(sum((A[u] == 1) for u in G.inIterator(i)) + 1)
                  for i in G.nodeIterator() if A[i] == 1) )


def PowerContagion(beta, G, A):
    """Power Contagion statistic

       *
      /
     *--*
      \ :
       *

    """
    return sum(math.pow(sum((A[u] == 1) for u in G.neighbourIterator(i)),
                        1/beta)
               for i in G.nodeIterator() if A[i] == 1)


def directedPowerContagion(beta, G, A):
    """Directed Power Contagion statistic

        >*
      /
     *-->*
      \ :
       >*

          *
        /
      <
     *<--*
      <  :
        \
         *
    """
    return  ( sum(math.pow(sum((A[u] == 1) for u in G.outIterator(i)), 1/beta)
                  for i in G.nodeIterator() if A[i] == 1) +
              sum(math.pow(sum((A[u] == 1) for u in G.inIterator(i)), 1/beta)
                  for i in G.nodeIterator() if A[i] == 1) )


######################### test functions #####################################
#
##############################################################################

def test_undirected_graph():

    """
    test Graph object
    """
    print("testing Graph object...")
    start = time.time()
    g = Graph("../examples/data/simulated_n1000_bin_cont/n1000_kstar_simulate12750000.txt",
              "../examples/data/simulated_n1000_bin_cont/binaryAttribute_50_50_n1000.txt",
              "../examples/data/simulated_n1000_bin_cont/continuousAttributes_n1000.txt")
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

    print("OK,", time.time() - start, "s")
    print()


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
    assert g.numEdges() == len(list(g.edgeIterator()))
    g.printSummary()
    outcome_binvar = list(map(int_or_na, open("../examples/data/karate_club/karate_outcome.txt").read().split()[1:]))
    obs_stats = computeObservedStatistics(g, outcome_binvar, [changeDensity, changeActivity, changeTwoStar, changeThreeStar, changeContagion, changeTriangleT1, changeTriangleT2, changeTriangleT3, changeIndirectPartnerAttribute, changePartnerAttributeActivity, changePartnerPartnerAttribute, partial(changeoOb, "senior"), partial(changeo_Ob, "senior"), partial(changeoOc, "age"), partial(changeo_Oc, "age"), partial(changeoO_Osame, "gender")])
    print(obs_stats)
    assert all(numpy.round(obs_stats, 3) == numpy.array([18, 80, 271, 955, 35, 57, 55, 18, 219, 477, 416, 12, 49, 578.407, 2537.189, 20])) # verified on IPNet 1.5  (nb IPNet 1.5 uses binattr not contattr on matching hence 20 not 40 for oO_Osame_gender)
    obs_alter2star1 = computeObservedStatistics(g, outcome_binvar,
                                                [changePartnerActivityTwoPath])
    print (obs_alter2star1)
    assert obs_alter2star1 == [566] # verified on MPNet (see examples/data/karateclub/README)
    obs_alter2star2 = computeObservedStatistics(g, outcome_binvar,
                                                [changeIndirectPartnerAttribute])
    print (obs_alter2star2)
    assert obs_alter2star2 == [219] # verified on MPNet (see examples/data/karateclub/README)
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

    # There is a single NA value for the sex categorical attribute.
    # That node has an indegree of 4 and an outdegree of 4.
    # It has a total of 8 arcs incident to it (counting each direction as
    # a separate arc, i.e. a mutual arc counts as 2) and 5 arcs ignoring
    # direction (i.e. collapsing mutual into a single arc).
    # 3 of these 5 arcs are mutual (reciprocated), and 2 are not.
    # Verified using igraph with network loaded using
    # load_highschoolfriendship_directed_network.R:
    # > V(g)[29]$sex
    # [1] "Unknown"
    # > incident(g, V(g)[29], 'all')
    # + 8/668 edges from b2f5311 (vertex names):
    # [1] 34 ->151 151->34  34 ->277 277->34  34 ->502 34 ->866 866->34  201->34
    assert g.catattr['sex'].count(NA_VALUE) == 1
    sex_na_node = g.catattr['sex'].index(NA_VALUE) # node with NA for sex
    assert g.outdegree(sex_na_node) == 4
    assert g.indegree(sex_na_node) == 4
    assert len(set(g.outIterator(sex_na_node)).union(set(g.inIterator(sex_na_node)))) == 5
    g.printSummary()
    outcome_binvar = list(map(int, open("../examples/data/directed/HighSchoolFriendship/highschool_friendship_binattr.txt").read().split()[1:])) # male
    # > V(g)[neighbors(g, V(g)[29], 'all')]$sex
    # [1] "M" "M" "F" "F" "F" "M" "M" "M"
    # > V(g)[neighbors(g, V(g)[29], 'in')]$sex
    # [1] "M" "F" "M" "M"
    # > V(g)[neighbors(g, V(g)[29], 'out')]$sex
    # [1] "M" "F" "F" "M"
    assert outcome_binvar[sex_na_node] == 0 # NA was converted to 0 for outcome binary variable for MPNet
    # categorical attribute is coded as Female=1, Male=2
    assert len([g.catattr['sex'][u] for u in g.inIterator(sex_na_node)]) == 4
    assert [g.catattr['sex'][u] for u in g.inIterator(sex_na_node)].count(1) == 1
    assert [g.catattr['sex'][u] for u in g.inIterator(sex_na_node)].count(2) == 3
    assert len([g.catattr['sex'][u] for u in g.outIterator(sex_na_node)]) == 4
    assert [g.catattr['sex'][u] for u in g.outIterator(sex_na_node)].count(1) == 2
    assert [g.catattr['sex'][u] for u in g.outIterator(sex_na_node)].count(2) == 2
    # repeat for outcome binary variable, where Female (1) converted
    # to 0, and Male (2) coverted to 1 (and the single NA value
    # converted to 0, already tested above).
    assert len([outcome_binvar[u] for u in g.inIterator(sex_na_node)]) == 4
    assert [outcome_binvar[u] for u in g.inIterator(sex_na_node)].count(0) == 1
    assert [outcome_binvar[u] for u in g.inIterator(sex_na_node)].count(1) == 3
    assert len([outcome_binvar[u] for u in g.outIterator(sex_na_node)]) == 4
    assert [outcome_binvar[u] for u in g.outIterator(sex_na_node)].count(0) == 2
    assert [outcome_binvar[u] for u in g.outIterator(sex_na_node)].count(1) == 2
    obs_stats = computeObservedStatistics(g, outcome_binvar, [changeDensity, changeStatisticsALAAMdirected.changeSender, changeStatisticsALAAMdirected.changeReceiver, changeStatisticsALAAMdirected.changeReciprocity, changeStatisticsALAAMdirected.changeContagion, changeStatisticsALAAMdirected.changeContagionReciprocity, changeStatisticsALAAMdirected.changeEgoInTwoStar, changeStatisticsALAAMdirected.changeEgoOutTwoStar, changeStatisticsALAAMdirected.changeMixedTwoStar, changeStatisticsALAAMdirected.changeMixedTwoStarSource, changeStatisticsALAAMdirected.changeMixedTwoStarSink, changeStatisticsALAAMdirected.changeTransitiveTriangleT1, changeStatisticsALAAMdirected.changeTransitiveTriangleT3, changeStatisticsALAAMdirected.changeTransitiveTriangleD1, changeStatisticsALAAMdirected.changeTransitiveTriangleU1, changeStatisticsALAAMdirected.changeCyclicTriangleC1, changeStatisticsALAAMdirected.changeCyclicTriangleC3, changeStatisticsALAAMdirected.changeAlterInTwoStar2, changeStatisticsALAAMdirected.changeAlterOutTwoStar2, partial(changeStatisticsALAAMdirected.changeSenderMatch, "class"), partial(changeStatisticsALAAMdirected.changeReceiverMatch, "class"), partial(changeStatisticsALAAMdirected.changeReciprocityMatch, "class"), partial(changeStatisticsALAAMdirected.changeSenderMismatch, "class"), partial(changeStatisticsALAAMdirected.changeReceiverMismatch, "class"), partial(changeStatisticsALAAMdirected.changeReciprocityMismatch, "class"), partial(changeStatisticsALAAMdirected.changeSenderMatch, "sex"), partial(changeStatisticsALAAMdirected.changeReceiverMatch, "sex"), partial(changeStatisticsALAAMdirected.changeReciprocityMatch, "sex"), partial(changeStatisticsALAAMdirected.changeSenderMismatch, "sex"), partial(changeStatisticsALAAMdirected.changeReceiverMismatch, "sex"), partial(changeStatisticsALAAMdirected.changeReciprocityMismatch, "sex")])
    print(obs_stats)
    assert all(obs_stats == [54, 293, 285, 209, 156, 52, 855, 993, 1713, 1633, 1584, 785, 267, 796, 775, 659, 62, 408, 435, 227, 221, 171, 66, 64, 38, 156, 156, 104, 137-3, 129-2, 105-2]) # verified on MPNet, the three mismatch for sex verified manually with NA values as MPNet cannot handle them (below verified same as MPNet where 99999, i.e. matches nothing else, used instead of NA)

    g.catattr['sex'][sex_na_node] = 99999 # to match MPNet which cannot handle NA
    obs_stats = computeObservedStatistics(g, outcome_binvar, [partial(changeStatisticsALAAMdirected.changeSenderMismatch, "sex"), partial(changeStatisticsALAAMdirected.changeReceiverMismatch, "sex"), partial(changeStatisticsALAAMdirected.changeReciprocityMismatch, "sex")])
    print(obs_stats)
    assert all(obs_stats == [137, 129, 105]) # verified on MPNet

    print("OK,", time.time() - start, "s")
    print()


def test_gwcontagion():
    """
    Test of GWContagion statistic implementation on hand-worked example
    (handwritten derivation of change statistic dated 13/10/23 scanned
    in 16/10/2023).
    """
    print("testing GWContagion...")
    start = time.time()
    # Note we only create the relevant part of the graph here, it is
    # just a line graph 0 -- 1 -- 2 -- 3
    # with all nodes but 1 having outcome A[i] = 1 (we then compute
    # GWContagion with A[1] == 0 and A[1] == 1 and the change between them)
    G = Graph(num_nodes = 4)
    assert G.numNodes() == 4
    assert G.numEdges() == 0
    G.insertEdge(0, 1)
    G.insertEdge(1, 2)
    G.insertEdge(2, 3)
    assert G.numEdges() == 3
    assert G.degree(0) == 1
    assert G.degree(1) == 2
    assert G.degree(2) == 2
    assert G.degree(3) == 1
    alpha = log(2)
    A = [1, 0, 1, 1]
    #
    # * -- o -- * -- *
    #
    assert Activity(G, A) == 1 + 0 + 2 + 1
    assert Contagion(G, A) == 1
    assert GWContagion(alpha, G, A) == exp(0) + 0 + exp(-alpha) + exp(-alpha)
    A[1] = 1
    #
    # * -- * -- * -- *
    #
    assert Activity(G, A) == 1 + 2 + 2 + 1
    assert Contagion(G, A) == 3
    assert GWContagion(alpha, G, A) == exp(-alpha) + exp(-alpha*2) + exp (-alpha*2) + exp(-alpha)
    A[1] = 0
    assert changeGWContagion(alpha, G, A, 1) == exp(-alpha*2) + (exp(-alpha*(0+1)) - exp(-alpha*0)) + (exp(-alpha*(1+1)) - exp(-alpha*1))
    print("OK,", time.time() - start, "s")
    print()


def test_regression_undirected_change_stats(netfilename, outcomefilename,
                                            binattrfilename, contattrfilename,
                                            catattrfilename = None,
                                            num_tests = DEFAULT_NUM_TESTS):
    """
    test new against old version of undirected ALAAM change stats

    Parameters:
           netfilename     - filename undirected network in Pajek format
           outcomefilename - filename of binary outcome file
           binattrfilename - filename of binary attributes
           contattrfilename- filename of continuous attributes
           catattrfilename - filename of categorical attributes
           num_tests       - number of nodes to sample (number of times
                            the change statistic is computed)
    
    """
    print("testing undirected change stats for ", netfilename)
    print("for ", num_tests, "iterations...")
    start = time.time()
    g = Graph(netfilename, binattrfilename, contattrfilename)
    g.printSummary()
    assert g.numEdges() == len(list(g.edgeIterator()))
    outcome_binvar = list(map(int_or_na, open(outcomefilename).read().split()[1:]))
    assert len(outcome_binvar) == g.numNodes()

    print("changePartnerPartnerAttribute")
    compare_changestats_implementations(g, outcome_binvar, changePartnerPartnerAttribute_OLD, changePartnerPartnerAttribute, num_tests)

    print("changeTriangleT1")
    compare_changestats_implementations(g, outcome_binvar, changeTriangleT1_OLD, changeTriangleT1, num_tests)

    print("changeContagion")
    assert Contagion(g, outcome_binvar) == Contagion_nodeiter(g, outcome_binvar)
    compare_statistic_sum_changestatistic(g, outcome_binvar, Contagion, changeContagion)
    compare_changestats_implementations(g, outcome_binvar, changeContagion_LISTCOMP, changeContagion, num_tests)
    compare_changestats_implementations(g, outcome_binvar, changeContagion_GENEXP, changeContagion, num_tests)

    print("changeActivity")
    compare_statistic_sum_changestatistic(g, outcome_binvar, Activity, changeActivity)

    print("changeGWActivity")
    for alpha in [log(2)] + [x * 0.2 for x in range(1,25)]:
        compare_statistic_sum_changestatistic(g, outcome_binvar, partial(GWActivity, alpha), partial(changeGWActivity, alpha), epsilon = 1e-08)
        compare_statistic_sum_changestatistic(g, outcome_binvar, partial(GWActivity_kiter, alpha), partial(changeGWActivity, alpha), epsilon = 1e-08)

    print("GWContagion")
    for alpha in [log(2)] + [x * 0.2 for x in range(1,25)]:
        assert math.isclose(GWContagion(alpha, g, outcome_binvar), GWContagion_kiter(alpha, g, outcome_binvar), abs_tol = 1e-08)
        compare_statistic_sum_changestatistic(g, outcome_binvar, partial(GWContagion, alpha), partial(changeGWContagion, alpha), epsilon = 1e-08)
        compare_statistic_sum_changestatistic(g, outcome_binvar, partial(GWContagion_kiter, alpha), partial(changeGWContagion, alpha), epsilon = 1e-08)
        compare_changestats_implementations(g, outcome_binvar, partial(changeGWContagion_LISTCOMP, alpha), partial(changeGWContagion, alpha), num_tests, epsilon = 1e-08)

    print("LogContagion")
    compare_statistic_sum_changestatistic(g, outcome_binvar, LogContagion, changeLogContagion, epsilon = 1e-08)

    print("PowerContagion")
    for beta in range(2,11):
        compare_statistic_sum_changestatistic(g, outcome_binvar, partial(PowerContagion, beta), partial(changePowerContagion, beta), epsilon = 1e-08)
    print("OK,", time.time() - start, "s")
    print()


def test_bipartite_change_stats_tiny():
    """ test BipartiteGraph object and bipartite undirected change stats on
    tiny example (manually verified)
    """
    print("testing bipartite change stats on tiny example...")
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
    print("testing bipartite change stats on Inouye-Pyke example...")
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
           netfilename  - filename bipartite network in Pajek format
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


def test_regression_directed_change_stats(netfilename, outcomefilename,
                                          binattrfilename, contattrfilename,
                                          catattrfilename = None,
                                          num_tests = DEFAULT_NUM_TESTS):
    """
    test new against old version of directed ALAAM change stats

    Parameters:
           netfilename     - filename directed network in Pajek format
           outcomefilename - filename of binary outcome file
           binattrfilename - filename of binary attributes
           contattrfilename- filename of continuous attributes
           catattrfilename - filename of categorical attributes
           num_tests       - number of nodes to sample (number of times
                             the change statistic is computed)
    
    """
    print("testing directed change stats for ", netfilename)
    print("for ", num_tests, "iterations...")
    start = time.time()
    g = Digraph(netfilename, binattrfilename, contattrfilename)
    g.printSummary()
    outcome_binvar = list(map(int_or_na, open(outcomefilename).read().split()[1:]))
    assert len(outcome_binvar) == g.numNodes()

    print("changeContagion")
    compare_changestats_implementations(g, outcome_binvar, changeStatisticsALAAMdirected.changeContagion_OLD, changeStatisticsALAAMdirected.changeContagion, num_tests)
    compare_changestats_implementations(g, outcome_binvar, changeStatisticsALAAMdirected.changeContagion_GENCOMP, changeStatisticsALAAMdirected.changeContagion, num_tests)

    print("changeContagionReciprocity")
    compare_changestats_implementations(g, outcome_binvar, changeStatisticsALAAMdirected.changeContagionReciprocity_OLD, changeStatisticsALAAMdirected.changeContagionReciprocity, num_tests)

    print("changeReciprocity")
    compare_changestats_implementations(g, outcome_binvar, changeStatisticsALAAMdirected.changeReciprocity_OLD, changeStatisticsALAAMdirected.changeReciprocity, num_tests)

    print("changeGWContagion")
    for alpha in [log(2)] + [x * 0.2 for x in range(1,25)]:
        compare_statistic_sum_changestatistic(g, outcome_binvar, partial(directedGWContagion, alpha), partial(changeStatisticsALAAMdirected.changeGWContagion, alpha), epsilon = 1e-08)
        compare_changestats_implementations(g, outcome_binvar, partial(changeStatisticsALAAMdirected.changeGWContagion_LISTCOMP, alpha), partial(changeStatisticsALAAMdirected.changeGWContagion, alpha), num_tests, epsilon = 1e-08)

    print("changeLogContagion")
    compare_statistic_sum_changestatistic(g, outcome_binvar, directedLogContagion, changeStatisticsALAAMdirected.changeLogContagion, epsilon = 1e-08)

    print("changePowerContagion")
    for beta in range(2,11):
        compare_statistic_sum_changestatistic(g, outcome_binvar, partial(directedPowerContagion, beta), partial(changeStatisticsALAAMdirected.changePowerContagion, beta), epsilon = 1e-08)

    print("OK,", time.time() - start, "s")
    print()


def test_changestats_comparison():
    """
    Test the function that tests if two change stats functions are
    the same (needed as we cannot just compare functions due to use
    of functools.partial for example, resulting equality operator showing
    them different when really they are not).
    """
    print("testing changestats comparison...")
    assert is_same_changestat(changeContagion, changeContagion)
    assert not is_same_changestat(changeContagion, changeLogContagion)
    assert is_same_changestat(partial(changeoOc, "age"), partial(changeoOc, "age"))
    # We need this because e.g.: assert partial(changeoOc, "age") != partial(changeoOc, "age")
    assert not is_same_changestat(partial(changeoOc, "age"), partial(changeoOc, "height"))
    assert is_same_changestat(partial(changeGWActivity, log(2.0)), partial(changeGWActivity, log(2.0)))
    assert not is_same_changestat(partial(changeGWActivity, log(2.0)), partial(changeGWActivity, 2.0))
    assert is_same_changestat(partial(changeBipartiteActivity, MODE_A), partial(changeBipartiteActivity, MODE_A))
    assert not is_same_changestat(partial(changeBipartiteActivity, MODE_A), partial(changeBipartiteActivity, MODE_B))
    assert not is_same_changestat(partial(changeBipartiteActivity, MODE_A), partial(changeBipartiteDensity, MODE_A))
    print("OK")


def test_mahalanobis():
    """
    Test the Mahalanobis distance function
    """
    print("testing Mahalanobis distance...")
    # Manually entered and checked observed statistics of SIENA example
    # data used in ../examples/simple/directed/glasgow_s50:
    # DensityA SenderAttrA ReceiverAttrA ReciprocityAttrA ContagionArcA ContagionReciprocityA EgoIn2StarA AlterIn2Star2A EgoOut2StarA AlterOut2Star2A Mixed2StarA T1TA T3TA T3CA sport_oOA alcohol_oOA
    obs_stats = numpy.array([17, 43, 40, 26, 25, 7, 57, 20, 44, 40, 88, 27, 13, 3, 28, 59])
    # get Z as matrix where rows are observations and columns are variables.
    # The first row is skipped (header) and first column is skipped (Sample_id)
    # s50_sim.txt is a saved copy of MPNet GoF simulated stats from
    # ../examples/simple/directed/glasgow_s50
    Z = numpy.loadtxt('s50_sim.txt', skiprows=1, usecols=range(1, 17))
    assert numpy.shape(Z) == (1000, 16)
    ## Verified manually with R:
    # > sqrt( mahalanobis(obs_stats, colMeans(Z), cov(Z)) ) # mahalanobis() returns squared Mahalanobis dist
    # [1] 2.874224
    # > sqrt( (obs_stats - colMeans(Z)) %*% solve(cov(Z)) %*% (obs_stats - colMeans(Z)) )
    #          [,1]
    # [1,] 2.874224
    assert math.isclose(mahalanobis(obs_stats, Z), 2.874224, abs_tol = 0.000001)
    print("OK")



def test_new_bipartite_change_stats_tiny():
    """ test new bipartite undirected change stats Alter
    match/mismatch on TwoStar1 and Twostar2 and Alter binary TwoStar1
    and TwoStar2 on tiny example (manually verified). Note that these
    just directly call the general (one-mode) implementations, but intended
    specifically for two-mode graphs.
    """
    print("testing new bipartite change stats on tiny example...")
    g = BipartiteGraph("../examples/data/bipartite/tiny/tiny_bipartite.net",
                       binattr_filename = "../examples/data/bipartite/tiny/tiny_binattr.txt",
                       catattr_filename = "../examples/data/bipartite/tiny/tiny_catattr.txt")
    g.printSummary()
    outcome_binvar = list(map(int, open("../examples/data/bipartite/tiny/tiny_outcome.txt").read().split()[1:]))
    obs_stats = computeObservedStatistics(g, outcome_binvar, [partial(changeBpAlterSameTwoStar1, MODE_A, 'catattr'), partial(changeBpAlterSameTwoStar2, MODE_A, 'catattr'), partial(changeBpAlterDiffTwoStar1, MODE_A, 'catattr'), partial(changeBpAlterDiffTwoStar2, MODE_A, 'catattr'), partial(changeBpAlterBinaryTwoStar1, MODE_A, 'binattr'), partial(changeBpAlterBinaryTwoStar1, MODE_A, 'binattr')])
    assert all(obs_stats == numpy.array([0, 0, 0, 0, 0, 0])) #mode A all zero

    obs_stats = computeObservedStatistics(g, outcome_binvar, [partial(changeBpAlterSameTwoStar1, MODE_B, 'catattr'), partial(changeBpAlterSameTwoStar2, MODE_B, 'catattr'), partial(changeBpAlterDiffTwoStar1, MODE_B, 'catattr'), partial(changeBpAlterDiffTwoStar2, MODE_B, 'catattr'), partial(changeBpAlterBinaryTwoStar1, MODE_B, 'binattr'), partial(changeBpAlterBinaryTwoStar2, MODE_B, 'binattr')])
    assert all(obs_stats == numpy.array([0, 0, 2, 0, 1, 0]))

    assert changeBpAlterSameTwoStar1(MODE_B, 'catattr', g, outcome_binvar, 3) == 0
    assert changeBpAlterSameTwoStar2(MODE_B, 'catattr', g, outcome_binvar, 3) == 0
    assert changeBpAlterDiffTwoStar1(MODE_B, 'catattr', g, outcome_binvar, 3) == 2
    assert changeBpAlterDiffTwoStar2(MODE_B, 'catattr', g, outcome_binvar, 3) == 2
    assert changeBpAlterBinaryTwoStar1(MODE_B, 'binattr', g, outcome_binvar, 3) == 1
    assert changeBpAlterBinaryTwoStar2(MODE_B, 'binattr', g, outcome_binvar, 3) == 1
    print("OK")
    print()

    
############################### main #########################################

def main():
    """main: run all tests
    """
    test_undirected_graph()
    test_undirected_change_stats_karate()
    test_directed_change_stats_highschool()
    test_gwcontagion()
    test_regression_undirected_change_stats("../examples/data/karate_club/karate.net", "../examples/data/karate_club/karate_outcome.txt", "../examples/data/karate_club/karate_binattr.txt","../examples/data/karate_club/karate_contattr.txt", "../examples/data/karate_club/karate_catattr.txt")
    test_regression_undirected_change_stats("../examples/data/simulated_n500_bin_cont2/n500_kstar_simulate12750000.txt", "../examples/data/simulated_n500_bin_cont2/sample-n500_bin_cont6700000.txt", "../examples/data/simulated_n500_bin_cont2/binaryAttribute_50_50_n500.txt", "../examples/data/simulated_n500_bin_cont2/continuousAttributes_n500.txt")
    test_regression_undirected_change_stats("../examples/data/simulated_n1000_bin_cont/n1000_kstar_simulate12750000.txt", "../examples/data/simulated_n1000_bin_cont/sample-n1000_bin_cont3800000.txt", "../examples/data/simulated_n1000_bin_cont/binaryAttribute_50_50_n1000.txt", "../examples/data/simulated_n1000_bin_cont/continuousAttributes_n1000.txt")
    test_bipartite_change_stats_tiny()
    test_bipartite_change_stats_inouye()
    test_regression_twopaths("../examples/data/bipartite/Inouye_Pyke_pollinator_web/inouye_bipartite.net")
    test_regression_twopaths_iterators("../examples/data/bipartite/Inouye_Pyke_pollinator_web/inouye_bipartite.net")
    test_regression_bipartite_change_stats("../examples/data/bipartite/Inouye_Pyke_pollinator_web/inouye_bipartite.net", "../examples/data/bipartite/Inouye_Pyke_pollinator_web/inouye_outcome.txt")
    #too slow (and data large for GitHub): test_regression_bipartite_change_stats("../examples/data/bipartite/Evtusehnko_Gastner_directors/evtushenko_directors_bipartite.net", "../examples/data/bipartite/Evtusehnko_Gastner_directors/evtushenko_directors_outcome.txt", 10)
    test_regression_directed_change_stats("../examples/data/directed/HighSchoolFriendship/highschool_friendship_arclist.net", '../examples/data/directed/HighSchoolFriendship/highschool_friendship_binattr.txt', None, None, '../examples/data/directed/HighSchoolFriendship/highschool_friendship_catattr.txt')
    test_changestats_comparison()
    test_mahalanobis()
    test_new_bipartite_change_stats_tiny()

if __name__ == "__main__":
    main()

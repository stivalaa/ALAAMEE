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
from functools import partial
import numpy

from Graph import Graph
from Digraph import Digraph
from computeObservedStatistics import computeObservedStatistics
from changeStatisticsALAAM import *
import changeStatisticsALAAMdirected

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


def main():
    """main: run all tests
    """
    test_undirected_change_stats_karate()
    test_directed_change_stats_highschool()
    

if __name__ == "__main__":
    main()

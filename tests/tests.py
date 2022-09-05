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

from Graph import Graph

from changeStatisticsALAAM import *

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
    print(time.time() - start, "s")
    g.printSummary()
    

def main():
    """main: run all tests
    """
    test_undirected_change_stats_karate()
    

if __name__ == "__main__":
    main()

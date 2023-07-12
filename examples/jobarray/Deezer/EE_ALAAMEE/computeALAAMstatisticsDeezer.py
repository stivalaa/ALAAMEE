#!/usr/bin/env python3
#
# File:    run computeALAAMstatisticsDeezer.py
# Author:  Alex Stivala
# Created: April 2023
#
"""Compute the observed statistics of specified ALAAM outcome vector
   and network and node attributes.
"""
import sys
import numpy as np         # used for matrix & vector data types and functions
from functools import partial

from computeObservedStatistics import computeObservedStatistics
from Graph import Graph,NA_VALUE,int_or_na
from BipartiteGraph import BipartiteGraph,MODE_A,MODE_B
from changeStatisticsALAAMbipartite import *
from changeStatisticsALAAM import *

def get_observed_stats_from_network_attr(edgelist_filename, param_func_list,
                                         labels,
                                         outcome_bin_filename,
                                         binattr_filename=None,
                                         contattr_filename=None,
                                         catattr_filename=None):
    """Compute observed stats for outcome on specified network with binary
    and/or continuous and categorical attributes.
    
    Parameters:
         edgelist_filename - filename of Pajek format edgelist 
         param_func_list   - list of change statistic functions corresponding
                             to statistics to compute
         labels            - list of strings corresponding to param_func_list
                             to label output (header line)
         outcome_bin_filename - filename of binary attribute (node per line)
                                of outcome variable for ALAAM
         binattr_filename - filename of binary attributes (node per line)
                            Default None, in which case no binary attr.
         contattr_filename - filename of continuous attributes (node per line)
                            Default None, in which case no continuous attr.
         catattr_filename - filename of continuous attributes (node per line)
                            Default None, in which case no categorical attr.

    Write output to stdout.

    """
    assert(len(param_func_list) == len(labels))

    G = Graph(edgelist_filename, binattr_filename, contattr_filename,
              catattr_filename)

    outcome_binvar = list(map(int_or_na, open(outcome_bin_filename).read().split()[1:]))
    assert(len(outcome_binvar) == G.numNodes())
    A = outcome_binvar

    assert( all([x in [0,1,NA_VALUE] for x in A]) )
 
    # Calculate observed statistics by summing change stats for each 1 variable
    Zobs = computeObservedStatistics(G, A, param_func_list)

    sys.stdout.write(' '.join(labels) + '\n')
    sys.stdout.write(' '.join([str(z) for z in Zobs]) + '\n')



##
## main
##

get_observed_stats_from_network_attr(
        '../data/deezer_europe.net',
        [changeDensity, changeActivity, changeTwoStar, changeThreeStar, changePartnerActivityTwoPath, changeContagion, changeIndirectPartnerAttribute, changePartnerAttributeActivity, changePartnerPartnerAttribute, changeTriangleT1, changeTriangleT2, changeTriangleT3],
        ["Density", "Activity", "Two-Star", "Three-Star", "Alter-2Star1", "Contagion", "Alter-2Star2", "Partner-Activity", "Partner-Resource", "T1", "T2", "T3"],
        '../data/deezer_europe_target.txt'  # use gender as outcome variable
)

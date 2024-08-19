#!/usr/bin/env python3
#
# File:    run computeALAAMstatisticsSimpleDemo.py
# Author:  Alex Stivala
# Created: June 2020
#
"""Compute the observed statistics of specified ALAAM outcome vector
   and network and node attributes.
"""
import sys
import numpy as np         # used for matrix & vector data types and functions
from functools import partial

from computeObservedStatistics import computeObservedStatistics
from Graph import Graph,NA_VALUE,int_or_na
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

## 500 node example:
get_observed_stats_from_network_attr(
    '../data/simulated_n500_bin_cont2/n500_kstar_simulate12750000.txt',
    [changeDensity, changeActivity, changeContagion, partial(changeoOb, "binaryAttribute"), partial(changeoOc, "continuousAttribute")] + [changeTwoStar, changeThreeStar, changePartnerActivityTwoPath,
             changeTriangleT1, changeContagion,
             changeIndirectPartnerAttribute,
             changePartnerAttributeActivity, 
             changePartnerPartnerAttribute,
             changeTriangleT2,
             changeTriangleT3],
    ["Density", "Activity", "Contagion", "Binary", "Continuous"] + ['Two-Star', 'Three-Star', 'Alter-2Star1A', 'T1', 'Contagion', 'Alter-2Star2A', 'Partner-Activity', 'Partner-Resource','T2', 'T3'],
    '../data/simulated_n500_bin_cont2/sample-n500_bin_cont6700000.txt',
    '../data/simulated_n500_bin_cont2/binaryAttribute_50_50_n500.txt',
    '../data/simulated_n500_bin_cont2/continuousAttributes_n500.txt'
)

### 1000 node example:
# get_observed_stats_from_network_attr(
#    '../data/simulated_n1000_bin_cont/n1000_kstar_simulate12750000.txt',    
#     [changeDensity, changeActivity, changeContagion, partial(changeoOb, "binaryAttribute"), partial(changeoOc, "continuousAttribute")],
#     ["Density", "Activity", "Contagion", "Binary", "Continuous"],
#     '../data/simulated_n1000_bin_cont/sample-n1000_bin_cont3800000.txt',
#     '../data/simulated_n1000_bin_cont/binaryAttribute_50_50_n1000.txt',
#     '../data/simulated_n1000_bin_cont/continuousAttributes_n1000.txt'
# )

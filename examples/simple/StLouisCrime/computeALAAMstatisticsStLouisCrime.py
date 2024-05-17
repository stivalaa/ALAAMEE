#!/usr/bin/env python3
#
# File:    run computeALAAMstatisticsStLouisCrime.py
# Author:  Alex Stivala
# Created: September 2022
#
"""Compute the observed statistics of specified ALAAM outcome vector
   and network and node attributes.
"""
import sys
import numpy as np         # used for matrix & vector data types and functions
from functools import partial

from computeObservedStatistics import get_observed_stats_from_network_attr
from Graph import Graph,NA_VALUE,int_or_na
from BipartiteGraph import BipartiteGraph,MODE_A,MODE_B
from changeStatisticsALAAMbipartite import *
from changeStatisticsALAAM import *

from model import param_func_list


##
## main
##

## Add extra statistics not in model for goodness-of-fit
statfuncs = [partial(changeBipartiteActivity, MODE_A),
             partial(changeBipartiteEgoTwoStar, MODE_A),
             partial(changeBipartiteEgoThreeStar, MODE_A),
             partial(changeBipartiteAlterTwoStar1,MODE_A),
             partial(changeBipartiteAlterTwoStar2,MODE_A),
             partial(changeBipartiteFourCycle1, MODE_A),
             partial(changeBipartiteFourCycle2, MODE_A)]
             

param_func_list += [f for f in statfuncs if not any(is_same_changestat(f, g) for g in param_func_list)]



get_observed_stats_from_network_attr(
    'crime_bipartite.net',
    param_func_list,
    [param_func_to_label(f) for f in param_func_list],
    'crime_outcome.txt',
    'crime_binattr.txt',
    'crime_contattr.txt',
    'crime_catattr.txt',
    bipartite = True
)

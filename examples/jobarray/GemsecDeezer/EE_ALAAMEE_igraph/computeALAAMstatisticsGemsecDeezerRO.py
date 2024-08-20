#!/usr/bin/env python3
#
# File:    run computeALAAMstatisticsGemsecDezerRO.py
# Author:  Alex Stivala
# Created: August 2024
#
"""Compute the observed statistics of specified ALAAM outcome vector
   and network and node attributes.

   This version uses the data in an igraph object rather than 
   reading the network and data inside ALAAMEE functions.
"""
import sys
import numpy as np         # used for matrix & vector data types and functions
import igraph
from functools import partial

from computeObservedStatistics import get_observed_stats
from changeStatisticsALAAM import *

from model import param_func_list
from readData import read_ro_data

## Add extra statistics not in model for goodness-of-fit
statfuncs = [changeDensity, changeActivity, changeTwoStar, changeThreeStar, changePartnerActivityTwoPath, changeContagion, changeIndirectPartnerAttribute, changePartnerAttributeActivity, changePartnerPartnerAttribute, changeTriangleT1, changeTriangleT2, changeTriangleT3]

param_func_list += [f for f in statfuncs if not any(is_same_changestat(f, g) for g in param_func_list)]

##
## main
##

g = read_ro_data()
get_observed_stats(g, g.binattr['outcome'],
        param_func_list,
        [param_func_to_label(f) for f in param_func_list],
        degreestats = True
)

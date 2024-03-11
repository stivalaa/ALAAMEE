#!/usr/bin/env python3
#
# File:    run computeALAAMstatisticsGemsecDezerRO.py
# Author:  Alex Stivala
# Created: April 2023
#
"""Compute the observed statistics of specified ALAAM outcome vector
   and network and node attributes.
"""
import sys
import numpy as np         # used for matrix & vector data types and functions
from functools import partial

from computeObservedStatistics import get_observed_stats_from_network_attr
from changeStatisticsALAAM import *

from model import param_func_list

## Add extra statistics not in model for goodness-of-fit
statfuncs = [changeDensity, changeActivity, changeTwoStar, changeThreeStar, changePartnerActivityTwoPath, changeContagion, changeIndirectPartnerAttribute, changePartnerAttributeActivity, changePartnerPartnerAttribute, changeTriangleT1, changeTriangleT2, changeTriangleT3]

param_func_list += [f for f in statfuncs if not any(is_same_changestat(f, g) for g in param_func_list)]

##
## main
##

get_observed_stats_from_network_attr(
        '../data/deezer_ro_friendship.net',
        param_func_list,
        [param_func_to_label(f) for f in param_func_list],
        '../data/deezer_ro_outcome_alternative.txt',
        contattr_filename = '../data/deezer_ro_contattr.txt',
        degreestats = True
)

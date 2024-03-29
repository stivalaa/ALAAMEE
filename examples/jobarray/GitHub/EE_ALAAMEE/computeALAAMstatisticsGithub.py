#!/usr/bin/env python3
#
# File:    run computeALAAMstatisticsGithub.py
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

param_func_list += [f for f in statfuncs if f not in param_func_list]

##
## main
##

get_observed_stats_from_network_attr(
        '../data/musae_git.net',
        param_func_list,
        [param_func_to_label(f) for f in param_func_list],
        '../data/musae_git_target.txt' , # use target developer type as outcome variable
        degreestats = True
)

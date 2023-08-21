#!/usr/bin/env python3
#
# File:    run computeALAAMstatisticsHiggs.py
# Author:  Alex Stivala
# Created: August 2023
#
"""Compute the observed statistics of specified ALAAM outcome vector
   and network and node attributes.
"""
import sys
import numpy as np         # used for matrix & vector data types and functions
from functools import partial

from computeObservedStatistics import get_observed_stats_from_network_attr
from changeStatisticsALAAM import *
from changeStatisticsALAAMdirected import *

from model import param_func_list



##
## main
##

## Add extra statistics not in model for goodness-of-fit
statfuncs =  [changeSender, changeReceiver, changeReciprocity, changeEgoInTwoStar, changeEgoOutTwoStar, changeMixedTwoStar,  changeContagionReciprocity]  
param_func_list += [f for f in statfuncs if f not in param_func_list]

get_observed_stats_from_network_attr(
        '../data/higgs_social.net',
        param_func_list,
        [param_func_to_label(f) for f in param_func_list],
        '../data/higgs_reply_active.txt',
        directed = True
)

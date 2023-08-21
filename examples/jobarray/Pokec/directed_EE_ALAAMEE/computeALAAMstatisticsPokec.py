#!/usr/bin/env python3
#
# File:    run computeALAAMstatisticsPokec.py
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
statfuncs =  [changeReciprocity, changeEgoInTwoStar, changeEgoOutTwoStar, changeMixedTwoStar, changeContagionReciprocity, partial(changeSenderMatch, "region"), partial(changeReceiverMatch, "region"), partial(changeReciprocityMatch, "region"), changeSender, changeReceiver]
param_func_list += [f for f in statfuncs if f not in param_func_list]

get_observed_stats_from_network_attr(
        '../data/soc-pokec-relationships-directed.net',
        param_func_list,
        [param_func_to_label(f) for f in param_func_list],
        '../data/soc-pokec-binattr.txt',  # use male as outcome variable
        None, #'../data/soc-pokec-binattr.txt',
        '../data/soc-pokec-contattr.txt',
        '../data/soc-pokec-catattr.txt',
        directed = True
)

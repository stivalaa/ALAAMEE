#!/usr/bin/env python3
#
# File:    run computeALAAMstatisticsHiggsOutcomeReply.py
# Author:  Alex Stivala
# Created: April 2023
#
"""Compute the observed statistics of specified ALAAM outcome vector
   and network and node attributes.
"""
import sys
from math import log
import numpy as np         # used for matrix & vector data types and functions
from functools import partial

from computeObservedStatistics import get_observed_stats_from_network_attr
from changeStatisticsALAAM import *
from changeStatisticsALAAMdirected import *




##
## main
##

param_func_list  =  [changeDensity, changeSender, changeReceiver, changeContagion, changeReciprocity, changeEgoInTwoStar, changeEgoOutTwoStar, changeMixedTwoStar,  changeContagionReciprocity, changeAlterOutTwoStar2, changeTransitiveTriangleT1, changeTransitiveTriangleT3,  partial(changeGWSender, log(2.0)),  partial(changeGWReceiver, log(2.0)), partial(changeGWContagion, log(2.0)), changeLogContagion]

get_observed_stats_from_network_attr(
        '../../../higgsTwitterSimulations/data/higgs_social.net',
        param_func_list,
        [param_func_to_label(f) for f in param_func_list],
        '../../../higgsTwitterSimulations/data/higgs_reply_active.txt',
        directed = True
)

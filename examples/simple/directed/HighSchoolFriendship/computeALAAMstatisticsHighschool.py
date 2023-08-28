#!/usr/bin/env python3
#
# File:    run computeALAAMstatisticsHighschool.py
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
from changeStatisticsALAAM import changeDensity,param_func_to_label
from changeStatisticsALAAMdirected import *


param_func_list =  [changeDensity, partial(changeGWSender, log(2.0)), partial(changeGWReceiver, log(2.0)), changeContagion]

## Add extra statistics not in model for goodness-of-fit
statfuncs = [changeSender, changeReceiver, changeReciprocity,
             changeEgoInTwoStar, changeEgoOutTwoStar,
             changeMixedTwoStar, changeMixedTwoStarSource,
             changeMixedTwoStarSink, changeContagion,
             changeContagionReciprocity,
             changeTransitiveTriangleT1,
             changeTransitiveTriangleT3,
             changeTransitiveTriangleD1,
             changeTransitiveTriangleU1,
             changeCyclicTriangleC1,
             changeCyclicTriangleC3,
             changeAlterInTwoStar2,
             changeAlterOutTwoStar2]
   

param_func_list += [f for f in statfuncs if f not in param_func_list]

##
## main
##

get_observed_stats_from_network_attr(
    '../../../data/directed/HighSchoolFriendship/highschool_friendship_arclist.net',
    param_func_list,
    [param_func_to_label(f) for f in param_func_list],
    outcome_bin_filename = '../../../data/directed/HighSchoolFriendship/highschool_friendship_binattr.txt', # 1 means male    
    catattr_filename = '../../../data/directed/HighSchoolFriendship/highschool_friendship_catattr.txt',
    directed = True
)

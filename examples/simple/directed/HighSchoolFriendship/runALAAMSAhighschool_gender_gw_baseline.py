#!/usr/bin/env python3
#
# File:    runALAAMSAhighschool_gender_gw.py
# Author:  Alex Stivala
# Created: August 2023
#
"""Run the python implementation of the Stochastic
 Approximation algorithm for estimation of Autologistic Actor Attribute
 Model (ALAAM) parameters on the SocioPatterns high school frienship network
 with gender as "outcome" variable.

 See ../../../data/directed/HighSchoolFriendship/README.txt 
 for more details.
"""
from functools import partial
from math import log
import estimateALAAMSA
from changeStatisticsALAAMdirected import *
from changeStatisticsALAAM import changeDensity, param_func_to_label, is_same

from gof_stats import gof_funcs

param_func_list =  [changeDensity, partial(changeGWSender, log(2.0))]

estimateALAAMSA.run_on_network_attr(
        '../../../data/directed/HighSchoolFriendship/highschool_friendship_arclist.net',
        param_func_list,
        [param_func_to_label(f) for f in param_func_list],
        outcome_bin_filename = '../../../data/directed/HighSchoolFriendship/highschool_friendship_binattr.txt', # 1 means male
        catattr_filename = '../../../data/directed/HighSchoolFriendship/highschool_friendship_catattr.txt',
        directed = True,
        gof_param_func_list = param_func_list + [f for f in gof_funcs if not any(is_same(f, g) for g in param_func_list)] #TODO do this in run_on_network_attr instead
    )

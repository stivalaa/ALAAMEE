#!/usr/bin/env python3
#
# File:    runALAAMSAhighschool_class_gw_more.py
# Author:  Alex Stivala
# Created: August 2023
#
"""Run the python implementation of the Stochastic
 Approximation algorithm for estimation of Autologistic Actor Attribute
 Model (ALAAM) parameters on the SocioPatterns high school frienship network
 with class as "outcome" variable.

 See ../../../data/directed/HighSchoolFriendship/README.txt 
 for more details.
"""
from math import log
from functools import partial
import estimateALAAMSA
from changeStatisticsALAAMdirected import *
from changeStatisticsALAAM import changeDensity, param_func_to_label

param_func_list =  [changeDensity, partial(changeGWSender, log(2.0)), partial(changeGWReceiver, log(2.0)), changeContagion,changeReciprocity, changeContagionReciprocity, changeMixedTwoStarSource, changeMixedTwoStarSink, changeTransitiveTriangleT1, changeTransitiveTriangleT3, partial(changeSenderMatch, "sex"), partial(changeReceiverMatch, "sex"), partial(changeReciprocityMatch, "sex")]

estimateALAAMSA.run_on_network_attr(
        '../../../data/directed/HighSchoolFriendship/highschool_friendship_arclist.net',
        param_func_list,
        [param_func_to_label(f) for f in param_func_list],
        outcome_bin_filename = '../../../data/directed/HighSchoolFriendship/highschool_friendship_class2BIO3.txt', # 1 means class 2BIO3
        binattr_filename = '../../../data/directed/HighSchoolFriendship/highschool_friendship_binattr.txt',
        catattr_filename = '../../../data/directed/HighSchoolFriendship/highschool_friendship_catattr.txt',
        directed = True
    )

#!/usr/bin/env python3
#
# File:    runALAAMSASimpleDemoDirected.py
# Author:  Alex Stivala
# Created: February 2022
#
"""Run the python implementation of the Stochastic
 Approximation algorithm for estimation of Autologistic Actor Attribute
 Model (ALAAM) parameters on a directed network.
"""
import  estimateALAAMSA
from changeStatisticsALAAMdirected import *
from changeStatisticsALAAM import changeDensity

estimateALAAMSA.run_on_network_attr(
        '../../data/directed/HighSchoolFriendship/highschool_friendship_arclist.net',
        [changeDensity, changeSender, changeReceiver, changeContagion],
        ["Density", "Sender", "Receiver", "Contagion"],
        outcome_bin_filename = '../../data/directed/HighSchoolFriendship/highschool_friendship_binattr.txt',
        catattr_filename = '../../data/directed/HighSchoolFriendship/highschool_friendship_catattr.txt',
        directed = True
    )

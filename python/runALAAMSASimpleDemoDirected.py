#!/usr/bin/env python3
#
# File:    run ALAAMSASimpleDemoDirected.py
# Author:  Alex Stivala
# Created: February 2022
#
"""Run the simple demonstration implementation of the Stochastic
 Approximation algorithm for estimation of Autologistic Actor Attribute
 Model (ALAAM) parameters on a directed network.
"""
import  ALAAMSASimpleDemo
from changeStatisticsALAAMdirected import *
from changeStatisticsALAAM import changeDensity

ALAAMSASimpleDemo. run_on_network_attr(
        '../../data/directed/HighSchoolFriendship/highschool_friendship_arclist.net',
        [changeDensity, changeSender, changeReceiver, changeContagion],
        ["Density", "Sender", "Receiver", "Contagion"],
        outcome_bin_filename = '../../data/directed/HighSchoolFriendship/highschool_friendship_binattr.txt',
        directed = True
    )

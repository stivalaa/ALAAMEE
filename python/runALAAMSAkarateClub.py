#!/usr/bin/env python
#
# File:    run ALAAMSAkarateClub.py
# Author:  Alex Stivala
# Created: Februrary 2020
#
"""Run the simple demonstration implementation of the Stochastic
 Approximation algorithm for estimation of Autologistic Actor Attribute
 Model (ALAAM) parameters on the Zachary Karate Club example.
"""


import  ALAAMSASimpleDemo
from changeStatisticsALAAM import *

ALAAMSASimpleDemo.run_on_network_attr(
    '../data/karate_club/karate.net',
    [changeDensity, changeActivity, changeContagion],
    ["Density", "Activity", "Contagion"],
    '../data/karate_club/karate_outcome.txt',
    '../data/karate_club/karate_binattr.txt',
    '../data/karate_club/karate_contattr.txt'
    )




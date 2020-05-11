#!/usr/bin/env python
#
# File:    run ALAAMEEkarateClub.py
# Author:  Alex Stivala
# Created: Februrary 2020
#
"""Run the simple demonstration implementation of the Equilibrium
 Expectation algorithm for estimation of Autologistic Actor Attribute
 Model (ALAAM) parameters on the Zachary Karate Club example.
"""


import  ALAAMEESimpleDemo
from changeStatisticsALAAM import *

ALAAMEESimpleDemo.run_on_network_attr(
    '../data/karate_club/karate.net',
    [changeDensity, changeActivity, changeContagion],
    ["Density", "Activity", "Contagion"],
    '../data/karate_club/karate_outcome.txt',
    '../data/karate_club/karate_binattr.txt',
    '../data/karate_club/karate_contattr.txt',
    EEiterations = 100000
    )




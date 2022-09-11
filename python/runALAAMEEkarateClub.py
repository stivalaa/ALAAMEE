#!/usr/bin/env python3
#
# File:    runALAAMEEkarateClub.py
# Author:  Alex Stivala
# Created: Februrary 2020
#
"""Run the python implementation of the Equilibrium
 Expectation algorithm for estimation of Autologistic Actor Attribute
 Model (ALAAM) parameters on the Zachary Karate Club example.
"""


import  estimateALAAMEE
from changeStatisticsALAAM import *

estimateALAAMEE.run_on_network_attr(
    '../data/karate_club/karate.net',
    [changeDensity, changeActivity, changeContagion],
    ["Density", "Activity", "Contagion"],
    '../data/karate_club/karate_outcome.txt',
    '../data/karate_club/karate_binattr.txt',
    '../data/karate_club/karate_contattr.txt',
    '../data/karate_club/karate_catattr.txt',
    EEiterations = 100000
    )




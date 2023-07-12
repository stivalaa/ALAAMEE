#!/usr/bin/env python3
#
# File:    run ALAAMSAdeezer.py
# Author:  Alex Stivala
# Created: May 2023
#
"""Run the python implementation of the Stochastic
 Approximation algorithm for estimation of Autologistic Actor Attribute
 Model (ALAAM) parameters on the Deezer Europe network
"""
from functools import partial

import  estimateALAAMSA
from changeStatisticsALAAM import *

estimateALAAMSA.run_on_network_attr(
    '../data/deezer_europe.net',
    [changeDensity, changeActivity, changeContagion, changeTriangleT1],
    ["Density", "Activity", "Contagion", "T1"],
    '../data/deezer_europe_target.txt' # use gender as outcome variable
    )




#!/usr/bin/env python3
#
# File:    run runALAAMsimulateGoFDeezer.py
# Author:  Alex Stivala
# Created: April 2023
#
"""Simulate from  Autologistic Actor Attribute Model (ALAAM).
"""
import sys
from functools import partial
import numpy as np

from changeStatisticsALAAM import *
from changeStatisticsALAAMbipartite import *
from BipartiteGraph import MODE_A,MODE_B
from basicALAAMsampler import basicALAAMsampler
from simulateALAAM import simulateALAAM
from simulateALAAMsimpleDemo import simulate_from_network_attr
from Graph import int_or_na

    

# parameters and corresponding labels 
# TODO parse from estimation output

param_func_list  = [changeDensity, changeActivity, changeContagion, changeTriangleT1, changeTwoStar, changeThreeStar, changePartnerActivityTwoPath, changeIndirectPartnerAttribute, changePartnerAttributeActivity, changePartnerPartnerAttribute, changeTriangleT2, changeTriangleT3]
labels           = ["Density",     "Activity",     "Contagion",     "T1",             "Two-Star",    "Three-Star",    "Alter-2Star1",               "Alter-2Star2",                 "Partner-Activity",             "Partner-Resource",            "T2",             "T3"]
     

# Estimation results from estimation.txt
##
#Pooled
#Density -0.1955887 0.01882442 0.03717472 0.003601472 * 
#Activity -0.05343727 0.003266467 0.01382956 0.02007964 * 
#Contagion 0.1140487 0.006944979 0.02863196 0.01230757 * 
#T1 -0.001004573 0.001309763 0.002806518 0.02791803  
#TotalRuns 100 
#ConvergedRuns 100 
# TODO parse these from estimation output

theta = np.array([-0.1955887, -0.05343727, 0.1140487, -0.001004573, 0, 0, 0, 0, 0, 0, 0, 0])

assert len(param_func_list) == len(labels)
assert len(theta) == len(param_func_list)

gof_param_func_list = param_func_list
goflabels = labels
gof_theta = theta

n = len(gof_param_func_list)
assert len(goflabels) == n

simulate_from_network_attr(
    '../data/deezer_europe.net',
    gof_param_func_list,
    goflabels, 
    gof_theta,
    sampler_func = basicALAAMsampler,
    iterationInStep = 100000,
    burnIn = 1000000
    )




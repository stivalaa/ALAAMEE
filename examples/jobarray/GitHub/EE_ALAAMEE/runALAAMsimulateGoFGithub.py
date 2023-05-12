#!/usr/bin/env python3
#
# File:    run runALAAMsimulateGoFGithub.py
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
param_func_list =        [changeDensity, changeActivity, changeContagion]
labels =                 ["Density",     "Activity",     "Contagion"]

     

# Estimation results from estimation.txt
##
#Pooled
#Density -0.531597 0.04397413 0.2648604 -0.008196847 * 
#Activity -0.1653597 0.01002643 0.06078387 -0.02436076 * 
#Contagion 0.4649383 0.02807401 0.1767471 -0.086256 * 
#TotalRuns 1 
#ConvergedRuns 1 
# TODO parse these from estimation output

theta = np.array([-0.531597, -0.1653597, 0.4649383])

assert len(param_func_list) == len(labels)
assert len(theta) == len(param_func_list)

gof_param_func_list = param_func_list
goflabels = labels
gof_theta = theta

n = len(gof_param_func_list)
assert len(goflabels) == n

simulate_from_network_attr(
    '../data/musae_git.net',
    gof_param_func_list,
    goflabels, 
    gof_theta,
    sampler_func = basicALAAMsampler,
    iterationInStep = 100000,
    burnIn = 1000000
    )




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
#Density -0.5321122 0.01338513 0.3305217 -0.002374985  
#Activity -0.1635088 0.002972134 0.05140955 -0.008738786 * 
#Contagion 0.4567552 0.008892461 0.1299677 -0.02582267 * 
#TotalRuns 2 
#ConvergedRuns 2 
## TODO parse these from estimation output

theta = np.array([-0.5321122, -0.1635088, 0.4567552])

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




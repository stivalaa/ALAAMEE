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
#Density -0.53586 0.043821 0.2762325 0.09203356  
#Activity -0.1653545 0.009248309 0.06732604 0.06141516 * 
#Contagion 0.4641499 0.02752406 0.1606117 -0.001245204 * 
#TotalRuns 1 
#ConvergedRuns 1 
# TODO parse these from estimation output

theta = np.array([-0.53586, -0.1653545, 0.4641499])

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




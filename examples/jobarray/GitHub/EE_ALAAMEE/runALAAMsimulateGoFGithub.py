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
param_func_list =        [changeDensity, changeContagion]
labels =                 ["Density",     "Contagion"]

     

# Estimation results from estimation.txt
##
#Pooled
#Density -1.059162 0.05737307 0.2255518 0.03083322 * 
#Contagion -0.0002923242 0.001657929 0.01037891 -0.01372051  
#TotalRuns 1 
#ConvergedRuns 1 
# TODO parse these from estimation output

theta = np.array([-1.059162, -0.0002923242])

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




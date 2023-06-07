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
#Density -0.5365325 0.04596909 0.08739228 0.03865613 * 
#Activity -0.1652275 0.009578548 0.01737109 0.0168499 * 
#Contagion 0.4641411 0.0281529 0.04280775 -0.04349935 * 
#TotalRuns 10 
#ConvergedRuns 10 
# TODO parse these from estimation output

theta = np.array([-0.5365325, -0.1652275, 0.4641411])

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




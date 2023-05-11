#!/usr/bin/env python3
#
# File:    run runALAAMsimulateGoFPokec.py
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
#Pooled
#Density -0.1550667 0.05452227 0.008926721 0.02489506 * 
#Contagion -0.007727162 0.004478487 0.0008638177 0.01694675 * 
#age_oOc 0.009514543 0.002756846 0.0004219472 -0.006381448 * 
#TotalRuns 100 
#ConvergedRuns 100 
# TODO parse from estimation output
param_func_list  =     [changeDensity, changeContagion, partial(changeoOc, "age")]
labels =        ["Density", "Contagion",  "age_oOc"]

# Estimation results from estimation.txt
theta = np.array([-0.1550667, -0.007727162, 0.009514543])

assert len(param_func_list) == len(labels)
assert len(theta) == len(param_func_list)

gof_param_func_list = param_func_list
goflabels = labels
gof_theta = theta

n = len(gof_param_func_list)
assert len(goflabels) == n

simulate_from_network_attr(
    '../data/soc-pokec-relationships-undirected.net',
    gof_param_func_list,
    goflabels, 
    gof_theta,
    None, #'../data/soc-pokec-binattr.txt',
    '../data/soc-pokec-contattr.txt',
    '../data/soc-pokec-catattr.txt',
     sampler_func = basicALAAMsampler,
     iterationInStep = 1000000,
     burnIn = 10000000
    )




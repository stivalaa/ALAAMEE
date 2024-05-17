#!/usr/bin/env python3
#
# File:    run runALAAMsimualteGoFStLouisCrime.py
# Author:  Alex Stivala
# Created: September 2022
#
"""Simuilate bipartite Autologistic Actor Attribute Model (ALAAM).
"""
import sys
from functools import partial
import random
import numpy as np

from changeStatisticsALAAM import *
from changeStatisticsALAAMbipartite import *
from BipartiteGraph import MODE_A,MODE_B
from bipartiteALAAMsampler import bipartiteALAAMsampler
from simulateALAAM import simulate_from_network_attr
from parseEstimationEEOutput import parseEstimationEEOutput
from utils import int_or_na

from model import param_func_list


###
### main
###


labels =  [param_func_to_label(f) for f in param_func_list]

# Estimation results from output of computeALAMEEcovariance.R
(paramnames, estimates) = parseEstimationEEOutput('estimation_StLouisCrime_bipartite.txt')

assert paramnames == labels

theta = np.array(estimates)

## Add extra statistics not in model for goodness-of-fit
statfuncs = [partial(changeBipartiteActivity, MODE_A),
             partial(changeBipartiteEgoTwoStar, MODE_A),
             partial(changeBipartiteEgoThreeStar, MODE_A),
             partial(changeBipartiteAlterTwoStar1,MODE_A),
             partial(changeBipartiteAlterTwoStar2,MODE_A),
             partial(changeBipartiteFourCycle1, MODE_A),
             partial(changeBipartiteFourCycle2, MODE_A)]

param_func_list += [f for f in statfuncs if not any(is_same_changestat(f, g) for g in param_func_list)]
labels =  [param_func_to_label(f) for f in param_func_list]

# pad theta vector with zeros for the parameters not in the model
theta = np.array(list(theta) + (len(param_func_list)-len(theta))*[0])


assert len(param_func_list) == len(labels)
assert len(theta) == len(param_func_list)


simulate_from_network_attr(
    'crime_bipartite.net',
    param_func_list, labels, theta,
    'crime_binattr.txt',
    'crime_contattr.txt',
    'crime_catattr.txt',
     sampler_func = partial(bipartiteALAAMsampler, MODE_A),
     iterationInStep = 1000000,
     burnIn = 1000000,
     bipartite = True,
     bipartiteFixedMode = MODE_B
    )




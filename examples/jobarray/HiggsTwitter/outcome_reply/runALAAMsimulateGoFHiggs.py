#!/usr/bin/env python3
#
# File:    run runALAAMsimulateGoFHiggs.py
# Author:  Alex Stivala
# Created: August 2023
#
"""Simulate from  Autologistic Actor Attribute Model (ALAAM).
"""
import sys
from functools import partial
import numpy as np

from changeStatisticsALAAM import *
from changeStatisticsALAAMdirected import *
from basicALAAMsampler import basicALAAMsampler
from simulateALAAM import simulate_from_network_attr
from parseEstimationEEOutput import parseEstimationEEOutput

from model import param_func_list


###
### main
###

labels =  [param_func_to_label(f) for f in param_func_list]

# Estimation results from output of computeALAMEEcovariance.R
(paramnames, estimates) = parseEstimationEEOutput('estimation.txt')

assert paramnames == labels

theta = np.array(estimates)

## Add extra statistics not in model for goodness-of-fit
statfuncs =  [changeSender, changeReceiver, changeReciprocity, changeEgoInTwoStar, changeEgoOutTwoStar, changeMixedTwoStar, changeContagion,  changeContagionReciprocity]  
param_func_list += [f for f in statfuncs if f not in param_func_list]
labels =  [param_func_to_label(f) for f in param_func_list]

# pad theta vector with zeros for the parameters not in the model
theta = np.array(list(theta) + (len(param_func_list)-len(theta))*[0])


assert len(param_func_list) == len(labels)
assert len(theta) == len(param_func_list)



simulate_from_network_attr(
    '../data/higgs_social.net',
    param_func_list, labels, theta,
    sampler_func = basicALAAMsampler,
    iterationInStep = 1000000,
    burnIn = 10000000,
    directed = True
    )




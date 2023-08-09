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
statfuncs = [changeActivity, changeTwoStar, changeThreeStar]
param_func_list += [f for f in statfuncs if f not in param_func_list]
labels =  [param_func_to_label(f) for f in param_func_list]

# pad theta vector with zeros for the parameters not in the model
theta = np.array(list(theta) + (len(param_func_list)-len(theta))*[0])


assert len(param_func_list) == len(labels)
assert len(theta) == len(param_func_list)


simulate_from_network_attr(
    '../data/musae_git.net',
    param_func_list, labels, theta,
    iterationInStep = 100000,
    burnIn = 1000000
    )




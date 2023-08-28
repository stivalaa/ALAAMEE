#!/usr/bin/env python3
#
# File:    run runALAAMsimualteGoFexample.py
# Author:  Alex Stivala
# Created: June 2020
#
"""Run the simple demonstration implementation simulation from
   Autologistic Actor Attribute Model (ALAAM) parameters.
"""
from functools import partial
import numpy as np

from changeStatisticsALAAM import *
from simulateALAAM import simulate_from_network_attr

# parameters and corresponding labels 
# TODO parse frmo estimation output
param_func_list = [changeDensity, changeActivity, changeContagion, partial(changeoOb, "binaryAttribute"), partial(changeoOc, "continuousAttribute")]
labels = ["Density", "Activity", "Contagion", "Binary", "Continuous"]

# example results from alaamee_covariance_simexample-1151160.out
# Pooled
# Density -7.604183 0.8603461 0.9077859 0.07263692 * 
# Activity 0.6080458 0.1430582 0.08504583 0.02069999 * 
# Contagion 1.016383 0.08432854 0.3663313 0.09485121 * 
# Binary 1.274613 0.2081605 0.6249419 0.004049665 * 
# Continuous 1.08334 0.07026062 0.4265949 0.001842026 * 
# TotalRuns 100 
# ConvergedRuns 100 
# TODO parse these from estimation output
theta = np.array([-7.604183, 0.6080458, 1.016383, 1.274613, 1.08334])


# change stats functions to add to GoF if not already in estimation
statfuncs = [changeTwoStar, changeThreeStar, changePartnerActivityTwoPath,
             changeTriangleT1, changeContagion,
             changeIndirectPartnerAttribute,
             changePartnerAttributeActivity, 
             changePartnerPartnerAttribute,
             changeTriangleT2,
             changeTriangleT3]
statlabels = ['Two-Star', 'Three-Star', 'Alter-2Star1A',
              'T1', 'Contagion', 'Alter-2Star2A', 'Partner-Activity',
              'Partner-Resource','T2', 'T3']
gof_param_func_list = (list(param_func_list) +
                       [f for f in statfuncs
                        if f not in param_func_list])
goflabels = (list(labels) + [f for f in statlabels
                             if f not in labels])
n = len(gof_param_func_list)
assert len(goflabels) == n
# pad theta vector with zeros for the added parameters
gof_theta = np.array(list(theta) + (n-len(theta))*[0])


simulate_from_network_attr(
    '../data/simulated_n500_bin_cont2/n500_kstar_simulate12750000.txt',
    gof_param_func_list,
    goflabels, 
    gof_theta,
    '../data/simulated_n500_bin_cont2/binaryAttribute_50_50_n500.txt',
    '../data/simulated_n500_bin_cont2/continuousAttributes_n500.txt',
    outputSimulatedVectors = True
    )




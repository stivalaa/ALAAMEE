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
from math import log

from changeStatisticsALAAM import changeDensity,param_func_to_label
from changeStatisticsALAAMdirected import *
from simulateALAAM import simulate_from_network_attr
from parseEstimationEEOutput import parseEstimationEEOutput


###
### main
###

param_func_list =  [changeDensity, partial(changeGWSender, log(2.0)), partial(changeGWReceiver, log(2.0)), changeContagion]
theta = np.array([-1.68704826,  3.56490062, -0.24034214,  0.20616495])
labels =  [param_func_to_label(f) for f in param_func_list]


## Add extra statistics not in model for goodness-of-fit
statfuncs = [changeSender, changeReceiver, changeReciprocity,
             changeEgoInTwoStar, changeEgoOutTwoStar,
             changeMixedTwoStar, changeMixedTwoStarSource,
             changeMixedTwoStarSink, changeContagion,
             changeContagionReciprocity,
             changeTransitiveTriangleT1,
             changeTransitiveTriangleT3,
             changeTransitiveTriangleD1,
             changeTransitiveTriangleU1,
             changeCyclicTriangleC1,
             changeCyclicTriangleC3,
             changeAlterInTwoStar2,
             changeAlterOutTwoStar2]
param_func_list += [f for f in statfuncs if f not in param_func_list]
labels =  [param_func_to_label(f) for f in param_func_list]

# pad theta vector with zeros for the parameters not in the model
theta = np.array(list(theta) + (len(param_func_list)-len(theta))*[0])


assert len(param_func_list) == len(labels)
assert len(theta) == len(param_func_list)


simulate_from_network_attr(
    '../../../data/directed/HighSchoolFriendship/highschool_friendship_arclist.net',
    param_func_list, labels, theta,
    iterationInStep = 1000,
    burnIn = 10000,
    directed = True,
    outputSimulatedVectors = True
    )




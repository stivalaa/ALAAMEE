#!/usr/bin/env python3
#
# File:    run runALAAMsimulateGoFGithub.py
# Author:  Alex Stivala
# Created: April 2023
#
"""Simulate from  Autologistic Actor Attribute Model (ALAAM).
   
   Usage: runALAAMsimulateGoFGithub.py <estimated | negative | positive>

   estimated/negative/positive controls value of GWSender(log(2.0)) parameter:

     estimated - use estimated parameter value of GWSender
     zero      - use zero for GWSender
     negative  - use strongly negative parameter on GWSender
     positive  - use strongly positive parameter on GWSender
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

if len(sys.argv) != 2:
    sys.stderr.write("Usage: " + sys.argv[0] + " estimated | zero | negative | positive\n")
    sys.exit(1)

        
param_func_list =  [changeDensity, partial(changeGWSender, log(2.0))]

if sys.argv[1] == "estimated":
    ## parameters estimated from model with Density, GWSender(log(2)) only
    theta     = np.array([-0.44657605, 0.57893814])
elif sys.argv[1] == "zero":    
    ## Model with Density only is just logit of probability of node
    ## with outcome 1: p = 0.4029851; logit(p) = -0.3930425
    theta = np.array([-0.3930425, 0])    
elif sys.argv[1] == "negative":
    theta = np.array([-0.3930425, -15])
elif sys.argv[1] == "positive":
    theta = np.array([-0.3930425, -15])
else:
    sys.stderr.write("Usage: " + sys.argv[0] + " estimated | zero | negative | positive\n")
    sys.exit(1)
    

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
    outputSimulatedVectors = True,
    simvecFilePrefix = "sim_outcome_"+sys.argv[1]
    )




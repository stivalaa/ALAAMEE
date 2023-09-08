#!/usr/bin/env python3
#
# File:    run runALAAMsimulateGoFHighschoolModel6.py
# Author:  Alex Stivala
# Created: September 2023
#
"""Simulate from  Autologistic Actor Attribute Model (ALAAM).
   
   Usage: runALAAMsimulateGoFHighschoolModel6.py

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

        
param_func_list =  [changeDensity, partial(changeGWSender, log(2.0)), partial(changeGWReceiver, log(2.0)), changeContagion, changeReciprocity, changeContagionReciprocity, changeMixedTwoStarSource, changeMixedTwoStarSink, changeTransitiveTriangleT1, changeTransitiveTriangleT3, partial(changeSenderMatch, "class"), partial(changeReceiverMatch, "class"), partial(changeReciprocityMatch, "class")]

## theta vaules from alaam_sa_highschool_gender_gw_more.out
## TODO parse from SA output like parseEstimationEEOutput() does for EE output
theta     = np.array([-2.63655716,5.25906295,-0.57848754,0.72511577,-0.09219398,-1.04759659,0.02454693,-0.00771666,-0.04788056,-0.01170659,0.10484196,-0.03113242,0.18434274])

labels =  [param_func_to_label(f) for f in param_func_list]


## Add extra statistics if not in model for goodness-of-fit
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
    catattr_filename = '../../../data/directed/HighSchoolFriendship/highschool_friendship_catattr.txt',
    iterationInStep = 1000,
    burnIn = 10000,
    directed = True,
    outputSimulatedVectors = True,
    simvecFilePrefix = "sim_outcome_model6"
    )




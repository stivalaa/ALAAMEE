#!/usr/bin/env python3
#
# File:    runALAAMSAs50simpleModel.py
# Author:  Alex Stivala
# Created: May 2023
#
"""Run the python implementation of the Stochastic
 Approximation algorithm for estimation of Autologistic Actor Attribute
 Model (ALAAM) parameters on the directed network
 excerpt of 50 girls from 'Teenage Friends and Lifestyle Study' data
 from SIENA.

 See README file and downloadAndConvertSIENAs50DataToALAAMEEformat.R
 in this directory for more details.

 This version is a simple model similar to that shown in
 https://github.com/johankoskinen/ALAAM/blob/main/ALAAM%20tutorial.Rmd
 
"""
from functools import partial
import  estimateALAAMSA
from changeStatisticsALAAMdirected import *
from changeStatisticsALAAM import changeDensity, changeoOc, param_func_to_label

model_param_funcs =  [changeDensity, changeContagion, changeContagionReciprocity, partial(changeoOc, "sport"), partial(changeoOc, "alcohol"), changeSender, changeReciprocity]

gof_param_funcs = [changeDensity, changeSender, changeReceiver, changeContagion, changeReciprocity, changeContagionReciprocity, changeEgoInTwoStar, changeEgoOutTwoStar, changeMixedTwoStar, changeTransitiveTriangleT1, changeAlterInTwoStar2, changeAlterOutTwoStar2, changeTransitiveTriangleT3, changeCyclicTriangleC3]

estimateALAAMSA.run_on_network_attr(
        's50-friendships-directed.net',
        model_param_funcs,
        [param_func_to_label(f) for f in model_param_funcs],    
        outcome_bin_filename = 's50-outcome.txt',
        binattr_filename = 's50-binattr.txt',
        contattr_filename = 's50-contattr.txt',
        catattr_filename = 's50-catattr.txt',
        directed = True,
        gof_param_func_list = model_param_funcs + [f for f in gof_param_funcs if f not in model_param_funcs]     #TODO do this inside func instead
    )

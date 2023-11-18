#!/usr/bin/env python3
#
# File:    runALAAMSAs50GW.py
# Author:  Alex Stivala
# Created: May 2023
#
"""Run the python implementation of the Stochastic
 Approximation algorithm for estimation of Autologistic Actor Attribute
 Model (ALAAM) parameters on the directed network
 excerpt of 50 girls from 'Teenage Friends and Lifestyle Study' data
 from SIENA.

 This version uses the Getometrically Weighted Sender and Receiver
 parameters instead of simple Sender and Receiver.

 See README file and downloadAndConvertSIENAs50DataToALAAMEEformat.R
 in this directory for more details.
"""
from functools import partial
from math import log
import  estimateALAAMSA
from changeStatisticsALAAMdirected import *
from changeStatisticsALAAM import changeDensity, changeoOc, param_func_to_label

from gof_stats import gof_funcs

model_param_funcs =         [changeDensity, partial(changeGWSender, log(2.0)), partial(changeGWReceiver, log(2.0)), changeContagion, changeReciprocity, changeContagionReciprocity, changeEgoInTwoStar, changeEgoOutTwoStar, changeMixedTwoStar, changeTransitiveTriangleT1, partial(changeoOc, "sport"), partial(changeoOc, "alcohol")]

estimateALAAMSA.run_on_network_attr(
        's50-friendships-directed.net',
        model_param_funcs,
        [param_func_to_label(f) for f in model_param_funcs],
        outcome_bin_filename = 's50-outcome.txt',
        binattr_filename = 's50-binattr.txt',
        contattr_filename = 's50-contattr.txt',
        catattr_filename = 's50-catattr.txt',
        directed = True,
        add_gof_param_func_list = gof_funcs    
    )

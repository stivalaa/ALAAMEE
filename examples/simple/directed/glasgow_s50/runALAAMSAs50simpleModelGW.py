#!/usr/bin/env python3
#
# File:    runALAAMSAs50simpleModelGW.py
# Author:  Alex Stivala
# Created: August 2023
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
 but with Geometrically Weighted Sender rather than Sender.
 
"""
from functools import partial
from math import log
import  estimateALAAMSA
from changeStatisticsALAAMdirected import *
from changeStatisticsALAAM import changeDensity, changeoOc, param_func_to_label

from gof_stats import gof_funcs

model_param_funcs =         [changeDensity, changeContagion, changeContagionReciprocity, partial(changeoOc, "sport"), partial(changeoOc, "alcohol"), partial(changeGWSender, log(2.0)), changeReciprocity]

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

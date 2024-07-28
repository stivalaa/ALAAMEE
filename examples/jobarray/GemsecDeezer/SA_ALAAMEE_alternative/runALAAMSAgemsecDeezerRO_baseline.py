#!/usr/bin/env python3
#
# File:    runALAAMSAgemsecDeezerRO_baseline.py
# Author:  Alex Stivala
# Created: July 2024
#
"""Run the python implementation of the Stochastic
 Approximation algorithm for estimation of Autologistic Actor Attribute
 Model (ALAAM) parameters on the Deezer Europe network.
 This model is the "baseline" model that is equivalent to logistic
 regression, by not using any paramters related to more than 
 an individual node itself.
"""
from functools import partial

import  estimateALAAMSA
from changeStatisticsALAAM import *

param_func_list = [changeDensity,
                   partial(changeoOc, "num_genres")]

estimateALAAMSA.run_on_network_attr(
    '../data/deezer_ro_friendship.net',
    param_func_list,
    [param_func_to_label(f) for f in param_func_list],
    '../data/deezer_ro_outcome_alternative.txt',
    contattr_filename = '../data/deezer_ro_contattr.txt'
    )




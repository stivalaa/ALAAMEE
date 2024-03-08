#!/usr/bin/env python3
#
# File:    run ALAAMSAdeezer.py
# Author:  Alex Stivala
# Created: May 2023
#
"""Run the python implementation of the Stochastic
 Approximation algorithm for estimation of Autologistic Actor Attribute
 Model (ALAAM) parameters on the Deezer Europe network
"""
from functools import partial

import  estimateALAAMSA
from changeStatisticsALAAM import *

param_func_list = [changeDensity, partial(changeGWActivity, 2.0),
                   changeContagion,
                   partial(changeoOc, "num_genres"),
                   partial(changeo_Oc, "num_genres")]

estimateALAAMSA.run_on_network_attr(
    '../data/deezer_hr_friendship.net',
    param_func_list,
    [param_func_to_label(f) for f in param_func_list],
    '../data/deezer_hr_outcome.txt',
    contattr_filename = '../data/deezer_hr_contattr.txt'
    )




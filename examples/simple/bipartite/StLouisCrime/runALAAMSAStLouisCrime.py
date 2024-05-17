#!/usr/bin/env python3
#
# File:    run ALAAMSAStLouisCrime.py
# Author:  Alex Stivala
# Created: May 2023
#
"""Run the python implementation of the Stochastic
 Approximation algorithm for estimation of Autologistic Actor Attribute
 Model (ALAAM) parameters on the St Louis crime network
"""
from functools import partial

import estimateALAAMSA
from BipartiteGraph import MODE_A,MODE_B
from changeStatisticsALAAMbipartite import *
from changeStatisticsALAAM import changeoOc,changeo_Oc,param_func_to_label
from bipartiteALAAMsampler import bipartiteALAAMsampler

from model import param_func_list
from gof_stats import gof_funcs


estimateALAAMSA.run_on_network_attr(
    'crime_bipartite.net',
    param_func_list,
    [param_func_to_label(f) for f in param_func_list],
    'crime_outcome.txt',
    'crime_binattr.txt',
    'crime_contattr.txt',
    'crime_catattr.txt',
     sampler_func = partial(bipartiteALAAMsampler, MODE_A),
     bipartite = True,
     GoFiterationInStep = 10000,
     GoFburnIn = 100000,
     bipartiteGoFfixedMode = MODE_B,
     add_gof_param_func_list = gof_funcs
    )




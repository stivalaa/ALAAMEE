#!/usr/bin/env python3
#
# File:    run ALAAMSASeierstad_betweenness.py
# Author:  Alex Stivala
# Created: May 2024
#
"""Run the implementation of the Stochastic Approximation
 algorithm for estimation of Autologistic Actor Attribute
 Model (ALAAM) parameters. 

 Usage:
     python3 runALAAMSASeierstad_betweenness.py 
"""
from functools import partial

import estimateALAAMSA
from BipartiteGraph import MODE_A,MODE_B
from changeStatisticsALAAM import param_func_to_label
from bipartiteALAAMsampler import bipartiteALAAMsampler

from model_betweenness import param_func_list
from gof_stats import gof_funcs



def main():
    """
    See usage message in module header block
    """
    estimateALAAMSA.run_on_network_attr(
        'norwegian_director_interlock_20090801_bipartite.net',
        param_func_list,
        [param_func_to_label(f) for f in param_func_list],
        'norwegian_director_interlock_20090801_outcome.txt',
        'norwegian_director_interlock_20090801_binattr.txt',
        'norwegian_director_interlock_20090801_contattr.txt',
        'norwegian_director_interlock_20090801_catattr.txt',
        sampler_func = partial(bipartiteALAAMsampler, MODE_A),
        bipartite = True,
        GoFiterationInStep = 10000,
        GoFburnIn = 100000,
        bipartiteGoFfixedMode = MODE_B,
        add_gof_param_func_list = gof_funcs
    )


if __name__ == "__main__":
    main()



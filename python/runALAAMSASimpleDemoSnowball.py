#!/usr/bin/env python
#
# File:    run ALAAMSASimpleDemoSnowball.py
# Author:  Alex Stivala
# Created: March 2021
#
"""Run the simple demonstration implementation of the Stochastic
 Approximation algorithm for estimation of Autologistic Actor Attribute
 Model (ALAAM) parameters, on snowball sampled network data.
"""
from functools import partial

from conditionalALAAMsampler import conditionalALAAMsampler
from changeStatisticsALAAM import *
import  ALAAMSASimpleDemo

ALAAMSASimpleDemo.run_on_network_attr(
        'n500_kstar_simulate12750000_waves2_seeds10_num6700000.txt',
        [changeDensity, changeActivity, changeContagion, partial(changeoOb, "binaryAttribute"), partial(changeoOc, "continuousAttribute")],
        ["Density", "Activity", "Contagion", "Binary", "Continuous"],
        'sample-n500_bin_cont6700000_waves2_seeds10.txt',
        'binaryAttribute_50_50_n500_waves2_seeds10_num6700000.txt',
        'continuousAttributes_n500_waves2_seeds10_num6700000.txt',
        catattr_filename = None,
        sampler_func = conditionalALAAMsampler,
        zone_filename = 'snowball_zonefile_waves2_seeds10_num6700000.txt')



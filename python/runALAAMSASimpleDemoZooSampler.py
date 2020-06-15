#!/usr/bin/env python
#
# File:    run ALAAMSASimpleDemoZooSampler.py
# Author:  Alex Stivala
# Created: June 2020
#
"""Run the simple demonstration implementation of the Stochastic
 Approximation algorithm for estimation of Autologistic Actor Attribute
 Model (ALAAM) parameters with the Zero-Or-One (ZOO) ALAAM sampler
"""
from functools import partial

from zooALAAMsampler import zooALAAMsampler
from changeStatisticsALAAM import *
import  ALAAMSASimpleDemo


ALAAMSASimpleDemo.run_on_network_attr(
        '../data/simulated_n500_bin_cont2/n500_kstar_simulate12750000.txt',
        [changeDensity, changeActivity, changeContagion, partial(changeoOb, "binaryAttribute"), partial(changeoOc, "continuousAttribute")],
        ["Density", "Activity", "Contagion", "Binary", "Continuous"],
        '../data/simulated_n500_bin_cont2/sample-n500_bin_cont6700000.txt',
        '../data/simulated_n500_bin_cont2/binaryAttribute_50_50_n500.txt',
        '../data/simulated_n500_bin_cont2/continuousAttributes_n500.txt',
        sampler_func = zooALAAMsampler
    )

#!/usr/bin/env python3
#
# File:    runALAAMEESimpleDemoZooSampler.py
# Author:  Alex Stivala
# Created: June 2020
#
"""Run the python implementation of the Equilibrium
 Expectation algorithm for estimation of Autologistic Actor Attribute
 Model (ALAAM) parameters, using the Zero-Or-One (ZOO) sampler.
"""
from functools import partial

from zooALAAMsampler import zooALAAMsampler
from changeStatisticsALAAM import *
import  estimateALAAMEE

estimateALAAMEE.run_on_network_attr(
        '../data/simulated_n500_bin_cont2/n500_kstar_simulate12750000.txt',
        [changeDensity, changeActivity, changeContagion, partial(changeoOb, "binaryAttribute"), partial(changeoOc, "continuousAttribute")],
        ["Density", "Activity", "Contagion", "Binary", "Continuous"],
        '../data/simulated_n500_bin_cont2/sample-n500_bin_cont6700000.txt',
        '../data/simulated_n500_bin_cont2/binaryAttribute_50_50_n500.txt',
        '../data/simulated_n500_bin_cont2/continuousAttributes_n500.txt',
        sampler_func = zooALAAMsampler
    )

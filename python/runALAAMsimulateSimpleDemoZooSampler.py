#!/usr/bin/env python3
#
# File:    runALAAMsimulateSimpleDemoZooSampler.py
# Author:  Alex Stivala
# Created: June 2020
#
"""Run the python implementation simulation from
   Autologistic Actor Attribute Model (ALAAM) parameters using the 
   Zero-Or-One (ZOO) ALAAM sampler.
"""
from functools import partial
import numpy as np

from zooALAAMsampler import zooALAAMsampler
from changeStatisticsALAAM import *
import  simulateALAAMsimpleDemo


simulateALAAMsimpleDemo.simulate_from_network_attr(
        '../data/simulated_n500_bin_cont2/n500_kstar_simulate12750000.txt',
        [changeDensity, changeActivity, changeContagion, partial(changeoOb, "binaryAttribute"), partial(changeoOc, "continuousAttribute")],
        ["Density", "Activity", "Contagion", "Binary", "Continuous"],
        np.array([-7.2, 0.55, 1.0, 1.2, 1.15]),
        '../data/simulated_n500_bin_cont2/binaryAttribute_50_50_n500.txt',
        '../data/simulated_n500_bin_cont2/continuousAttributes_n500.txt',
        sampler_func = zooALAAMsampler
    )




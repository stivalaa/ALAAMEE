#!/usr/bin/env python
#
# File:    run runALAAMsimualteGoFexample.py
# Author:  Alex Stivala
# Created: June 2020
#
"""Run the simple demonstration implementation simulation from
   Autologistic Actor Attribute Model (ALAAM) parameters.
"""
from functools import partial
import numpy as np

from changeStatisticsALAAM import *
import  simulateALAAMsimpleDemo


simulateALAAMsimpleDemo.simulate_from_network_attr(
    '../data/simulated_n500_bin_cont2/n500_kstar_simulate12750000.txt',
    [changeDensity, changeActivity, changeContagion, partial(changeoOb, "binaryAttribute"), partial(changeoOc, "continuousAttribute")],
    ["Density", "Activity", "Contagion", "Binary", "Continuous"],
    # example results from alaamee_covariance_simexample-1151160.out
    # Pooled
    # Density -7.604183 0.8603461 0.9077859 0.07263692 * 
    # Activity 0.6080458 0.1430582 0.08504583 0.02069999 * 
    # Contagion 1.016383 0.08432854 0.3663313 0.09485121 * 
    # Binary 1.274613 0.2081605 0.6249419 0.004049665 * 
    # Continuous 1.08334 0.07026062 0.4265949 0.001842026 * 
    # TotalRuns 100 
    # ConvergedRuns 100 
    # TODO parse these from estimation output
    np.array([-7.604183, 0.6080458, 1.016383, 1.274613, 1.08334]),
    '../data/simulated_n500_bin_cont2/binaryAttribute_50_50_n500.txt',
    '../data/simulated_n500_bin_cont2/continuousAttributes_n500.txt'
    )




#!/usr/bin/env python3
#
# File:    runALAAMSASimpleDemoN1000.py
# Author:  Alex Stivala
# Created: May 2020
#
"""Run the python implementation of the Stochastic
 Approximation algorithm for estimation of Autologistic Actor Attribute
 Model (ALAAM) parameters with simualted 1000 node network.
"""
from functools import partial
import  estimateALAAMSA
from changeStatisticsALAAM import *

estimateALAAMSA.run_on_network_attr(
        '../data/simulated_n1000_bin_cont/n1000_kstar_simulate12750000.txt',
        [changeDensity, changeActivity, changeContagion, partial(changeoOb, "binaryAttribute"), partial(changeoOc, "continuousAttribute")],
        ["Density", "Activity", "Contagion", "Binary", "Continuous"],
        '../data/simulated_n1000_bin_cont/sample-n1000_bin_cont3800000.txt',
        '../data/simulated_n1000_bin_cont/binaryAttribute_50_50_n1000.txt',
        '../data/simulated_n1000_bin_cont/continuousAttributes_n1000.txt'
    )

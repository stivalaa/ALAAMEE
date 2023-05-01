#!/usr/bin/env python3
#
# File:    runALAAMSAs50simpleModel.py
# Author:  Alex Stivala
# Created: May 2023
#
"""Run the python implementation of the Stochastic
 Approximation algorithm for estimation of Autologistic Actor Attribute
 Model (ALAAM) parameters on the directed network
 excerpt of 50 girls from 'Teenage Friends and Lifestyle Study' data
 from SIENA.

 See README file and downloadAndConvertSIENAs50DataToALAAMEEformat.R
 in this directory for more details.

 This version is a simple model similar to that shown in
 https://github.com/johankoskinen/ALAAM/blob/main/ALAAM%20tutorial.Rmd
 
"""
from functools import partial
import  estimateALAAMSA
from changeStatisticsALAAMdirected import *
from changeStatisticsALAAM import changeDensity, changeoOc

estimateALAAMSA.run_on_network_attr(
        's50-friendships-directed.net',
        [changeDensity, changeContagion, changeContagionReciprocity, partial(changeoOc, "sport"), partial(changeoOc, "alcohol"), changeSender, changeReciprocity],
        ["Density",     "Contagion",     "ContagionReciprocity",     "sport_oOc",                 "alcohol_oOc",                 "Sender",     "Reciprocity"],
        outcome_bin_filename = 's50-outcome.txt',
        binattr_filename = 's50-binattr.txt',
        contattr_filename = 's50-contattr.txt',
        catattr_filename = 's50-catattr.txt',
        directed = True
    )
#!/usr/bin/env python3
#
# File:    runALAAMSAbadgersMore.py
# Author:  Alex Stivala
# Created: May 2023
#
"""Run the python implementation of the Stochastic
 Approximation algorithm for estimation of Autologistic Actor Attribute
 Model (ALAAM) parameters on the undirected network

 See README file and convertBadgerDataToALAAMEEFormat.R in ./data/
 directory for more details, as well as:

     Silk, M. J., Croft, D. P., Delahay, R. J., Hodgson, D. J.,
     Weber, N., Boots, M., & McDonald, R. A. (2017). 
     The application of statistical network models in disease research. 
     Methods in Ecology and Evolution, 8(9), 1026-1041.
 

This model is similar to the network autocorrelation model in the S.I.
of the above paper (included in zip file in data directory).

"""
from functools import partial
import  estimateALAAMSA
from changeStatisticsALAAM import *

param_func_list =  [changeDensity, changeActivity, changeContagion, 
                    changePartnerActivityTwoPath,
                    changeTriangleT1, changeTriangleT3,
                    partial(changeoOb, "male"),
                    partial(changeoOb, "yearling"),
                    partial(changeoOc, "betweenGroupFlowCent")]

estimateALAAMSA.run_on_network_attr(
        'data/badgers_overallnetwork.net',
        param_func_list,
        [param_func_to_label(f) for f in param_func_list],
        outcome_bin_filename = 'data/badgers_TBpos.txt',
        binattr_filename = 'data/badgers_binattr.txt',
        contattr_filename = 'data/badgers_contattr.txt',
        catattr_filename = 'data/badgers_catattr.txt',
        directed = False
    )

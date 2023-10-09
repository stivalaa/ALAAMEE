#!/usr/bin/env python3
#
# File:    runALAAMSAdevilsSimpleModel.py
# Author:  Alex Stivala
# Created: October 2023
#
"""Run the python implementation of the Stochastic
 Approximation algorithm for estimation of Autologistic Actor Attribute
 Model (ALAAM) parameters on the Tasmanian Devils contact network with
 devil facial tumour disease (DFTD) as binary outcmoe variable.

  See convertDevilDataToALAAMEEFormat.R for details of data, and reference:

   Hamilton, D. G., Jones, M. E., Cameron, E. Z., Kerlin, D. H.,
   McCallum, H., Storfer, A., ... & Hamede, R. K. (2020). Infectious
   disease and sickness behaviour: tumour progression affects
   interaction patterns and social network structure in wild
   Tasmanian devils. Proceedings of the Royal Society B, 287(1940),
   20202454.

For network autocorrelation model with the same outcome variable see
Chapter 5 (Table 5.2, p. 145) of:

   Hamilton, D. G. (2020). Behaviour, social networks and transmission
   of devil facial tumour disease (Doctoral dissertation, University
   Of Tasmania). https://figshare.utas.edu.au/articles/thesis/Behaviour_social_networks_and_transmission_of_devil_facial_tumour_disease/23249180`

"""
from functools import partial
import  estimateALAAMSA
from changeStatisticsALAAM import *

param_func_list =  [changeDensity, changeActivity, changeContagion, 
                    partial(changeoOb, "male"),
                    partial(changeoOc, "wounds")]

## Takes about 7 minutes to run, only 1 minute for estimation but 6 for GoF
## (probably because GoF includes triangle statistics and this model does not,
## and this network is dense)
estimateALAAMSA.run_on_network_attr(
        'devils_contact_all.net',
        param_func_list,
        [param_func_to_label(f) for f in param_func_list],
        outcome_bin_filename = 'devils_DFTD_status_all.txt',
        binattr_filename = 'devils_binattr_all.txt',
        contattr_filename = 'devils_contattr_all.txt',
        catattr_filename = 'devils_catattr_all.txt',
        directed = False
    )

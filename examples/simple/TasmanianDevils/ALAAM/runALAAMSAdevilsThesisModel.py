#!/usr/bin/env python3
#
# File:    runALAAMSAdevilsThesisModel.py
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

This model is the ALAAM equivalent of the network autocorrelation model
in Table 5.2 of the Hamilton (2020) thesis (although here we use all time
periods, without separating in to mating and non-mating seasons)

"""
from functools import partial
import  estimateALAAMSA
from changeStatisticsALAAM import *

## Note very high correlations (> 0.9) between betweenness, closeness, degree
## (and correlation between closeness and degree centralities is  > 0.99)
## Also large negative correlations (< -0.75) between clustering coef. and
## all three centrality measures. 

## Not including Activity to make model equivalent to network autocorrelation
## model (it will also be correlated with degree most likely)
param_func_list =  [changeDensity, changeContagion, 
                    partial(changeoOb, "male"),
                    partial(changeoOc, "wounds"),
                    partial(changeoOc, "degree_cent"),
                    partial(changeoOc, "betweenness_cent"),
                    partial(changeoOc, "closeness_cent"),
                    partial(changeoOc, "clustering_coef")]

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

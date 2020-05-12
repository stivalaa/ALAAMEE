#!/usr/bin/env python
#
# File:    run ALAAMSAkarateClub.py
# Author:  Alex Stivala
# Created: Februrary 2020
#
"""Run the simple demonstration implementation of the Stochastic
 Approximation algorithm for estimation of Autologistic Actor Attribute
 Model (ALAAM) parameters on the Zachary Karate Club example.
"""


import  ALAAMSASimpleDemo
from changeStatisticsALAAM import *

ALAAMSASimpleDemo.run_on_network_attr(
    '../data/karate_club/karate.net',
    [changeDensity, changeActivity, changeTwoStar, changeThreeStar, changeContagion, changeTriangleT1, changeTriangleT2, changeTriangleT3, changeIndirectPartnerAttribute, changePartnerAttributeActivity, changePartnerPartnerAttribute],
    ["Density", "Activity", "Star2", "Star3", "Contagion", "T1", "T2", "T3", "2-Path-Equivalence", "Partner-Attribute-Activity", "Partner-Resource"],
    '../data/karate_club/karate_outcome.txt',
    '../data/karate_club/karate_binattr.txt',
    '../data/karate_club/karate_contattr.txt'
    )




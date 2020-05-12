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
    [changeDensity, changeActivity, changeTwoStar, changeThreeStar, changeContagion, changeTriangleT1, changeTriangleT2, changeTriangleT3, changeIndirectPartnerAttribute, changePartnerAttributeActivity, changePartnerPartnerAttribute, changeoOb, changeo_Ob, changeoOc, changeo_Oc, changeoO_Osame],
    ["Density", "Activity", "Star2", "Star3", "Contagion", "T1", "T2", "T3", "2-Path-Equivalence", "Partner-Attribute-Activity", "Partner-Resource", "senior_oOb", "senior_o_Ob", "age_oOc", "age_o_Oc", "gender_match"],
    '../data/karate_club/karate_outcome.txt',
    '../data/karate_club/karate_binattr.txt',
    '../data/karate_club/karate_contattr.txt',
    '../data/karate_club/karate_catattr.txt'
    )



